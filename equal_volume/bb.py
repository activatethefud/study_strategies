import numpy as np
import datetime as dt
import sys
import math
import copy

assert(len(sys.argv) >= 2)

INPUT_FILE = sys.argv[1]

data = []
solutions = []

global_min = 10e10

today = dt.date.today()
#today = dt.datetime.strptime(input("Date: "),"%d/%m/%Y").date()

TUNING = 1000

def perms(arr, index, TUNING):

    if index == len(arr):
            return True

    for i in range(TUNING,0,-1):

        global global_min

        arr[index] = i
        rating = solution_rating(sum_times(data, arr))

        if rating <= global_min:

            global_min = rating
            solutions.append(tuple([
                np.copy(arr),
                solution_rating(sum_times(data, arr))
            ]))

            perms(arr, index+1, TUNING)


with open(INPUT_FILE, "r") as file_handler:

    for line in file_handler.readlines():

        if line[0] == '#' or line[0] == '\n':
            continue

        line = line.rstrip('\n').split(",")

        data.append(tuple([
            line[0],
            dt.datetime.strptime(line[1], "%d/%m/%Y").date()
        ]))

    data = [x for x in data if (x[1] - today).days > 0]

    file_handler.close()

# Sort the data by date
data.sort(key=lambda x: x[1])


def get_times(data, coefs, coefs_sum, time=1.0):

    assert(len(data) == len(coefs))
    return (time/coefs_sum)*coefs


def sum_times(data, _coefs):

    end = data[-1][1]

    coefs = np.copy(_coefs)
    coefs_sum = sum(coefs)

    times_sum = np.resize([], len(data))

    for index in range(len(data)):

        if index == 0:
            multiplication_coef = (data[index][1] - today).days + 1
        else:
            multiplication_coef = (data[index][1] - data[index-1][1]).days

        times_sum = np.add(times_sum, multiplication_coef *
                           get_times(data, coefs, coefs_sum))

        coefs_sum -= coefs[index]
        coefs[index] = 0

    return times_sum


#def solution_rating2(total_times):
#
#    max_ = total_times[0]
#    min_ = total_times[0]
#
#    for i in range(len(total_times)):
#
#        max_ = max(max_, total_times[i])
#        min_ = min(min_, total_times[i])
#
#    return max_ - min_
#

def solution_rating(total_times):

    avg = sum(total_times)*1.0/len(total_times)

    rating = 0

    for time in total_times:
        rating += abs(time-avg)

    return rating


print("Working...")
arr = np.resize([], len(data))

# UPPER_LIMIT = 12**5 # ~~ 250k
UPPER_LIMIT = 5*10**5  # ~~ 500k
#TUNING = math.floor(UPPER_LIMIT ** (1.0/len(data)))

arr.fill(TUNING)

print("Tuning: " + str(TUNING))

perms(arr, 0, TUNING)

solutions.sort(key=lambda x: x[1])
#print(solutions[::-1])

def pomodoro(time):

    # POMODORO

    p = 40
    s = 7
    l = 7

    time_x = 0

    def expression(x, p, l, s, n):

        pc = math.floor(x/p)

        return x + (pc - math.floor(pc/4))*s + math.floor(pc/4)*l + (n-1)*s

    while expression(time_x, p, l, s, len(data)) <= time:
        time_x += 1

    return time_x - 1


def simulate(data, coefs, time):

    import matplotlib.pyplot as plt

    today_ = copy.copy(today)
    due = data[-1][1]

    coefs_sum = sum(coefs)
    time_total = np.resize([], len(coefs))

    while (due - today_).days > 0:

        for index in range(len(coefs)):

            if (data[index][1] - today_).days <= 0:
                coefs_sum -= coefs[index]
                coefs[index] = 0

        today_ += dt.timedelta(days=1)
        time_total += get_times(data, coefs, coefs_sum, time)

    plt.bar(range(len(time_total)), time_total)
    plt.title("Date: %s, Tuning: %d" % ((today).strftime("%d/%m/%Y"), TUNING))

    for i in range(len(time_total)):
        plt.annotate(str(time_total[i]), (i, time_total[i]))

    plt.savefig(dt.datetime.today().strftime("%s") + ".png")


def print_plan(data, time):

    for index in range(len(data)):

        print(data[index][0] + ": " + str(time[index]) +
              " " + str((data[index][1] - today).days))

# Main


print(solutions[0])
time = int(eval(input("Time: ")))

best_solution = solutions[0][0]

# Simulate and plot total times
# simulate(data,best_solution,pomodoro(time))
# sys.exit(0)

if len(sys.argv) > 2 and sys.argv[2] == "-p":
    print_plan(data, get_times(data, best_solution,
                               sum(best_solution), pomodoro(time)))
else:
    print_plan(data, get_times(data, best_solution, sum(best_solution), time))
