import numpy as np
import beam
import moment
from matplotlib.offsetbox import AnnotationBbox, OffsetImage
from matplotlib._png import read_png
from numpy import trapz
import matplotlib.pyplot as plt

def calculateReactions(my_beam):
	force_LHS=[]
	moment_LHS=[]
	sum_loads=0
	moment_loads=0

	for position in my_beam.SUPPORTS:
		force_LHS.append(1)
		moment_LHS.append(position)

	for position in my_beam.LOADS:
		sum_loads+=my_beam.LOADS[position]
		moment_loads+=position*my_beam.LOADS[position]

	for dl in my_beam.DL:
		sum_loads+=shearDLInt(dl,dl["start"],dl["end"])
		moment_loads+=momentDLAboutO(dl)

	LHS=np.array([force_LHS,moment_LHS])
	RHS=np.array([sum_loads,moment_loads])
	reactions=np.linalg.solve(LHS,RHS)
	reaction_index=0
	print "---------\nReactions\n---------"
	for position in my_beam.SUPPORTS:
		my_beam.VERTICAL_REACTIONS[position]=reactions[reaction_index]
		reaction_index+=1
	for position in my_beam.VERTICAL_REACTIONS:
		print "Reaction at "+str(position)+" is "+str(my_beam.VERTICAL_REACTIONS[position])
	plotSFD(my_beam)
	plotBMD(my_beam)
	return

def forceAtX(my_beam,x):
	if x<0:
		return 0
	if x>my_beam.BEAM_LENGTH:
		return 0
	v=0
	for position in my_beam.VERTICAL_REACTIONS:
		if position<=x:
			v-=my_beam.VERTICAL_REACTIONS[position]
	for position in my_beam.LOADS:
		if position>x:
			return v
		v+=my_beam.LOADS[position]

	for dl in my_beam.DL:
		if x>=dl["start"] and x<=dl["end"]:
			v+=shearDLInt(dl,dl["start"],x)
		elif position>dl["end"]:
			v+=shearDLInt(dl,dl["start"],dl["end"])
		print v
	return -v

def momentDLAboutO(dl):
	h=0.01
	start=dl["start"]
	end=dl["end"]
	sum=0
	while start<=end-h:
		sum+=start*(getDLAtX(dl,start)+getDLAtX(dl,start+h))*h/2
		start+=h
	return sum

def momentDLInt(dl,first,last,position):
	sum=0
	h=0.01
	while last>first+h:
		sum+=(getDLAtX(dl,last)+getDLAtX(dl,last-h))*h*(position-last)/2
		last-=h
	return sum

def shearDLInt(dl,first,last):
	h=0.01
	sum=0
	while(last>first+h):
		temp=(getDLAtX(dl,last)+getDLAtX(dl,last-h))*h/2
		sum+=temp
		last-=h
	return sum
		

def getDLAtX(dl,x):
	if x<dl["start"]:
		return 0
	else:
		slope=(dl["end_int"]-dl["start_int"])/(dl["end"]-dl["start"])
		return (slope*(x-dl["start"])+dl["start_int"])
	

def plotSFD(my_beam):
	x=np.arange(-0.00099,my_beam.BEAM_LENGTH+0.01,0.01)

	forces=[]
	for i in x:
		forces.append(forceAtX(my_beam,i))

	moments=[]
	for i in x:
		moments.append(moment.momentX(my_beam,i))
	
	supp_pos=[]
	supp_base=[]
	for i in my_beam.VERTICAL_REACTIONS:
		supp_pos.append(i)
		supp_base.append(0)
	plt.xlim(-my_beam.BEAM_LENGTH/2,my_beam.BEAM_LENGTH*3/2)
	plt.plot(supp_pos,supp_base,'^')	#supports
	plt.plot(x,x*0,'b--')				#beam
	plt.plot(x,forces,'r')				#shear force diagram
	plt.show()


def plotBMD(my_beam):
	x=np.arange(-0.00099,my_beam.BEAM_LENGTH+0.01,0.01)
	supp_pos=[]
	supp_base=[]
	for i in my_beam.VERTICAL_REACTIONS:
		supp_pos.append(i)
		supp_base.append(0)
	
	moments=[]
	for i in x:
		moments.append(moment.momentX(my_beam,i))

	plt.xlim(-my_beam.BEAM_LENGTH/2,my_beam.BEAM_LENGTH*3/2)
	plt.ylim(-max(moments)*3/2,max(moments)*3/2)

	plt.plot(supp_pos,supp_base,'^')	#supports
	plt.plot(x,x*0,'b--')				#beam
	plt.plot(x,moments,'g')				#bending moment diagram
	plt.show()
	
	
