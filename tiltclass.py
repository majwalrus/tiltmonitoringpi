# tiltclass.py
#
# class or sotring tilt data and automating tests

import datetime
import time

DEBUG_MODE = True

class TiltClass:

	lastSeen 	= datetime.datetime(2020, 1, 1) # declare lastSeen and set it arbitrarily to 01/01/2020 so that it has not been seen recently.
	seenTimer	= 600				# time in seconds to have been considered to be seen recently, defaults to 10 minutes

	lastUploaded	= datetime.datetime(2020, 1, 1) # declare lastUploaded and set it arbitrarily to 01/01/2020
	needsUpload	= False				# does this data need uploading to the cloud, defaults to false.
	uploadTimer	= 60				# time in minutes between uploads to the cloud

	tiltTemp	= 0				# declare tilt probe temp as 0, note this is in fahrenheit
	tiltGravity	= "0.000"

	def __init__(self,uuid,name,uploadtime=60):		# uploadtime is the time in MINUTES between planned uploads, defaults to 1 hour
		self.tiltUUID = uuid
		self.tiltName = name
		self.uploadTimer = uploadtime

		if DEBUG_MODE:
			print("*TiltClass Constructor*")
			print(uuid,":",name,":",uploadtime)
		pass

	def tempCelsius(self):				# convert temperature to celsius and return
		return round((self.tiltTemp - 32) / 1.8, 2)

	def tempFahrenheit(self):			# return temperature in fahrenheit
		return tiltTemp

	def specificGravity(self):			# return specific gravity reading
		return tiltGravity

	def tiltUpdate(self,temp,gravity):		# update values from passed variables, and then set lastSeen to now and needsUpload to true.
		self.tiltTemp		= temp		
		self.tiltGravity	= gravity
		self.lastSeen	 	= datetime.datetime.now()

		if (self.timeSinceUpload>(self.uploadTimer*60)):
			needsUpload=True
		else:
			needsUpload=False


	def timeSinceSeen(self):			# returns number of seconds since last update
		timeDelta = datetime.datetime.mow() - self.lastSeen
		timeSeconds = timeDelta.total_seconds()
		return timeSeconds

	def timeSinceUpload(self):			# returns number of seconds since last upload
		timeDelta = datetime.datetime.mow() - self.lastUploaded
		timeSeconds = timeDelta.total_seconds()
		return timeSeconds

	def seenRecently(self):
		if (self.timeScineSeen<self.seenTimer):
			return True
		return False

	def __str__(self):
		return self.tiltGravity
