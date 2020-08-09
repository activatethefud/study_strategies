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
	
	data = [x for x in data if (x[1] - dt.datetime.today() + dt.timedelta(days=1)).days > 0]
	
	file_handler.close()

# Sort the data by date
data.sort(key = lambda x : x[1])


def get_times(data,coefs,coefs_sum,time = 1.0):

	assert(len(data) == len(coefs))
	return (time/coefs_sum)*coefs

def sum_times(data,_coefs):

	start = dt.datetime.today() - dt.timedelta(days=1) # Because datetime counts FULL days only
	#start = dt.datetime.today() + dt.timedelta(days=6)
	#start = dt.datetime(2020,1,3)
	end = data[-1][1]

	coefs = np.copy(_coefs)
	coefs_sum = sum(coefs)

	times_sum = np.resize([],len(data))

	for index in range(len(data)):

		if index == 0:
			multiplication_coef = (data[index][1] - dt.datetime.today()).days + 1
		else:
			multiplication_coef = (data[index][1] - data[index-1][1]).days

		times_sum = np.add(times_sum,multiplication_coef * get_times(data,coefs,coefs_sum))

		coefs_sum -= coefs[index]
		coefs[index] = 0

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
#print(solutions[::-1])

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
	
	import matplotlib.pyplot as plt
	
	today = dt.datetime.today() - dt.timedelta(days=1)
	due = data[-1][1]

	coefs_sum = sum(coefs)
	time_total = np.resize([],len(coefs))

	while (due - today).days > 0:

		for index in range(len(coefs)):

			if (data[index][1] - today).days <= 0:
				coefs_sum -= coefs[index]
				coefs[index] = 0
		
		today += dt.timedelta(days=1)
		time_total += get_times(data,coefs,coefs_sum,time)
	
	plt.bar(range(len(time_total)),time_total)
	plt.show()
	

def print_plan(data,time):

	for index in range(len(data)):

		print(data[index][0] + ": " + str(time[index]) + " " + str((data[index][1] - dt.datetime.today()).days + 1))

# Main

time = int(eval(input("Time: ")))

best_solution = solutions[0][0]

# Simulate and plot total times
#simulate(data,best_solution,pomodoro(time))
#sys.exit(0)

if len(sys.argv) > 2 and sys.argv[2] == "-p":
	print_plan(data,get_times(data,best_solution,sum(best_solution),pomodoro(time)))
else:
	print_plan(data,get_times(data,best_solution,sum(best_solution),time))
