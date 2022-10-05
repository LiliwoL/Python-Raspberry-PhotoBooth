#!/usr/bin/env python

# Using py-getch
# Github: joeyespo/py-getch

from getch import getch, pause
import picamera, time, random, thread
import upload, os				# Upload
import pygame.mixer 				# Sound
import io, time					# Image Sequence
import errno


########################
# Create a Dir function
########################
def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise
########################



########################################
# Generate a GIF from images in a folder
########################################
def makeAGif(path, name):
	os.system( 'convert -delay 20 -loop 0 ' + path + '/*.jpg ' + path + "/" + name + '.gif' )
	return ( path + "/" + name + '.gif' )




# General
path = "/home/pi/photobooth/"


# Assets
dir_assets = os.listdir( path + "assets" )
assets = []
for file in dir_assets:
   assets.append( file )


# Sound
from pygame.mixer import music
pygame.mixer.init()



print "PhotoBooth by Ctrl Art Suppr"

########
# Camera
########

# Activation Camera
camera = picamera.PiCamera()

#Reglages
#camera.resolution = (2592, 1944) # 4/3
#camera.resolution = (1296, 730) # 16/9
#camera.resolution = (1296, 972) # 4/3
camera.resolution = (640, 480) # 4/3

#set color of annotation 
camera.annotate_foreground = picamera.Color(y=0.2, u=0, v=0)


# Effets
camera.brightness = 60
camera.start_preview()

while True:
	key = getch()
  
	if key == " ":
		print 'Espace!'
		#start camera preview                
	        

        	#display text over preview screen
	        camera.annotate_text = 'Get Ready!'

        	camera.annotate_text = '5'
		print "5"
		time.sleep(1)

		camera.annotate_text = '4'
		print "4"
		time.sleep(1)

		camera.annotate_text = '3'
		print "3"
		time.sleep(1)

		camera.annotate_text = '2'
		print "2"
		time.sleep(1)

		camera.annotate_text = '1'
		print "1"
		time.sleep(1)
		print "0"

		# Son
		assetFile = random.choice( assets )
		asset = music.load( path + "assets/" + assetFile )
		music.play()

		# Nom du fichier
		filename = path + "capture/" + time.strftime( "%Y%m%d-%H%M%S") + ".jpg"
		camera.capture( filename )

		#camera.stop_preview() #stop preview 
		print 'Photo prise!'

		###################
		# Upload sur Tumblr
		###################
		print upload.uploadToTumblr( filename )


	if key == "g":
		print "Animation!"
		
		start = time.time()
		animation_path = path + "capture/" + time.strftime( "%H%M")
		mkdir_p( animation_path )

		for filename in camera.capture_continuous( animation_path + '/img{counter:03d}.jpg' ):
			print( 'Captures %s' % filename )
			time.sleep( 1 )

			# Arret au bout de 5 secondes
			if time.time() - start > 5:
				break

		print 'Generate a GIF'
		gif = makeAGif ( animation_path, time.strftime( "%H%M") )
		
		###################
		# Upload sur Tumblr
		###################
		print upload.uploadToTumblr( gif )


	elif key == "0":
		break