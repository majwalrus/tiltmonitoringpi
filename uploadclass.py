# uploadclass.py
#
# Class for handling where to send data

import pycurl
import json

UC_METHOD_BREWERSFRIEND = 1
UC_METHOD_CUSTOM = 2

UC_METHOD_DEFAULT = UC_METHOD_BREWERSFRIEND

DEBUG_MODE = True

class UploadClass:
	
	uploadCustomURL	= "http://homeserver.home/brewery/api.php?"

	uploadBrewersFriendURL = "https://log.brewersfriend.com/stream/"
	uploadBrewersFriendAPI = "none"
	errorlog = "null"
	
	gravity_unit = "G"
	temp_unit = "C"
	content_type = "custom pi application"
	

	def __init__(self,method=UC_METHOD_DEFAULT):
		self.uploadMethod=method
		pass

	def uploadBrewersFriend(self,device,temp,gravity):
		if (self.uploadBrewersFriendAPI == "none"):
			self.errorlog = "No API key set."
			if DEBUG_MODE:
				print("uploadBrewersFriend Error: ",self.errorlog)
			return False

		connect_url=self.uploadBrewersFriendURL+self.uploadBrewersFriendAPI

		headerinfo = [	'Content-Type: application/json',
				'X-API-KEY: '+self.uploadBrewersFriendAPI]
		curl_data = {	"name" : "Tilt"+device,
				"device_source" : "Tilt",
				"report_source" : "tiltmonitoring.py",
				"og" : gravity/1000,
				"temp" : temp,
				"temp_unit" : self.temp_unit,
				"gravity_unit" : self.gravity_unit}

		if DEBUG_MODE:
			print ("uploadBrewersFriend - Debug Info")
			print ("URL: ",connect_url)
			print ("Header: ",headerinfo)
			print ("List: ",curl_data)
			print ("JSONL ",json.dumps(curl_data))

		pycurl_connect = pycurl.Curl()
		pycurl_connect.setopt(pycurl.URL, connect_url)
		pycurl_connect.setopt(pycurl.HTTPHEADER, headerinfo)
		pycurl_connect.setopt(pycurl.POST,1)
		pycurl_connect.setopt(pycurl.POSTFIELDS, json.dumps(curl_data))
		pycurl_connect.setopt(pycurl.VERBOSE,1)
		pycurl_connect.perform()
		if DEBUG_MODE:
			print("pyCurl Response: %d" % pycurl_connect.getinfo(pycurl_connect.RESPONSE_CODE))
		pycurl_connect.close()

		return True
	

	def uploadCustom(self,device_source,temp,gravity):
		return True

	def setBrewersFriendAPI(self,api):
		self.uploadBrewersFriendAPI = api
		return True

	def upload(self,device_source,temp,gravity):
		if ((self.uploadMethod & UC_METHOD_BREWERSFRIEND)>0):
			if not (self.uploadBrewersFriend(device_source,temp,gravity)):
				return False
		if ((self.uploadMethod & UC_METHOD_CUSTOM)>0):
			if not (self.uploadBrewersFriend(device_source,temp,gravity)):
				return False
		return True

