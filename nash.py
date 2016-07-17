#!/usr/bin/python
import itertools
import io
import os
import subprocess

# Helper function
def writeComment(fo,var1,var2,goal1,goal2):
	fo.write("-- Input iBG file" + "\n")
	fo.write("-- Player1: " + ", ".join(var1) + "\n")
	fo.write("-- Player2: " + ", ".join(var2) + "\n")
	fo.write("-- Goal1: " + goal1 + "\n")
	fo.write("-- Goal2: " + goal2 + "\n")
	fo.write("\n"*2)

def createEnvironment(fo):
	fo.write("Agent Environment\n")
	fo.write("  Obsvars:\n" + "    dummy : boolean;\n" + "  end Obsvars\n")
	fo.write("  Actions = {none};\n")
	fo.write("  Protocol:\n" + "    Other : {none};\n" + "  end Protocol\n")
	fo.write("  Evolution:\n" + "    dummy = true if Action=none;\n" + "  end Evolution\n")
	fo.write("end Agent\n")
	fo.write("\n"*2)

def createPlayer(fo,var,num):
	fo.write("Agent Player1\n") if num == "1" else fo.write("Agent Player2\n")

	# action list
	seqList = ["".join(seq) for seq in itertools.product("01", repeat = len(var))]
	actionList = ["ac" + seq for seq in seqList]
	
	# variables
	fo.write("  Vars:\n")
	for i in var:
		fo.write("    " + i + " : boolean;\n")
	fo.write("  end Vars\n")

	# actions
	fo.write("  Actions = {" + ", ".join(actionList) + "};\n")

	# protocals
	fo.write("  Protocol:\n")
	fo.write("    Other : {" + ", ".join(actionList) + "};\n")
	fo.write("  end Protocol\n")

	# evolution
	fo.write("  Evolution:\n")
	for i in range(len(seqList)):
		fo.write("    ")
		for j in range(len(var)):
			fo.write("(" + var[j] + " = " + str(bool(int(seqList[i][j]))).lower() + ")")
			if (j == len(var) - 1): break
			fo.write(" and ")
		fo.write(" if Action=" + actionList[i] + ";\n")
	fo.write("  end Evolution\n")

	fo.write("end Agent\n")
	fo.write("\n"*2)		

def createEvaluation(fo,var1,var2):
	fo.write("Evaluation\n")
	for item in var1:
		fo.write("  " + item + " if " + "Player1." + item + " = true;\n")
	for item in var2:
		fo.write("  " + item + " if " + "Player2." + item + " = true;\n")
	fo.write("end Evaluation\n")
	fo.write("\n"*2)

def createInitStates(fo,var1,var2):
	fo.write("InitStates\n")
	fo.write("  (Environment.dummy = true) and\n")

	for item in var1:
		fo.write("  ((Player1." + item + " = true) or (Player1." + item + " = false)) and\n")

	for i, item in enumerate(var2):
		fo.write("  ((Player2." + item + " = true) or (Player2." + item + " = false))")
		if (i == len(var2) - 1): 
			fo.write(";\n")
			break
		else:
			fo.write(" and\n")

	fo.write("end InitStates\n")
	fo.write("\n"*2)

def createFormulae(fo,goal1,goal2):
	fo.write("Formulae\n")
	# Environment
	fo.write("  <<strategy_env>> (Environment,strategy_env) (\n")

	# LTL SAT
	fo.write("    -- LTL SAT\n")
	fo.write("    ( <<strategy_p1>> (Player1, strategy_p1) <<strategy_p2>> (Player2, strategy_p2) ")
	fo.write("( (" + goal1 + ") and (" + goal2 + ") ) ) or\n")

	# CTL SYN
	fo.write("    -- CTL SYN\n")
	fo.write("    ( ( <<strategy_p1>> (Player1, strategy_p1) [[strategy_p2]] (Player2, strategy_p2) ")
	fo.write("(" + goal1 + ") )" )
	fo.write(" or\n")
	fo.write("      ( <<strategy_p2>> (Player2, strategy_p2) [[strategy_p1]] (Player1, strategy_p1) ")
	fo.write("(" + goal2 + ") ) ) or\n")

	# CTL SYN
	fo.write("    -- CTL SYN\n")
	fo.write("    ( ( <<strategy_p1>> (Player1, strategy_p1) [[strategy_p2]] (Player2, strategy_p2) ")
	fo.write("(!(" + goal2 + ") ) )" )	
	fo.write(" and\n")
	fo.write("      ( <<strategy_p2>> (Player2, strategy_p2) [[strategy_p1]] (Player1, strategy_p1) ")
	fo.write("(!(" + goal2 + ") ) ) ) or\n")	

	# CTL* SYN
	fo.write("    -- CTL* SYN\n")
	fo.write("    ( ( <<strategy_p1>> (Player1, strategy_p1) ")
	fo.write("( [[strategy_p2]] (Player2, strategy_p2) " +  "(!(" + goal2 + ") )")
	fo.write(" and ")
	fo.write("<<strategy_p2>> (Player2, strategy_p2) " + "(" + goal1 + ") ) )")
	fo.write(" or\n")
	fo.write("      ( <<strategy_p2>> (Player2, strategy_p2) ")
	fo.write("( [[strategy_p1]] (Player1, strategy_p1) " +  "(!(" + goal1 + ") )")
	fo.write(" and ")
	fo.write("<<strategy_p1>> (Player1, strategy_p1) " + "(" + goal2 + ") ) ) )\n")

	fo.write("  );\n")

	

	fo.write("end Formulae\n")


### MAIN ###

# Open user input file
fo = open("input.ibg", "r")
content = fo.read().splitlines() # content in list

# Parse variables and goals
for line in content:
	if "Player1" in line:
		var1 = line.replace("Player1:", "").lstrip().split(";") # vars for player1
	elif "Player2" in line:
		var2 = line.replace("Player2:", "").lstrip().split(";") # vars for player2
	elif "Goal1" in line:
		goal1 = line.replace("Goal1:", "").lstrip()
	elif "Goal2" in line:
		goal2 = line.replace("Goal2:", "").lstrip()
print var1
print var2
print goal1
print goal2


# Translate to .ispl file
fo = open("input.ispl", "w")
writeComment(fo,var1,var2,goal1,goal2)
createEnvironment(fo)
createPlayer(fo,var1,"1")
createPlayer(fo,var2,"2")
createEvaluation(fo,var1,var2)
createInitStates(fo,var1,var2)
createFormulae(fo,goal1,goal2)
fo.close()

# Call mcmas
os.chdir("../../")
#os.system("./mcmas examples/iBG/input.ispl ")
output = os.popen("./mcmas examples/iBG/input.ispl").read()

# Parse output
print output
print "-------------------------------"

if "is TRUE in the model" in output:
	print "The game has a Nash Equilibrium"
elif "is FALSE in the model" in output:
	print "The game has a Nash Equilibrium"
else:
	print "Error exists, please check your input"

print "-------------------------------"
