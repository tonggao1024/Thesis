### Test Case 1 ###

# Simple goal(unchanged)
# Vary # of variables
# number of variables growing exponentially

from sourcecode import *

varlist1 = ["x0","x1","x2","x3","x4","x5","x6","x7","x8","x9","x10"]
varlist2 = ["y0","y1","y2","y3","y4","y5","y6","y7","y8","y9","y10"]
goal1 = "x0 and y0"
goal2 = "!x0 and !y0"

var1 = varlist1[0:1]
for i in range(len(varlist2)):
	var2 = varlist2[0:(i+1)]
	translateAll(var1,var2,goal1,goal2)