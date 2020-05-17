import sys
sys.path.insert(1,"./lib")
import epd2in13_V2 as epdscreen

from PIL import Image, ImageDraw, ImageFont
import time

epd = epdscreen.EPD()

global_UpdateImage = Image.new('1',(epdscreen.EPD_HEIGHT, epdscreen.EPD_WIDTH) ,255)

temp_gravRead = 1.000

def initPartial():
	epd.init(epd.FULL_UPDATE)
	print("Clear...")
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



initPartial()


while(True):

	printGravity(getGravity())
	time.sleep(1)
	temp_gravRead=temp_gravRead+0.001


