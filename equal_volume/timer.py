from time import sleep
import subprocess
import sys

second = 1
minute = 60 * second
step = 1 * second

# POMODORO

p = 40
s = 7
l = 25

since_pomodoro = 0
pomodoro_counter = 0
POMODORO_COUNTER_FILE = "pomodoro_counter.txt"

# Set the pomodoro counter
try:
	file_handler = open(POMODORO_COUNTER_FILE,"r")
	pomodoro_counter = int(file_handler.read())
	file_handler.close()
except:
	pass


time = int(input("Time (minutes): "))*60
title = input("Title: ")

def sleep_for(time,title):

	while time > 0:
		try:
			subprocess.run("clear")
			print(title + "\n" + "Time left: " + str(time))

			sleep(minute)
			time -= 1
		except KeyboardInterrupt:
			break
	
	return 0

def alert(msg,sound_file,detach=None):
	
	date = subprocess.run("date",text=True,capture_output=True).stdout.rstrip('\n')

	# Notification

	if(msg is not None):
		subprocess.run(["notify-send","-t","0",date,msg])

	# Sound
	if(sound_file is not None):
		if detach is None:
			subprocess.Popen(["mpv","--no-video",sound_file])
		else:
			subprocess.run(["mpv","--no-video",sound_file])


def pomodoro_count_increase(counter,filename):
	
	file_handler = open(filename,"w")
	file_handler.write(str(counter))
	file_handler.close()

def pomodoro_count_get(filename):
	
	file_handler = open(filename,"r")

	count = int(file_handler.read())
	file_handler.close()

	return count
# Main

while time > 0:
	try:
		subprocess.run("clear")
		print(title)
		print("Since last pomodoro: " + str(since_pomodoro/60))
		print("Pomodoro count: " + str(pomodoro_counter))
		print("Time left: " + str(time/60))

		if since_pomodoro != 0 and (since_pomodoro)%(p*60) == 0:
			pomodoro_count_get(POMODORO_COUNTER_FILE)
			alert("Break time","./pomodoro_alert.mp3")
			pomodoro_counter += 1
			pomodoro_count_increase(pomodoro_counter,POMODORO_COUNTER_FILE)

		sleep(second)
		time -= step
		since_pomodoro += step
	except KeyboardInterrupt:
		opt = input("Paused. Press any key to continue\n")

		if opt == "p":

			opt = input("Short or long break [s/l]?: ")

			if opt == "s":
				since_pomodoro = sleep_for(s,"Short break")
			elif opt == "l":
				since_pomodoro = sleep_for(l,"Long break")

			alert("Break over","./break_over.mp3")

alert("Done - " + title,"./done.mp3",detach = False)
