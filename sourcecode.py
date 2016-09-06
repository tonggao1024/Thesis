#!/usr/bin/python
import itertools
import io
import os
import subprocess
import time
import re

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

def createFormulae_LTLSAT(fo,goal1,goal2):
	fo.write("Formulae\n")

	fo.write("  -- LTL SAT\n")
	fo.write("  <<strategy_env>> (Environment,strategy_env) (\n")
	fo.write("    ( <<strategy_p1>> (Player1, strategy_p1) <<strategy_p2>> (Player2, strategy_p2) ")
	fo.write(" X " + "( (" + goal1 + ") and (" + goal2 + ") ) )\n")
	fo.write("  );\n")

	fo.write("end Formulae\n")

def createFormulae_LTLSYN_OR1(fo,goal1,goal2):
	fo.write("Formulae\n")

	fo.write("  -- LTL SYN (OR1)\n")
	fo.write("  <<strategy_env>> (Environment,strategy_env) (\n")
	fo.write("    ( <<strategy_p1>> (Player1, strategy_p1) [[strategy_p2]] (Player2, strategy_p2) ")
	fo.write(" X " + "(" + goal1 + ") )\n" )
	fo.write("  );\n")

	fo.write("end Formulae\n")

def createFormulae_LTLSYN_OR2(fo,goal1,goal2):
	fo.write("Formulae\n")

	fo.write("  -- LTL SYN (OR2)\n")
	fo.write("  <<strategy_env>> (Environment,strategy_env) (\n")
	fo.write("      ( <<strategy_p2>> (Player2, strategy_p2) [[strategy_p1]] (Player1, strategy_p1) ")
	fo.write(" X " + "(" + goal2 + ") )\n")
	fo.write("  );\n")

	fo.write("end Formulae\n")

def createFormulae_LTLSYN_AND(fo,goal1,goal2):
	fo.write("Formulae\n")

	fo.write("  -- LTL SYN (AND)\n")
	fo.write("  <<strategy_env>> (Environment,strategy_env) (\n")
	fo.write("    ( <<strategy_p1>> (Player1, strategy_p1) [[strategy_p2]] (Player2, strategy_p2) ")
	fo.write(" X " + "(!(" + goal2 + ") ) )\n" )	
	fo.write("  );\n")

	fo.write("  <<strategy_env>> (Environment,strategy_env) (\n")
	fo.write("      ( <<strategy_p2>> (Player2, strategy_p2) [[strategy_p1]] (Player1, strategy_p1) ")
	fo.write(" X " + "(!(" + goal1 + ") ) )\n")
	fo.write("  );\n")

	fo.write("end Formulae\n")

def createFormulae_CTLStarSYN_OR1(fo,goal1,goal2):
	fo.write("Formulae\n")

	fo.write("  -- CTL* SYN (OR1)\n")
	fo.write("  <<strategy_env>> (Environment,strategy_env) (\n")
	fo.write("    ( <<strategy_p1>> (Player1, strategy_p1) ")
	fo.write("( [[strategy_p2]] (Player2, strategy_p2) " + " X " +  "(!(" + goal2 + ") )")
	fo.write(" and ")
	fo.write("<<strategy_p2>> (Player2, strategy_p2) " + " X " + "(" + goal1 + ") ) )\n")
	fo.write("  );\n")

	fo.write("end Formulae\n")

def createFormulae_CTLStarSYN_OR2(fo,goal1,goal2):
	fo.write("Formulae\n")

	fo.write("  -- CTL* SYN (OR2)\n")
	fo.write("  <<strategy_env>> (Environment,strategy_env) (\n")
	fo.write("      ( <<strategy_p2>> (Player2, strategy_p2) ")
	fo.write("( [[strategy_p1]] (Player1, strategy_p1) " + " X " +  "(!(" + goal1 + ") )")
	fo.write(" and ")
	fo.write("<<strategy_p1>> (Player1, strategy_p1) " + " X " + "(" + goal2 + ") ) )\n")
	fo.write("  );\n")

	fo.write("end Formulae\n")

def createFormulae(fo,goal1,goal2):
	fo.write("Formulae\n")

	# LTL SAT
	fo.write("  -- LTL SAT\n")
	fo.write("  <<strategy_env>> (Environment,strategy_env) (\n")
	fo.write("    ( <<strategy_p1>> (Player1, strategy_p1) <<strategy_p2>> (Player2, strategy_p2) ")
	fo.write(" X " + "( (" + goal1 + ") and (" + goal2 + ") ) )\n")
	fo.write("  );\n")
	fo.write("\n")

	# LTL SYN1
	fo.write("  -- LTL SYN\n")
	fo.write("  <<strategy_env>> (Environment,strategy_env) (\n")
	fo.write("    ( <<strategy_p1>> (Player1, strategy_p1) [[strategy_p2]] (Player2, strategy_p2) ")
	fo.write(" X " + "(" + goal1 + ") )\n" )
	fo.write("  );\n")

	fo.write("  <<strategy_env>> (Environment,strategy_env) (\n")
	fo.write("      ( <<strategy_p2>> (Player2, strategy_p2) [[strategy_p1]] (Player1, strategy_p1) ")
	fo.write(" X " + "(" + goal2 + ") )\n")
	fo.write("  );\n")
	fo.write("\n")

	# LTL SYN2
	fo.write("  -- LTL SYN\n")
	fo.write("  <<strategy_env>> (Environment,strategy_env) (\n")
	fo.write("    ( <<strategy_p1>> (Player1, strategy_p1) [[strategy_p2]] (Player2, strategy_p2) ")
	fo.write(" X " + "(!(" + goal2 + ") ) )\n" )	
	fo.write("  );\n")

	fo.write("  <<strategy_env>> (Environment,strategy_env) (\n")
	fo.write("      ( <<strategy_p2>> (Player2, strategy_p2) [[strategy_p1]] (Player1, strategy_p1) ")
	fo.write(" X " + "(!(" + goal1 + ") ) )\n")
	fo.write("  );\n")
	fo.write("\n")

	# CTL* SYN
	fo.write("  -- CTL* SYN\n")
	fo.write("  <<strategy_env>> (Environment,strategy_env) (\n")
	fo.write("    ( <<strategy_p1>> (Player1, strategy_p1) ")
	fo.write("( [[strategy_p2]] (Player2, strategy_p2) " + " X " +  "(!(" + goal2 + ") )")
	fo.write(" and ")
	fo.write("<<strategy_p2>> (Player2, strategy_p2) " + " X " + "(" + goal1 + ") ) )\n")
	fo.write("  );\n")

	fo.write("  <<strategy_env>> (Environment,strategy_env) (\n")
	fo.write("      ( <<strategy_p2>> (Player2, strategy_p2) ")
	fo.write("( [[strategy_p1]] (Player1, strategy_p1) " +  " X " + "(!(" + goal1 + ") )")
	fo.write(" and ")
	fo.write("<<strategy_p1>> (Player1, strategy_p1) " + " X " + "(" + goal2 + ") ) )\n")
	fo.write("  );\n")
	fo.write("\n")

	fo.write("end Formulae\n")

def createFormulaeSL(fo,goal1,goal2):
	fo.write("Formulae\n")

	fo.write("  <<strategy_env>> (Environment,strategy_env) (\n")
	fo.write("   <<strategy_p1>> <<strategy_p2>> (Player1, strategy_p1) (Player2, strategy_p2) ")
	fo.write("( (" + goal1 + ") or [[alt_strategy_p1]] (Player1,alt_strategy_p1)" + " !(" + goal1 +") )")
	fo.write(" and ")
	fo.write("( (" + goal2 + ") or [[alt_strategy_p2]] (Player2,alt_strategy_p2)" + " !(" + goal2 +") )")
	fo.write("  );\n")

	fo.write("end Formulae\n")

def runMCMAS(filename):
	start_time = time.time()
	print("%s:running MCMAS..." % start_time)
	print("----------------------------------------------")

	# Call mcmas
	os.chdir("../../") # change directory
	output = os.popen("./mcmas examples/iBG/" + filename).read()

	# Set flag
	done = False

	# track excution time
	print output
	print("----------------------------------------------")
	print("%s:finishing MCMAS..." % time.time())
	print("----------------------------------------------")
	end_time = time.time() - start_time
	print("Execution Time:%s seconds " % end_time)
	print("----------------------------------------------")

	f = open('examples/iBG/excutiontime.ibg','a+')
	f.write("Execution Time:%s seconds\n" % end_time)
	f.close()

	#identidy filename
	if filename == "input.ispl":
		# Parse output
		result1 = re.search("Formula number 1(.*)model", output)
		result2 = re.search("Formula number 2(.*)model", output)
		result3 = re.search("Formula number 3(.*)model", output)
		result4 = re.search("Formula number 4(.*)model", output)
		result5 = re.search("Formula number 5(.*)model", output)
		result6 = re.search("Formula number 6(.*)model", output)
		result7 = re.search("Formula number 7(.*)model", output)

		if (("is TRUE" in result1.group(1)) or ("is TRUE" in result2.group(1)) or 
		   ("is TRUE" in result3.group(1)) or ("is TRUE" in result6.group(1)) or 
		   ("is TRUE" in result7.group(1))):
			# raise flag
			done = True
			# print result
			print "The game has a Nash Equilibrium "
		elif ("is TRUE" in result4.group(1)) and ("is TRUE" in result5.group(1)):
			# raise flag
			done = True
			# print result
			print "The game has a Nash Equilibrium "
		else:
			print "The game doesn't have a Nash Equilibrium "
	elif filename == "input_LTLSAT.ispl":
		if "is TRUE in the model" in output:
			# raise flag
			done = True
			# print result
			print "The game has a Nash Equilibrium "
			print "LTL SAT is satisfied"
	elif filename == "input_LTLSYN_OR1.ispl":
		if "is TRUE in the model" in output:
			# raise flag
			done = True
			# print result
			print "The game has a Nash Equilibrium "
			print "LTL SYN(OR1) is satisfied"
	elif filename == "input_LTLSYN_OR2.ispl":
		if "is TRUE in the model" in output:
			# raise flag
			done = True
			# print result
			print "The game has a Nash Equilibrium "
			print "LTL SYN(OR2) is satisfied"
	elif filename == "input_LTLSYN_AND.ispl":
		if "is FALSE in the model" not in output:
			# raise flag
			done = True
			# print result
			print "The game has a Nash Equilibrium "
			print "LTL SYN(AND) is satisfied"
	elif filename == "input_CTLSTAR_OR1.ispl":
		if "is TRUE in the model" in output:
			# raise flag
			done = True
			# print result
			print "The game has a Nash Equilibrium "
			print "CTL* SYN(OR1) is satisfied"
	elif filename == "input_CTLSTAR_OR2.ispl":
		if "is TRUE in the model" in output:
			# raise flag
			done = True
			# print result
			print "The game has a Nash Equilibrium "
			print "CTL* SYN(OR2) is satisfied"
		else:
			print "The game doesn't have a Nash Equilibrium "

	print("----------------------------------------------")

	os.chdir("examples/iBG/") # change directory back

	return done 

def translateAll(var1,var2,goal1,goal2):
	print(str(time.time()) + ":generating .ispl file...")
	print("----------------------------------------------")

	# Translate to .ispl file
	filename = "input.ispl"
	fo = open(filename, "w")
	writeComment(fo,var1,var2,goal1,goal2)
	createEnvironment(fo)
	createPlayer(fo,var1,"1")
	createPlayer(fo,var2,"2")
	createEvaluation(fo,var1,var2)
	createInitStates(fo,var1,var2)
	createFormulae(fo,goal1,goal2)
	fo.close()

	# Run MCMAS
	runMCMAS(filename)

def translateSL(var1,var2,goal1,goal2):
	print(str(time.time()) + ":generating .ispl file...")
	print("----------------------------------------------")

	# Translate to .ispl file
	filename = "input.ispl"
	fo = open(filename, "w")
	writeComment(fo,var1,var2,goal1,goal2)
	createEnvironment(fo)
	createPlayer(fo,var1,"1")
	createPlayer(fo,var2,"2")
	createEvaluation(fo,var1,var2)
	createInitStates(fo,var1,var2)
	createFormulaeSL(fo,goal1,goal2)
	fo.close()

	# Run MCMAS
	runMCMAS(filename)

def translateEach(var1,var2,goal1,goal2):
	# Translate to 4 .ispl file and run one by one

	### LTL SAT
	filename = "input_LTLSAT.ispl"
	fo = open(filename, "w")
	writeComment(fo,var1,var2,goal1,goal2)
	createEnvironment(fo)
	createPlayer(fo,var1,"1")
	createPlayer(fo,var2,"2")
	createEvaluation(fo,var1,var2)
	createInitStates(fo,var1,var2)
	createFormulae_LTLSAT(fo,goal1,goal2)
	fo.close()

	# Run MCMAS
	done = runMCMAS(filename)
	if done: return

	### LTL SYN (OR1)
	filename = "input_LTLSYN_OR1.ispl"
	fo = open(filename, "w")
	writeComment(fo,var1,var2,goal1,goal2)
	createEnvironment(fo)
	createPlayer(fo,var1,"1")
	createPlayer(fo,var2,"2")
	createEvaluation(fo,var1,var2)
	createInitStates(fo,var1,var2)
	createFormulae_LTLSYN_OR1(fo,goal1,goal2)
	fo.close()

	# Run MCMAS
	done = runMCMAS(filename)
	if done: return

	### LTL SYN (OR2)
	filename = "input_LTLSYN_OR2.ispl"
	fo = open(filename, "w")
	writeComment(fo,var1,var2,goal1,goal2)
	createEnvironment(fo)
	createPlayer(fo,var1,"1")
	createPlayer(fo,var2,"2")
	createEvaluation(fo,var1,var2)
	createInitStates(fo,var1,var2)
	createFormulae_LTLSYN_OR2(fo,goal1,goal2)
	fo.close()

	# Run MCMAS
	done = runMCMAS(filename)
	if done: return

	### LTL SYN (AND)
	filename = "input_LTLSYN_AND.ispl"
	fo = open(filename, "w")
	writeComment(fo,var1,var2,goal1,goal2)
	createEnvironment(fo)
	createPlayer(fo,var1,"1")
	createPlayer(fo,var2,"2")
	createEvaluation(fo,var1,var2)
	createInitStates(fo,var1,var2)
	createFormulae_LTLSYN_AND(fo,goal1,goal2)
	fo.close()

	# Run MCMAS
	done = runMCMAS(filename)
	if done: return

	# CTL* SYN (OR1)
	filename = "input_CTLSTAR_OR1.ispl"
	fo = open(filename, "w")
	writeComment(fo,var1,var2,goal1,goal2)
	createEnvironment(fo)
	createPlayer(fo,var1,"1")
	createPlayer(fo,var2,"2")
	createEvaluation(fo,var1,var2)
	createInitStates(fo,var1,var2)
	createFormulae_CTLStarSYN_OR1(fo,goal1,goal2)
	fo.close()

	# Run MCMAS
	done = runMCMAS(filename)
	if done: return

	# CTL* SYN (OR2)
	filename = "input_CTLSTAR_OR2.ispl"
	fo = open(filename, "w")
	writeComment(fo,var1,var2,goal1,goal2)
	createEnvironment(fo)
	createPlayer(fo,var1,"1")
	createPlayer(fo,var2,"2")
	createEvaluation(fo,var1,var2)
	createInitStates(fo,var1,var2)
	createFormulae_CTLStarSYN_OR2(fo,goal1,goal2)
	fo.close()

	# Run MCMAS
	done = runMCMAS(filename)
	if done: return