import numpy as np
import datetime as dt
import sys
import matplotlib as plt

assert(len(sys.argv) == 2)


INPUT_FILE = sys.argv[1]
TUNING = 5

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
	
	file_handler.close()


def get_times(data,coefs):
	assert(len(data) == len(coefs))

	time = 1

	coefs_sum = sum(coefs)
	times = []
	
	for index in range(len(coefs)):
		times.append(coefs[index]*1.0/coefs_sum)
	
	return times

def sum_times(data,_coefs):

	#start = dt.datetime.today()
	start = dt.datetime.today() + dt.timedelta(days=6)
	#start = dt.datetime(2020,1,3)
	end = data[len(data)-1][1]

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

arr = np.resize([],len(data))
perms(arr,0)

solutions.sort(key = lambda x : x[1])
print(solutions)

def gen_optimal(data,coefs,time):

	today = dt.datetime.today()

	for index in range(len(coefs)):

		if (data[index][1] - today).days <= 0:
			coefs[index] = 0

	coefs_sum = sum(coefs)
	coefs *= time*1.0/coefs_sum

	for index in range(len(coefs)):

		print(data[index][0] + " " + str(coefs[index]))

gen_optimal(data,solutions[0][0],int(eval(input("Time: "))))
