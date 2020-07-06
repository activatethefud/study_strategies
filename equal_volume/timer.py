from time import sleep
import subprocess

second = 1
minute = 60 * second

# POMODORO

p = 25
s = 7
l = 25

time = int(input("Time (minutes): "))*60
title = input("Title: ")

def sleep_for(time,title):

	try:
		while time > 0:
			subprocess.run("clear")
			print(title + "\n" + "Time left: " + str(time))

			sleep(minute)
			time -= 1
	except KeyboardInterrupt:
		return 0


while time > 0:
	try:
		subprocess.run("clear")
		print(title + "\n" + "Time left: " + str(time/60))

		sleep(second)
		time -= 1
	except KeyboardInterrupt:
		opt = input("Paused. Press any key to continue\n")

		if opt == "p":

			opt = input("Short or long break [s/l]?: ")

			if opt == "s":
				sleep_for(s,"Short break")
			elif opt == "l":
				sleep_for(l,"Long break")
