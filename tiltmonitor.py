import sys
sys.path.insert(1,"./lib")
import epd2in13_V2 as epdscreen

from PIL import Image, ImageDraw, ImageFont
import time
import datetime

import bluetooth._bluetooth as bluez

import blescan
import tiltclass

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

def initPartial():
	epd.init(epd.FULL_UPDATE)
	print("Clear eink display...")
	epd.Clear(0xFF)
	epd.displayPartBaseImage(epd.getbuffer(global_UpdateImage))
	epd.init(epd.PART_UPDATE)

def printGravity(string):
#	gravImage = Image.new('1',(epdscreen.EPD_HEIGHT, epdscreen.EPD_WIDTH), 255) # define gravImage based on screen maximum size
	drawObj = ImageDraw.Draw(global_UpdateImage) # Create draw object and pass in the image layer
	drawObj.rectangle((15,5,140,20), fill = 255)
	drawObj.rectangle((60,30,180,100), fill = 255)
	fontGravityObj = ImageFont.truetype('/usr/share/fonts/truetype/msttcorefonts/Times_New_Roman.ttf',48)
	fontTimeObj = ImageFont.truetype('/usr/share/fonts/truetype/msttcorefonts/Times_New_Roman.ttf',16)
	drawObj.text((60,30),string, font = fontGravityObj, fill = 0)
	drawObj.text((15,5), time.strftime('%d/%m/%y - %H:%M:%S') , font = fontTimeObj, fill = 0)
	epd.displayPartial(epd.getbuffer(global_UpdateImage))

def getGravity():
	gravityReading = temp_gravRead
	return f'{float(gravityReading):.3f}'

def distinct(objects):
	seen = set()
	unique = []
	for obj in objects:
		if obj['uuid'] not in seen:
			unique.append(obj)
			seen.add(obj['uuid'])
	return unique

def monitor_tilts():
	while True:
		beacons = distinct(blescan.parseEvents(sock,10))
		for beacon in beacons:
			if beacon['uuid'] in TILTS.keys():
				# found a tilt
				print("colour: ", TILTS[beacon['uuid']]) # which tilt
				print("temp:", beacon['major']) # temp (in faranheit
				print("gravity:", beacon['minor'])
		time.sleep(10)



initPartial()


#while(True):
#
#	printGravity(getGravity())
#	time.sleep(1)
#	temp_gravRead=temp_gravRead+0.001

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
	monitor_tilts()
