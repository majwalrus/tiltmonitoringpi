# based on https://github.com/switchdoclabsiBeacon-Scanner- and https://github.com/atlefren/pytilt and updated to Python3

import os
import sys
import struct
import bluetooth._bluetooth as bluez

LE_META_EVENT = 0x3e
LE_PUBLIC_ADDRESS = 0x00
LE_RANDOM_ADDRESS = 0x01
LE_SET_SCAN_PARAMETERS_CP_SIZE = 7
OGF_LE_CTL = 0x08
OCF_LE_SET_SCAN_PARAMETERS = 0x000B
OCF_LE_SET_SCAN_ENABLE = 0x000C
OCF_LE_CREATE_CONN = 0x000D

LE_ROLE_MASTER = 0x00
LE_ROLE_SLAVE = 0x01

# these are actually subevents of LE_META_EVENT
EVT_LE_CONN_COMPLETE = 0x01
EVT_LE_ADVERTISING_REPORT = 0x02
EVT_LE_CONN_UPDATE_COMPLETE = 0x03
EVT_LE_READ_REMOTE_USED_FEATURES_COMPLETE = 0x04

# Advertisement event types
ADV_IND = 0x00
ADV_DIRECT_IND = 0x01
ADV_SCAN_IND = 0x02
ADV_NONCONN_IND = 0x03
ADV_SCAN_RSP = 0x04

def returnNumberPacket(pkt):
	integer=0
	multiple = 256
	for i in range(len(pkt)):
		integer+=struct.unpack('B',pkt[i:i+1])[0]*multiple
		multiple = 1
	return integer

def returnStringPacket(pkt):
	string=''
	for i in range(len(pkt)):
		string+='%02x' % struct.unpack('B',pkt[i:i+1])[0]
	return string

def printPacket(pkt):
	for c in pkt:
		sys.stdout.write('%02x' % struct.unpack('B',c)[0])

def getPackedBDaddr(bdaddr_string):
	packable_addr = []
	addr = bdaddr_string.split(':')
	addr.reverse()
	for b in addr:
		packable_addr.append(int(b,16))
	return struct.pack('<BBBBBB', *packable_addr)

def packedBDaddrToString(bdaddr_packed):
	return ':'.join('%02x' % i for i in struct.unpack("<BBBBBB", bdaddr_packed[::-1]))

def hciEnableLEScan(sock):
	hciToggleLEScan(sock,0x01)

def hciDisableLEScan(sock):
	hciToggleLEScan(sock,0x00)

def hciToggleLEScan(sock,enable):
	cmd_pkt = struct.pack("<BB", enable, 0x00)
	bluez.hci_send_cmd(sock, OGF_LE_CTL, OCF_LE_SET_SCAN_ENABLE, cmd_pkt)

def hciLESetScanParameters(sock):
	old_filter = sock.getsockopt(bluez.SOL_HCI, bluez.HCI_FILTER, 14)

	SCAN_RANDOM = 0x01
	OWN_TYPE = SCAN_RANDOM
	SCAN_TYPE = 0x01
	# Is ths needed? Doesn't look used


def parseEvents(sock,loop_count=100):
	old_filter = sock.getsockopt(bluez.SOL_HCI, bluez.HCI_FILTER, 14)

	# perform a device inquiry on bluetooth device #0
	# The inquiry should last 8 * 1.28 = 10.24 seconds
	# before the inquiry is performed, bluez should flush
	# its cache of previosuly discovered devices

	flt = bluez.hci_filter_new()
	bluez.hci_filter_all_events(flt)
	bluez.hci_filter_set_ptype(flt, bluez.HCI_EVENT_PKT)
	sock.setsockopt(bluez.SOL_HCI, bluez.HCI_FILTER, flt)
	beacons = []
	for i in range (0, loop_count):
		pkt = sock.recv(255)
		pktype, event, plen = struct.unpack('BBB', pkt[:3])

		if event == LE_META_EVENT:
			subevent, = struct.unpack('B', pkt[3:4])
			pkt = pkt[4:]
			if subevent == EVT_LE_CONN_COMPLETE:
				le_handle_connection_complete(pkt)
			elif subevent == EVT_LE_ADVERTISING_REPORT:
				num_reports = struct.unpack('B',pkt[0:1])[0]
				report_pkt_offset = 0
				for i in range(0, num_reports):
					beacons.append({
						'uuid': returnStringPacket(pkt[report_pkt_offset - 22: report_pkt_offset - 6]),
						'minor': returnNumberPacket(pkt[report_pkt_offset - 4: report_pkt_offset - 2]),
						'major': returnNumberPacket(pkt[report_pkt_offset - 6: report_pkt_offset - 4])
					})
				done = True
	sock.setsockopt(bluez.SOL_HCI, bluez.HCI_FILTER, old_filter)
	return beacons




