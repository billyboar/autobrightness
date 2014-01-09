#!/usr/bin/env python
import Image
import ImageStat
import math
import os
import time
import sys


def brightness(im_file):
   im = Image.open(im_file)
   stat = ImageStat.Stat(im)
   r,g,b = stat.mean
   return math.sqrt(0.241*(r**2) + 0.691*(g**2) + 0.068*(b**2))

def camera(tmpimg):
	import pygame.camera
	pygame.camera.init()
	cam = pygame.camera.Camera(pygame.camera.list_cameras()[0])
	cam.start()
	img = cam.get_image()
	import pygame.image
	pygame.image.save(img, tmpimg)
	pygame.camera.quit()
	cam.stop()
	
samplerate = 5
if len(sys.argv) >= 2:
	for arg in sys.argv:
		try:
                        samplerate = float(arg)
                except:
                	cfg_file = arg
                		
                        

while True:
	tmpimg = "/tmp/autobrightness-sample.bmp"
	camera(tmpimg)
	a = brightness(tmpimg)
	os.remove(tmpimg)
	set = (a*100)/255
	os.system('xbacklight -set '+str(set))
	time.sleep(samplerate)

