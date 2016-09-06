from sourcecode import *
import math

### Test Case 1 ###

# Simple goal(unchanged)
# Vary # of variables
# 1.number of variables growing linearly
# 2.number of variables growing exponentially
def testcase1():

	varlist1 = []
	varlist2 = []
	for i in range(100):
		varlist1.append("x" + str(i))
		varlist2.append("y" + str(i))
	goal1 = "x0"
	goal2 = "!y0"

	var1 = varlist1[0:7]
	var2 = varlist2[0:7]
	print var1
	print var2
	translateEach(var1,var2,goal1,goal2)

	# 1:n setting
	'''
	var1 = varlist1[0:6]
	for i in range(6):
		var2 = varlist2[0:(i+1)] # linear
		#var2 = varlist2[0:int(math.pow(2,i))] # exponential
		print var1
		print var2
		translateEach(var1,var2,goal1,goal2)
	'''
	'''
	# n:n setting
	for i in range(10):
		# linear
		var1 = varlist1[0:(i+1)] 
		var2 = varlist2[0:(i+1)] 
		print var1
		print var2
		translateAll(var1,var2,goal1,goal2)
	'''

### Test Case 2 ###

# Simple varibales(unchanged)
# Vary the scope(complexity) of goals
# 1.Only with F
# 2.Only with G
# 3.Only with U
# 4.Full LTL: X,U,F,G
def testcase2_1():
	'''
	var1 = ["x0","x1"]
	var2 = ["y0","y1"]
	goallist1 = ["F x0","F x0 and y1","F (x0 and y1) or !y0","F (y0 and x1) or F!y0 and x1"]
	goallist2 = ["F !y0","F !y0 and x1","F (!y0 and x0) or !x1","F (!y0 and x1) or F y1 and !x0"]
	'''

	var1 = ["x0","x1","x2"]
	var2 = ["y0","y1","y2"]
	goallist1 = ["F x0 and y1","F (x0 and y1) or !y2","F (y1 and x1) or F !y2 and x2"]
	goallist2 = ["F !y0 and x1","F (!y0 and x1) or !x2","F (!y0 and x0) or F y2 and !x1"]
	for i in range(len(goallist1)):
		goal1 = goallist1[i]
		goal2 = goallist2[i]
		print goal1
		print goal2
		translateAll(var1,var2,goal1,goal2)

def testcase2_2():
	'''
	var1 = ["x0","x1"]
	var2 = ["y0","y1"]
	goallist1 = ["G x0","G x0 and y1","G (x0 and y1) or !y0","G (y0 and x1) or G!y0 and x1"]
	goallist2 = ["G !y0","G !y0 and x1","G (!y0 and x0) or !x1","G (!y0 and x1) or G y1 and !x0"]
	'''
	'''
	var1 = ["x0","x1","x2"]
	var2 = ["y0","y1","y2"]
	goallist1 = ["G x0 and y1","G (x0 and y1) or !y2","G (y1 and x1) or G !y2 and x2","G (y1 and x1) or G (!y2 and x2) and (x0 or y0)"]
	goallist2 = ["G !y0 and x1","G (!y0 and x1) or !x2","G (!y0 and x0) or G (y2 and !x1)","G (!y0 and x0) or G (y2 and !x1) and (x2 or y1)"]
	'''
	var1 = ["x0","x1","x2","x3"]
	var2 = ["y0","y1","y2","y3"]
	goallist1 = ["x0","G x0","G x0 and y1","G (x0 and y1) or !y2","G (y1 and x1) or G !y2 and x2","G (y1 and x1) or G (!y2 and x2) and (x0 or y0)"]
	goallist2 = ["!y0","G !y0","G !y0 and x1","G (!y0 and x1) or !x2","G (!y0 and x0) or G (y2 and !x1)","G (!y0 and x0) or G (y2 and !x1) and (x2 or y1)"]

	for i in range(len(goallist1)):
		goal1 = goallist1[i]
		goal2 = goallist2[i]
		print goal1
		print goal2
		translateAll(var1,var2,goal1,goal2)

def testcase2_3():
	'''
	var1 = ["x0","x1"]
	var2 = ["y0","y1"]
	goallist1 = ["x0 U y0","(x0 U y1) or (!y0 U x1)","((x0 U y0) and !y1 ) or (y1 U !x1)"]
	goallist2 = ["!x0 U !y0","(!x0 U !y1) or (y0 U x1)","((!x0 U !y0) and x1 ) or (!y1 U x1)"]
	'''

	var1 = ["x0","x1","x2"]
	var2 = ["y0","y1","y2"]
	goallist1 = ["x0 U y0","(x0 U y1) or (!y0 U x1)","((x0 U y0) and !y1 ) or (y2 U !x1 and x2)"]
	goallist2 = ["!x0 U !y0","(!x0 U !y1) or (y0 U x1)","((!x0 U !y0) and x1 ) or (!y1 U x2 and y2)"]

	for i in range(len(goallist1)):
		goal1 = goallist1[i]
		goal2 = goallist2[i]
		print goal1
		print goal2
		translateAll(var1,var2,goal1,goal2)

def testcase2_4():
	'''
	var1 = ["x0","x1"]
	var2 = ["y0","y1"]
	goallist1 = ["G F (x0 U y0)","G F (x0 U y1) and X(!y0 U x1)","G F ((x1 U y0) and !y1 ) or ( X y1 U !x0)"]
	goallist2 = ["G F (!x0 U !y0)","G F (!x0 U !y1) or X(y1 U x1)","G F ((!x1 U !y0) and x0 ) or X (!y1 U x0)"]
	'''

	var1 = ["x0","x1","x2"]
	var2 = ["y0","y1","y2"]
	goallist1 = ["G F (x0 U y0)","G F (x0 U y1) and X(!y0 U x1)","G F ((x1 U y0) and !y1 ) or ( X y1 U !x0)"]
	goallist2 = ["G F (!x0 U !y0)","G F (!x0 U !y1) or X(y2 U x1)","G F ((!x1 U !y0) and x0 ) or X (!y1 U x0)"]

	for i in range(len(goallist1)):
		goal1 = goallist1[i]
		goal2 = goallist2[i]
		print goal1
		print goal2
		translateAll(var1,var2,goal1,goal2)

def testcase3():
	'''
	var1 = ["x0","x1"]
	var2 = ["y0","y1"]
	goallist1 = ["G F (x0 U y0)","G F (x0 U y1) and X(!y0 U x1)","G F ((x1 U y0) and !y1 ) or ( X y1 U !x0)"]
	goallist2 = ["G F (!x0 U !y0)","G F (!x0 U !y1) or X(y1 U x1)","G F ((!x1 U !y0) and x0 ) or X (!y1 U x0)"]
	'''

	var1 = ["x0","x1","x2"]
	var2 = ["y0","y1","y2"]
	goallist1 = ["G F (x0 U x1)","G F (x0 U y1) and X(!y0 U x1)","G F ((x1 U y0) and !y1 ) or ( X y1 U !x0)"]
	goallist2 = ["G F (!y0 U !y1)","G F (!x0 U !y1) or X(y2 U x1)","G F ((!x1 U !y0) and x0 ) or X (!y1 U x0)"]


	for i in range(len(goallist1)):
		goal1 = goallist1[i]
		goal2 = goallist2[i]
		print goal1
		print goal2
		translateAll(var1,var2,goal1,goal2)

### Main ###
testcase1()