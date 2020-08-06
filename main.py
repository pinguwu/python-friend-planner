from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import datetime
import json



weekDayRef = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']
# print (currentDate)

def menu ():
	with open ('info.json') as programInfo:
		info = json.load(programInfo)

	if len (info) == 0:
		setup()

	print ("\n")
	print ("[1] Add Friend")
	print ("[2] Create a Plan")
	print ("[3] Program Setup")
	print ("[4] Exit")
	print ("----------------------------")

	selection =  int(input ("Select an option: "))

	if selection == 1:
		addFriend()
	elif selection == 2:
		createPlans()
	elif selection == 3:
		setup()
	else:
		return

def setup ():
	with open ('info.json') as programInfo:
		info = json.load(programInfo)

	username = None
	password = None
	gc = None

	username = input ("Please input your Instagram username: ")
	password = input ("Please input your Instagram password: ")
	gc = input ("Please input the name of an Instagram group chat with your local friends: ")

	full = [username, password, gc]

	with open ('info.json', 'w') as out:
		json.dump(full, out)

def addFriend ():
	with open ('friends.json') as friends:
		friendsList = json.load(friends)
	friendToAdd = {}
	friendName = input ("Please enter the name of the friend you would like to add: ")
	friendToAdd["name"] = friendName
	friendJob = {}
	jobTitle = input ("Which days does this friend work? (enter false if they don't have a job. Input days in 3 letter format, i.e. mon, thu, sat...): ")
	if jobTitle.upper() == "FALSE":
		friendJob = []
	else:
		# jobDays = input ("Which days do they work? (input three letter days seperated by spaces i.e. 'wed, thu, tue...'): ")
		jobDaysList = jobTitle.split(' ')
		friendJob = jobDaysList

	friendToAdd["work"] = friendJob

	instagramUsername = input("Friends instagram username? ")

	friendToAdd["username"] = instagramUsername



	friendsList.append(friendToAdd)
	with open ('friends.json', 'w') as out:
		json.dump(friendsList, out)

	menu ()

def createPlans ():
	d = datetime.date.today()
	activity = input ("Select a location/activity: ")

	with open ('friends.json') as friends:
		friendsList = json.load(friends)


	i = 1
	for person in friendsList:
		print ("[" + str(i) + "] " + person["name"])
		i += 1
	allFriends = i
	print ("[" + str(i) + "] " + "All")

	friendSelect = input ("Select friends, seperated by spaces, or all: ")
	friendsSelected = []
	final = []
	
	if friendSelect == str(allFriends):
		# all friend stuff here
		for person in friendsList:
			final.append(person["name"])
			final.append("all")
	else:
		friendsSelected = friendSelect.split(" ")
		final = friendsSelected
		#for friend in friendsSelected:
		#	final.append(friendsList[int(friend) - 1]["name"])
		

	# print(final)


	
	while True:
		conflictWithWork = False
		date = input ("Which day? (You can set a specific date (yyyy-mm-dd) or just name a day (3 letter format) if it's this or the following week): ")
		if len(date) == 3:
			dayNum = 0
			for day in weekDayRef:
				if date.upper() == day:
					break
				dayNum += 1
			while d.weekday() != dayNum:
				d += datetime.timedelta(1)
			print (str(d))
		else:
			futureDate = []
			try:
				try:
					futureDate = date.split("-")
					d = datetime.datetime(futureDate)
				except:
					futureDate = date.split("/")
					d = datetime.datetime(futureDate)
			except:
				print("Bad date format!")


		for friend in friendsList:
			for jobDay in friend["work"]:
				if jobDay.upper() == weekDayRef[d.weekday()]:
					conflictWithWork = True
					print(jobDay + " == " + weekDayRef[d.weekday()])
					break
		if (conflictWithWork == True):
			print ("Day conflicts with a friend's work!")
			print ("This message will also appear if you didn't actually select a friend who has a job. It's being worked on.")
		else:
			print ("Date set!")
			dayTime = input ("What time? ")
			break




	print ("Does this message look good? -\n")
	subMessage = "BIG CHUNGUS ALERT: Listen up assholes, we should definitely {} on {} - {}. Like this message if you're coming."
	print(subMessage.format(activity, str(weekDayRef[d.weekday()]), str(d), dayTime))
	tf = input("[y/n]: ")
	msg = ""
	if tf == 'y':
		if "all" not in final:
			sendPlans(final, d, dayTime, activity, final)
		else:
			sendPlans(d, dayTime, activity)
	elif tf == 'n':
		msg = input ("input the message you would like to send instead: ")
		if "all" not in final:
			sendPlans(d, dayTime, activity, msg, final)
		else:
			sendPlans(d, dayTime, activity, msg)



def sendPlans (date, activityTime, activity, message="BIG CHUNGUS ALERT: Listen up assholes, we should definitely {} on {} - {}, at {}. Like this message if you're coming.", people=[]):
	with open ('friends.json') as friends:
		friendsList = json.load(friends)
	with open ('info.json') as programInfo:
		info = json.load(programInfo)


	driver = webdriver.Chrome("/home/paris/Downloads/chromedriver")
	driver.get("https://www.instagram.com/")

	time.sleep(2)

	username_input = driver.find_element_by_css_selector("input[name='username']")
	password_input = driver.find_element_by_css_selector("input[name='password']")

	username_input.send_keys(info[0])
	password_input.send_keys(info[1])

	login_button = driver.find_element_by_xpath("//button[@type='submit']")
	login_button.click()

	time.sleep(3.5)

	dm_button = driver.find_element_by_class_name("xWeGp")
	dm_button.click()

	time.sleep(1)

	notnow_button = driver.find_element_by_class_name("HoLwm")
	notnow_button.click()

	sendItTo = []
	# print(people)
	if people == []:
		time.sleep(1)
		gc = driver.find_element_by_xpath("//div[text()='" + info[2] + "']")
		gc.click()
		text = driver.find_element_by_class_name("focus-visible")
		if message == "BIG CHUNGUS ALERT: Listen up assholes, we should definitely {} on {} - {}, at {}. Like this message if you're coming.":
			text.send_keys(message.format(activity, str(weekDayRef[date.weekday()]), str(date), activityTime))
		else:
			text.send_keys(message)

		send = driver.find_element_by_xpath("//button[text()='Send']")
		send.click()
	else:
		
		for person in people:
			sendItTo.append(friendsList[int(person) - 1]["username"])

	personToSend = 0
	
	while personToSend < len(sendItTo):
		time.sleep(1)
		
		person = driver.find_element_by_xpath("//div[text()='" + sendItTo[personToSend] + "']")
		person.click()


		time.sleep(1)
		text = driver.find_element_by_class_name("focus-visible")
		
		if message == "BIG CHUNGUS ALERT: Listen up assholes, we should definitely {} on {} - {}, at {}. Like this message if you're coming.":
			text.send_keys(message.format(activity, str(weekDayRef[date.weekday()]), str(date), activityTime))
		else:
			text.send_keys(message)

		time.sleep(1.25)

		send = driver.find_element_by_xpath("//button[text()='Send']")
		send.click()

		time.sleep(0.5)

		if personToSend == len(sendItTo):
			break
		else:
			personToSend += 1

	driver.close()

	menu ()

#addFriend()
menu ()
# print ("Welcome to Automated Friend Planning Software!\n")
# print ("Select an option: \n")