import sys
import datetime
import time

import bluetooth._bluetooth as bluez

import blescan
import tiltclass


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

