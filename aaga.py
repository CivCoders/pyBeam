import numpy as np
import sys,subprocess
import help
import analyse
import beam
my_beam=beam.Beam()

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
	if my_beam.HAS_BEAM==0:
		print "No beam selected"
		return
	my_beam.BEAM_LENGTH=0
	my_beam.SUPPORTS={}
	my_beam.LOADS={}
	my_beam.VERTICAL_REACTIONS={}
	my_beam.HAS_BEAM=0
	eudlIndex=0
	print "Beam Destroyed"
	return

def createBeam():
	#global BEAM_LENGTH,HAS_BEAM
	if my_beam.HAS_BEAM==1:
		print "Already loaded a beam please destroy the previous beam to proceed"
		return
	print "Enter the length of the beam:"
	my_beam.BEAM_LENGTH=float(raw_input())
	my_beam.HAS_BEAM=1
	print "created a new Beam"

def showBeam():
	#global BEAM_LENGTH,HAS_BEAM,LOADS,SUPPORTS
	if my_beam.HAS_BEAM!=1:
		print "No beam to show,Please add a beam"
		return
	print "Beam Specs\n=========="
	print "Beam length: "+str(my_beam.BEAM_LENGTH)
	showSupports()
	showLoads()
	analyse.calculateReactions(my_beam)
	#calculateReactions()

def addSupports():
	#global SUPPORTS,HAS_BEAM
	if my_beam.HAS_BEAM!=1:
		print "Please create a beam to add supports"
		return
	ch="m"
	while(ch=='m'):
		if len(my_beam.SUPPORTS)==2:
			return "cannot add more supports to a determinate structure"
		print "Enter the position of support"
		position=float(raw_input())
		print "Enter the type of support"
		my_beam.SUPPORTS[position]=raw_input()
		print "Press m to enter more supports"
		ch=str(raw_input())
	return "Supports Added"

def addLoads():
	#global LOADS,HAS_BEAM
	if my_beam.HAS_BEAM!=1:
		print "Please create a beam before adding loads"
		return
	ch="m"
	while(ch=="m"):
		print "Enter Load position:"
		position=float(raw_input())
		if position>my_beam.BEAM_LENGTH or position<0:
			print "Invalid load position"
			sys.exit(1)
		print "Enter Load Value:"
		load_value=float(raw_input())
		my_beam.LOADS[position]=load_value
		print "Press m to enter more loads"
		ch=str(raw_input())
	return "Loads Added"

def addDistributedLoads():
	if my_beam.HAS_BEAM!=1:
		print "Please create a beam before adding loads"
		return
	ch='m'
	while(ch=='m'):
		dl={}
		print "Enter the starting position"
		dl["start"]=float(raw_input())
		if dl["start"]>my_beam.BEAM_LENGTH or dl["start"]<0:
			print "Invalid position"
			sys.exit(1)
		print "Enter the end position"
		dl["end"]=float(raw_input())
		if dl["end"]>my_beam.BEAM_LENGTH or dl["end"]<0 or dl["end"]<dl["start"]:
			print "Invalid position"
			sys.exit(1)
		print "Enter the starting Intensity"
		dl["start_int"]=float(raw_input())
		print "Enter the ending Intensity"
		dl["end_int"]=float(raw_input())
		my_beam.DL.append(dl)
		print "Press m to enter more DLs"
		ch=str(raw_input())
	return "DLs added"


def showSupports():
	print "--------\nSupports\n--------"
	for position in my_beam.SUPPORTS:
		print "Support at x="+str(position)+" : "+my_beam.SUPPORTS[position]
	return

def showLoads():
	print "-----\nLoads\n-----"
	for position in my_beam.LOADS:
		print "Load at x="+str(position)+" : "+str(my_beam.LOADS[position])
	return

def takeAction(x):
	try:
		return{
			"CB":createBeam,
			"SB":showBeam,
			"DB":destroyBeam,
			"AS":addSupports,
			"AL":addLoads,
			"ADL":addDistributedLoads,
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
