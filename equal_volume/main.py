import numpy as np
import datetime as dt
import sys
import math

assert(len(sys.argv) >= 2)

INPUT_FILE = sys.argv[1]
TUNING = 7

data = []
solutions = []

def perms(arr,index):

	if len(arr) == index:
		solutions.append(tuple([
			np.copy(arr),
			solution_rating(sum_times(data,arr))
		]))
		return True

	for i in range(TUNING):

		arr[index] = i+1
		perms(arr,index+1)


with open(INPUT_FILE,"r") as file_handler:

	for line in file_handler.readlines():
		
		if line[0] == '#':
			continue

		line = line.rstrip('\n').split(",")

		data.append(tuple([
			line[0],
			dt.datetime.strptime(line[1],"%d/%m/%Y")
		]))
	
	data = [x for x in data if (x[1] - dt.datetime.today()).days > 0]
	
	file_handler.close()

# Sort the data by date
data.sort(key = lambda x : x[1])


def get_times(data,coefs):
	assert(len(data) == len(coefs))

	time = 1

	coefs_sum = sum(coefs)
	times = []
	
	for index in range(len(coefs)):
		times.append(coefs[index]*1.0/coefs_sum)
	
	return times

def sum_times(data,_coefs):

	start = dt.datetime.today() - dt.timedelta(days=1) # Because datetime counts FULL days only
	#start = dt.datetime.today() + dt.timedelta(days=6)
	#start = dt.datetime(2020,1,3)
	end = data[-1][1]

	coefs = np.copy(_coefs)

	times_sum = np.resize([],len(data))

	while (end-start).days > 0:

		for index in range(len(coefs)):
	
			if (data[index][1] - start).days <= 0:
				coefs[index] = 0
	
		times = get_times(data,coefs)
		start += dt.timedelta(days=1)

		times_sum = np.add(times_sum,times)
	
	return times_sum

def solution_rating(total_times):
	
	avg = sum(total_times)*1.0/len(total_times)

	rating = 0

	for time in total_times:
		rating += abs(time-avg)
	
	return rating

print("Working...")
arr = np.resize([],len(data))
perms(arr,0)

solutions.sort(key = lambda x : x[1])
print(solutions[::-1])

def gen_optimal(data,coefs,time):

	today = dt.datetime.today() - dt.timedelta(days=1) # Because datetime counts FULL days only
	#today = dt.datetime.today() + dt.timedelta(days=6)

	#for index in range(len(coefs)):

	#	if (data[index][1] - today).days <= 0:
	#		coefs[index] = 0

	coefs_sum = sum(coefs)
	coefs *= time*1.0/coefs_sum

	global optimal_coefs
	optimal_coefs = coefs

	return coefs

def pomodoro(time):

	# POMODORO
	
	p = 25
	s = 7
	l = 25

	time_x = 0

	def expression(x,p,l,s,n):
		
		pc = math.floor(x/p)

		return x + (pc - math.floor(pc/4))*s + math.floor(pc/4)*l + (n-1)*s
	
	while expression(time_x,p,l,s,len(data)) <= time:
		time_x += 1

	return time_x - 1

	
def simulate(data,coefs,time):
	
	global today
	due = data[-1][1]

	while (due - today).days > 0:

		for index in range(len(coefs)):

			if (data[index][1] - today).days <= 0:
				coefs[index] = 0
		
		print(get_times(data,coefs))

		today += dt.timedelta(days=1)
	

def print_plan(data,time):

	for index in range(len(data)):

		print(data[index][0] + ": " + str(time[index]) + " " + str((data[index][1] - dt.datetime.today()).days + 1))

# Main

time = int(eval(input("Time: ")))

best_solution = solutions[0][0]

if len(sys.argv) > 2 and sys.argv[2] == "-p":
	print_plan(data,gen_optimal(data,best_solution,pomodoro(time)))
else:
	print_plan(data,gen_optimal(data,best_solution,time))
