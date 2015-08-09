import beam
import analyse
def momentX(my_beam,x):
	net_moment=0
	
	if x<=0:
		return 0
	
	if x>my_beam.BEAM_LENGTH:
		return 0
	
	for position in my_beam.VERTICAL_REACTIONS:
		if position<=x:
			net_moment+=(x-position)*my_beam.VERTICAL_REACTIONS[position]

	for position in my_beam.LOADS:
		if position <=x:
			net_moment-=(x-position)*my_beam.LOADS[position]

	for dl in my_beam.DL:
		if x>dl["start"] and x<=dl["end"]:
			net_moment-=analyse.momentDLInt(dl,dl["start"],x,x)
		elif x>dl["end"]:
			net_moment-=analyse.momentDLInT(dl,dl["start"],dl["end"],x)
	return net_moment
