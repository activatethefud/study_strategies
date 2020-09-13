import sys,subprocess
import random as rd

times = {}
quant = 20

with open("plan.txt","r") as file_handler:
	
	for line in file_handler.readlines():

		line = line.rstrip("\n")

		if line[0] == '#' or line[0] == '\n':
			continue

		tokens = line.split(":")

		subject = tokens[0]
		time = float(tokens[1].split()[0])

		if times.get(subject) is None:
			times[subject] = time

def print_remaining(times):
	
	with open("plan.txt","w") as file_handler:

		for key in times.keys():
			
			print(key + ": " + str(times[key]),file=file_handler)

while len(times.keys()) > 0:

	keys = [x for x in times.keys()]
	choice = rd.choice(keys)

	work_time = min(times[choice],quant)

	try:
		subprocess.run(["python","timer.py",str(work_time),choice])
	except KeyboardInterrupt:
		print_remaining(times)
		sys.exit(0)

	times[choice] -= work_time
	
	print(choice + " " + str(times[choice]))

	if times[choice] == 0:
		del times[choice]

