#!/usr/bin/env python
import Image
import ImageStat
import math
import os
import time
import sys
import json


samplerate = 5.0
fixed = False

config_file = json.load(open('config.json'))
default_config = {'fixed':fixed, 'samplerate':samplerate}

def brightness(im_file):
	   im = Image.open(im_file)
	   stat = ImageStat.Stat(im)
	   r,g,b = stat.mean
	   return math.sqrt(0.241*(r**2) + 0.691*(g**2) + 0.068*(b**2))

def takeSample(tmpimg):
	import pygame.camera
	pygame.camera.init()
	cam = pygame.camera.Camera(pygame.camera.list_cameras()[0])
	cam.start()
	img = cam.get_image()
	import pygame.image
	pygame.image.save(img, tmpimg)
	pygame.camera.quit()
	cam.stop()



class autoBrightness():
	def __init__(self, samplerate=config_file['samplerate']):
		self.samplerate = samplerate
		while True:
			tmpimg = "/tmp/autobrightness-sample.bmp"
			takeSample(tmpimg)
			brightnessLevel = brightness(tmpimg)
			set = (brightnessLevel/255)*100
			os.system('xbacklight -set '+str(set))
			time.sleep(self.samplerate)	
	

if __name__ == "__main__":
	

	args = sys.argv
	if len(args) >= 2:
		error = True
		for i in xrange(len(args)):
			if args[i] == "help" or args[i] == "--help" or args[i] == "-help" or args[i] == "-h":
				print "USAGE: autobrightness [OPTION]... [TIME BETWEEN SAMPLES]...\n\n Adjusts a laptop's brightness automatically, by using camera samples taken at a user definable interval.\n\n -s, --set              set time between samples to your configuration file\n -t, --time              set time between samples for this session"
				exit()

			if args[i] == "-s" or args[i] == "--set":
				default_config['samplerate'] = args[i+1]
				print "Your default time interval is now '%s' seconds" % args[i+1]
				json.dump(default_config, open('config.json', 'w'))
				exit()

			if args[i] == "-t" or args[i] == "-time":
				if float(args[i]) < 0:
					print "Your sampling rate cannot be a negative number.  Resetting to default value of 5."
					error = False
					break

		if error:
			print "autobrightness: There is no '%s' OPTION\nTry 'autobrightness --help' for more information" % args[1]
			exit()
	autoBrightness(samplerate)

