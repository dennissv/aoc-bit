import sys
import math

#python jesper.py input_jesper.txt
def cost(weigth):
	return( math.floor( weigth/3.0 )-2 )

fuel_cost=[]
adjusted_cost=[]
for line in open(sys.argv[1]):
	weigth=int(line.strip())
	fuel_cost.append( cost( weigth ) )
	adjusted_cost.append(fuel_cost[-1])

	while True:
		if cost( adjusted_cost[-1] ) > 0:
			adjusted_cost.append(cost(adjusted_cost[-1]))
		else:
			break

#unadjusted fuel cost
print( sum(fuel_cost) )
#adjusted fuel cost
print (sum(adjusted_cost))
