import RPi.GPIO as GPIO
import time

########################
# Constantes
########################
BUTTON_YELLOW = 18
BUTTON_RED = 23

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_RED, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_YELLOW, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
	button_red_status = GPIO.input(BUTTON_RED)
	button_yellow_status = GPIO.input(BUTTON_YELLOW)

	if button_red_status == False:
		print("Button red pressed")
		# Temps de repos pour eviter la surchauffe du processeur
		time.sleep(0.3)
		

	if button_yellow_status == False:
		print("Button yellow pressed")
		# Temps de repos pour eviter la surchauffe du processeur
		time.sleep(0.3)
	
	

GPIO.cleanup()