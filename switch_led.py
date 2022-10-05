#!/usr/bin/env python

import RPi.GPIO as GPIO
from time import sleep
import picamera
from picamera import Color
import pygame

def main():

	# GPI Mode Test
	GPIO.setmode(GPIO.BCM)

	pygame.display.init()

	# Where the button is linked
	button = 18
	# Leds
	yellowLed = 17
	blueLed = 27

	# Set the switch as an input
	GPIO.setup(button, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

	# Set Leds as output
	GPIO.setup(yellowLed, GPIO.OUT)
	GPIO.setup(blueLed, GPIO.OUT)

	# GPIO.setwarnings(False)

	# Camera
	camera = picamera.PiCamera()
	camera.resolution = (640, 480)
	camera.brightness = 60
	camera.sharpness = 10
	camera.contrast = 30

	camera.annotate_text_size = 50
	camera.annotate_background = Color('blue')
	camera.annotate_foreground = Color('yellow')
	camera.annotate_text = " Photo? "

	camera.stop_preview()

	try:
		while True:
			if GPIO.input(button):
				GPIO.output(17,False)
			        GPIO.output(27,False)
				print("button pressed")
				sleep(0.2)

				camera.start_preview(alpha=200)
	
				for i in range(3):
					GPIO.output(yellowLed, True)
					sleep(1)
					GPIO.output(yellowLed, False)
				sleep(1)
			
				camera.annotate_text = " Souriez "
	
				for i in range(3):
					GPIO.output(yellowLed, True)
					sleep(.25)
					GPIO.output(yellowLed, False)
					sleep(.25)	
				
	
				camera.capture('test.jpg')
				camera.stop_preview()
	
				imgSurf= pygame.image.load('test.jpg')
				screen = pygame.display.set_mode( imgSurf.get_size(), pygame.FULLSCREEN )
				pygame.display.flip()
	
				#camera.close()
	
				camera.annotate_text = " Envoi de la photo "
		
				for i in range(5):
					GPIO.output(blueLed, True)
					sleep(.1)
					GPIO.output(blueLed, False)
					sleep(.1)
				camera.annotate_text = ""
	
				sleep(3)
				pygame.quit()
			else:
				GPIO.output(17,True)
			        GPIO.output(27,True)
	
		GPIO.cleanup()
	except KeyboardInterrupt:
		print ('program stopped')
		GPIO.cleanup()


if __name__=="__main__":
    main()
