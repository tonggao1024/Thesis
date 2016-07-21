### MAIN ###
from sourcecode import *

# Open user input file
print("----------------------------------------------")
print(str(time.time()) + ":parsing user input file...")
print("----------------------------------------------")

fo = open("input.ibg", "r")
content = fo.read().splitlines() # content in list

# Variables
singlerun = True

# Parse variables and goals
for line in content:
	if "Player1" in line:
		var1 = line.replace("Player1:", "").lstrip().split(";") # vars for player1
	elif "Player2" in line:
		var2 = line.replace("Player2:", "").lstrip().split(";") # vars for player2
	elif "Goal1" in line:
		goal1 = line.replace("Goal1:", "").lstrip() # goal for player1
	elif "Goal2" in line:
		goal2 = line.replace("Goal2:", "").lstrip() # goal for player2
	elif "Explore" in line:
		if "ALL" in line: singlerun = True
		elif "WHICH" in line: singlerun = False

# translate to .ispl file and run MCMAS
if singlerun:
	translateAll(var1,var2,goal1,goal2)
else:
	translateEach(var1,var2,goal1,goal2)