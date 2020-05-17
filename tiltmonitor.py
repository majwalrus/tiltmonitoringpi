import sys
sys.path.insert(1,"./lib")
import epd2in13_V2 as epdscreen

from PIL import Image, ImageDraw, ImageFont
import time
import datetime

import bluetooth._bluetooth as bluez

import blescan
import tiltclass
import threading


epd = epdscreen.EPD()

global_UpdateImage = Image.new('1',(epdscreen.EPD_HEIGHT, epdscreen.EPD_WIDTH) ,255)

temp_gravRead = 1.000

#
# Initialise Tilt bluetooth uuids and associated classes
#

TILTS = {
	'a495bb10c5b14b44b5121370f02d74de': 'Red',
	'a495bb20c5b14b44b5121370f02d74de': 'Green',
	'a495bb30c5b14b44b5121370f02d74de': 'Black',
	'a495bb40c5b14b44b5121370f02d74de': 'Purple',
	'a495bb50c5b14b44b5121370f02d74de': 'Orange',
	'a495bb60c5b14b44b5121370f02d74de': 'Blue',
	'a495bb70c5b14b44b5121370f02d74de': 'Yellow',
	'a495bb80c5b14b44b5121370f02d74de': 'Pink',
}

glob_tilts = []

for key in TILTS:
	glob_tilts.append(tiltclass.TiltClass(key, TILTS[key], 1)) # define all tilt classes, for debugging upload set to 1 minute

glob_currentTilt = "Null"

#
# eink display initialisation
#

def initPartial():
	epd.init(epd.FULL_UPDATE)
	print("Clear eink display...")
	epd.Clear(0xFF)
	epd.displayPartBaseImage(epd.getbuffer(global_UpdateImage))
	epd.init(epd.PART_UPDATE)

#
# eink screen update
#


def printTilt():
	global glob_currentTilt
#	gravImage = Image.new('1',(epdscreen.EPD_HEIGHT, epdscreen.EPD_WIDTH), 255) # define gravImage based on screen maximum size
	drawObj = ImageDraw.Draw(global_UpdateImage) # Create draw object and pass in the image layer
	drawObj.rectangle((0,0,140,15), fill = 255)
	drawObj.rectangle((0,30,220,100), fill = 255)

	fontTimeObj = ImageFont.truetype('/usr/share/fonts/truetype/msttcorefonts/Times_New_Roman.ttf',16)
	fontGravityObj = ImageFont.truetype('/usr/share/fonts/truetype/msttcorefonts/Times_New_Roman.ttf',48)
	fontTempObj = ImageFont.truetype('/usr/share/fonts/truetype/msttcorefonts/Times_New_Roman.ttf',32)
	fontNameObj = ImageFont.truetype('/usr/share/fonts/truetype/msttcorefonts/Times_New_Roman.ttf',20)
	fontUnitsObj = ImageFont.truetype('/usr/share/fonts/truetype/msttcorefonts/Times_New_Roman.ttf',18)

	drawObj.text((0,0), time.strftime('%d/%m/%y - %H:%M') , font = fontTimeObj, fill = 0)

	displayData = getDisplayData(glob_currentTilt)

	print(displayData)

	glob_currentTilt=displayData[0]						# set currentTilt to the new tiltname

	if displayData[0]=="None":	# No active tilt data found so display generic message
		drawObj.text((40,50),"No active Tilt found", font = fontNameObj, fill = 0)
		epd.displayPartial(epd.getbuffer(global_UpdateImage))
		return
	
	drawObj.text((0,42),displayData[0], font = fontNameObj, fill = 0)	# Display Tilt name
	drawObj.text((70,30),displayData[1], font = fontGravityObj, fill = 0)	# Display Tilt gravity
	drawObj.text((180,47),"SG", font = fontUnitsObj, fill = 0)		# Display specific gravity SG
	drawObj.text((90,70),displayData[2], font = fontTempObj, fill = 0)	# Display Tilt temperature
	drawObj.text((150,77),u"\u00b0"+"C", font = fontUnitsObj, fill = 0)	# Display degrees C
	
	epd.displayPartial(epd.getbuffer(global_UpdateImage))

def getDisplayData(currenttilt):
	num_of_tilts_active=0

	for tilt in glob_tilts:
		if tilt.seenRecently():
			num_of_tilts_active += 1
	
	if num_of_tilts_active==0:			# No active tilts found so return "None" as the name and
		return "None","0","0","Null"		# 0s to make sure tuple variable filled

	if num_of_tilts_active>1:			# More than 1 active tilt so cycle through tem and select the
		for tilt in glob_tilts:			# one after the currently displayed one
			if tilt.seenRecently():
				if tilt.checkName(currentTilt):
					continue
				return tilt.tiltName,f'{float(tilt.specificGravity()):.3f}',str(tilt.tempCelsius())
	
	for tilt in glob_tilts:				# Only one active tilt, so find it and return that info
		if tilt.seenRecently():
			return tilt.tiltName,f'{float(tilt.specificGravity()):.3f}',str(tilt.tempCelsius())


def distinct(objects):
	seen = set()
	unique = []
	for obj in objects:
		if obj['uuid'] not in seen:
			unique.append(obj)
			seen.add(obj['uuid'])
	return unique

def setTiltData(uuid,temp,gravity):
	for tilt in glob_tilts:
		if tilt.checkUUID(uuid):
			tilt.tiltUpdate(temp,gravity)
			return

def monitorTilts():
	while True:
		beacons = distinct(blescan.parseEvents(sock,10))
		for beacon in beacons:
			if beacon['uuid'] in TILTS.keys():
				# found a tilt
				print("colour: ", TILTS[beacon['uuid']]) # which tilt
				print("temp:", beacon['major']) # temp (in faranheit
				print("gravity:", beacon['minor'])
				setTiltData(beacon['uuid'],beacon['major'],beacon['minor'])
		time.sleep(10)



initPartial()



if __name__ == '__main__':
	dev_id=0
	try:
		sock=bluez.hci_open_dev(dev_id)
		print("Starting tilt testing ...")
	except:
		print("Critical Error: Unable to access bluetooth device.")
		sys.exit(1)

	blescan.hciLESetScanParameters(sock)
	blescan.hciEnableLEScan(sock)

	threadMonitorTilts = threading.Thread(target=monitorTilts)
	threadMonitorTilts.daemon = True
	print("Starting monitorTilts thread ...")
	threadMonitorTilts.start()

	while(True):
		printTilt()
		time.sleep(3)

