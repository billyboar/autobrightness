#!/usr/bin/env python
import Image
import ImageStat
import math
import os
import time


def convertToBmp(im_file):
	img = Image.open(im_file)
	img.save("out.bmp")
	return 

def brightness(im_file):
   im = Image.open(im_file)
   stat = ImageStat.Stat(im)
   r,g,b = stat.mean
   return math.sqrt(0.241*(r**2) + 0.691*(g**2) + 0.068*(b**2))
 
def camera():
	import pygame.camera
	pygame.camera.init()
	cam = pygame.camera.Camera(pygame.camera.list_cameras()[0])
	cam.start()
	img = cam.get_image()
	import pygame.image
	pygame.image.save(img, "photo.bmp")
	pygame.camera.quit()
	cam.stop()

while True:
	time.sleep(5)
	camera()	
	a = brightness('photo.bmp')
	set = (a*100)/110
	os.system('xbacklight -set '+str(set))

