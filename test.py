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

	# 1:n setting
	'''
	var1 = varlist1[0:1]
	for i in range(7):
		# var2 = varlist2[0:(i+1)] # linear
		var2 = varlist2[0:int(math.pow(2,i))] # exponential
		print var1
		print var2
		translateAll(var1,var2,goal1,goal2)
	'''

	# n:n setting
	for i in range(10):
		# linear
		var1 = varlist1[0:(i+1)] 
		var2 = varlist2[0:(i+1)] 
		print var1
		print var2
		translateAll(var1,var2,goal1,goal2)


### Test Case 2 ###

# Simple varibales(unchanged)
# Vary the scope(complexity) of goals
# 1.Only with F
# 2.Only with G
# 3.Only with U
# 4.Full LTL: X,U,F,G
def testcase2_1():

	var1 = ["x0"]
	var2 = ["y0"]
	goallist1 = ["F x0","F x0 and y0","F (x0 and y0) or !y0"]
	goallist2 = ["F !y0","F !y0 and x0","F (!y0 and x0) or !x0"]
	for i in range(len(goallist1)):
		goal1 = goallist1[i]
		goal2 = goallist2[i]
		print goal1
		print goal2
		translateAll(var1,var2,goal1,goal2)

def testcase2_2():

	var1 = ["x0"]
	var2 = ["y0"]
	goallist1 = ["G x0","G x0 and y0","G (x0 and y0) or !y0"]
	goallist2 = ["G !y0","G !y0 and x0","G (!y0 and x0) or !x0"]
	for i in range(len(goallist1)):
		goal1 = goallist1[i]
		goal2 = goallist2[i]
		print goal1
		print goal2
		translateAll(var1,var2,goal1,goal2)

def testcase2_3():

	var1 = ["x0"]
	var2 = ["y0"]
	goallist1 = ["x0 U y0","(x0 U y0) or (!y0 U x0)","((x0 U y0) and !y0 ) or (y0 U !x0)"]
	goallist2 = ["!x0 U !y0","(!x0 U !y0) or (y0 U x0)","((!x0 U !y0) and x0 ) or (!y0 U x0)"]
	for i in range(len(goallist1)):
		goal1 = goallist1[i]
		goal2 = goallist2[i]
		print goal1
		print goal2
		translateAll(var1,var2,goal1,goal2)

def testcase2_4():

	var1 = ["x0"]
	var2 = ["y0"]
	goallist1 = ["G F (x0 U y0)","G F (x0 U y0) and X(!y0 U x0)","G F ((x0 U y0) and !y0 ) or ( X y0 U !x0)"]
	goallist2 = ["G F (!x0 U !y0)","G F (!x0 U !y0) or X(y0 U x0)","G F ((!x0 U !y0) and x0 ) or X (!y0 U x0)"]
	for i in range(len(goallist1)):
		goal1 = goallist1[i]
		goal2 = goallist2[i]
		print goal1
		print goal2
		translateAll(var1,var2,goal1,goal2)

### Main ###
testcase1()