import numpy as np
import sys,subprocess
import help
import analyse
import beam
my_beam=beam.Beam()
#BEAM_LENGTH=0
#SUPPORTS={}
#LOADS={}
#VERTICAL_REACTIONS={}
#HAS_BEAM=0



def errorHandler():
	print "Unrecognised command"

def exitProgram():
	print "closing"
	sys.exit(0)

def clearScreen():
	a=subprocess.call('clear')
	print "PyBeam-open source beam analysis program"
	print "========================================"
	print "(Type help for help)"


def destroyBeam():
	global BEAM_LENGTH,SUPPORTS,LOADS,VERTICAL_REACTIONS,HAS_BEAM
	if HAS_BEAM==0:
		print "No beam selected"
		return
	BEAM_LENGTH=0
	SUPPORTS={}
	LOADS={}
	VERTICAL_REACTIONS={}
	HAS_BEAM=0
	eudlIndex=0
	print "Beam Destroyed"
	return

def createBeam():
	global BEAM_LENGTH,HAS_BEAM
	if HAS_BEAM==1:
		print "Already loaded a beam please destroy the previous beam to proceed"
		return
	print "Enter the length of the beam:"
	BEAM_LENGTH=float(raw_input())
	HAS_BEAM=1
	print "created a new Beam"

def showBeam():
	global BEAM_LENGTH,HAS_BEAM,LOADS,SUPPORTS
	if HAS_BEAM!=1:
		print "No beam to show,Please add a beam"
		return
	print "Beam Specs\n=========="
	print "Beam length: "+str(BEAM_LENGTH)
	showSupports()
	showLoads()
	analyse.calculateReactions(BEAM_LENGTH,LOADS,SUPPORTS,VERTICAL_REACTIONS)
	#calculateReactions()

def addSupports():
	global SUPPORTS,HAS_BEAM
	if HAS_BEAM!=1:
		print "Please create a beam to add supports"
		return
	ch="m"
	while(ch=='m'):
		if len(SUPPORTS)==2:
			return "cannot add more supports to a determinate structure"
		print "Enter the position of support"
		position=float(raw_input())
		print "Enter the type of support"
		SUPPORTS[position]=raw_input()
		print "Press m to enter more supports"
		ch=str(raw_input())
	return "Supports Added"

def addLoads():
	global LOADS,HAS_BEAM
	if HAS_BEAM!=1:
		print "Please create a beam before adding loads"
		return
	ch="m"
	while(ch=="m"):
		print "Enter Load position:"
		position=float(raw_input())
		if position>BEAM_LENGTH or position<0:
			print "Invalid load position"
			sys.exit(1)
		print "Enter Load Value:"
		load_value=float(raw_input())
		LOADS[position]=load_value
		print "Press m to enter more loads"
		ch=str(raw_input())
	return "Loads Added"

def showSupports():
	print "--------\nSupports\n--------"
	for position in SUPPORTS:
		print "Support at x="+str(position)+" : "+SUPPORTS[position]
	return

def showLoads():
	print "-----\nLoads\n-----"
	for position in LOADS:
		print "Load at x="+str(position)+" : "+str(LOADS[position])
	return

def calculateReactions():
	global	BEAM_LENGTH,LOADS,SUPPORTS
	force_LHS=[]
	moment_LHS=[]
	sum_loads=0
	moment_loads=0
	for position in SUPPORTS:
		force_LHS.append(1)
		moment_LHS.append(position)
	for position in LOADS:
		sum_loads+=LOADS[position]
		moment_loads+=position*LOADS[position]
	LHS=np.array([force_LHS,moment_LHS])
	RHS=np.array([sum_loads,moment_loads])
	reactions=np.linalg.solve(LHS,RHS)
	reaction_index=0
	print "---------\nReactions\n---------"
	for position in SUPPORTS:
		VERTICAL_REACTIONS[position]=reactions[reaction_index]
		reaction_index+=1
	for position in VERTICAL_REACTIONS:
		print "Reaction at "+str(position)+" is "+str(VERTICAL_REACTIONS[position])

def takeAction(x):
	try:
		return{
			"CB":createBeam,
			"SB":showBeam,
			"DB":destroyBeam,
			"AS":addSupports,
			"AL":addLoads,
			"X" :exitProgram,
			"CLS":clearScreen,
			"help":help.helper
		}[x]

	except:
		errorHandler()

def main():
	print "PyBeam-open source beam analysis program"
	print "========================================"
	print "(Type help for help)"
	ch=""
	while(ch!="X"):
		ch=raw_input()
		try:
			takeAction(ch)()
		except:
			pass


if __name__=='__main__':
	main()
