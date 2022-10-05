#!/usr/bin/env python

# PhotoBooth python
# Before use:
#   Set correct GPIO pins for LEDs and press buttons



import random, _thread
import upload, os           # Upload
import pygame.mixer         # Sound
import io, time             # Image Sequence
import errno

# PiCamera
import picamera
from picamera import Color

# GPIO Support
# Real GPIO
import RPi.GPIO as GPIO


# Emulator GPIO
#from EmulatorGUI import GPIO


# Image
from PIL import Image



########################
# Constantes
########################
LED_RED = 27
LED_YELLOW = 17
BUTTON_SNAP = 18
BUTTON_ANIMATION = 23

# General
PATH = "/home/pi/Documents/Photobooth/"
camera = 0






########################
# Create a Dir function
########################
def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EXIST and os.path.isdir(path):
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
########################################



########################################
# Uploads to tumblr
########################################
def uploadFile( file ):
    from threading import Thread

    #t = Thread( target=upload.uploadToTumblr( file ) )
    #t.daemon = True
    #t.start()

    upload.uploadToTumblr( file )

    # Blink red led
    blink_led( LED_RED, 10, .1 )


########################################


##########################################
# Blink a led
##########################################
def blink_led( led_color, how_many_time, blinking_duration ):

    # On alterne letat ON et letat OFF
    # led_color (int) GPIO pin number
    # how_many_time (int)
    # blinking_duraton (float) Second

    for i in range( how_many_time ):
        GPIO.output( led_color , True)
        time.sleep( blinking_duration )

        GPIO.output( led_color , False)
        time.sleep( blinking_duration )

    GPIO.output( led_color, False)

##########################################


##########################################
# Camera
##########################################
def camera_setup():
    global camera
    # Activation Camera
    camera = picamera.PiCamera()

    # Resolution
    camera.resolution = (2592, 1944) # 4/3
    #camera.resolution = (1296, 730) # 16/9
    #camera.resolution = (1296, 972) # 4/3
    #camera.resolution = (640, 480) # 4/3

    # Reglages de limage
    camera.brightness = 60
    camera.sharpness = 10
    camera.contrast = 30

    # Effets
    #camera.image_effect = 'cartoon'

    # Texte dannotation
    #camera.annotate_text_size = 60
    #camera.annotate_background = Color('blue')
    #camera.annotate_foreground = picamera.Color(y=0.2, u=0, v=0)

#########################################


########################################
# ImageMagick Filter
########################################
def apply_filter( filter, image_src):
    import ctypes
    from wand.api import library
    from wand.image import image

    library.MagickVignetteImage.argtypes = [ctypes.c_void_p, # wand
                                            ctypes.c_double, #Radius
                                            ctypes.c_double, #Sigma
                                            ctypes.c_long,   # x
                                            ctypes.c_long]   # y
    class VignetteImage(Image):
        def vignette( self, radius=0.0, sigma=0.0, offet_x=0, offset_y=0):
            library.MagickVignetteImage( self.wand,
                                         radius,
                                         sigma,
                                         offset_x,
                                         offset_y)


    # Toaster Effect
    # Old polaroid Effect
    if filter == "toaster":
        with VignetteImage( image_src ) as toaster:
            toaster.vignette(0.0, 5.0)
            toaster.save( filename="toaster.png")
########################################


######################################
# Play a Sound
######################################
def playSound( sound ):
    # sound is a variable to choose which sound to be played
    # Sound files must be located in PATH/assets/sound folder

    # Sound import
    from pygame.mixer import music
    pygame.mixer.init()


    # Liste des assets music
    sound_assets_dir = os.listdir( PATH + "assets/sound" )
    assets = []
    for file in sound_assets_dir:
       assets.append( file )

    assetFile = random.choice( assets )


    music.load( sound_assets_dir + "/" + assetFile )
    #music.play()
######################################


################
# Take a snap! #
################
def snap():

    # the button is being pressed, so turn on the green LED
    # and turn off the red LED
    #GPIO.output( LED_YELLOW, False)
    #GPIO.output( LED_RED, False)

    #music.init()

    #start camera preview
    #camera.start_preview() #alpha=200

    #display text over preview screen
    #camera.annotate_text = 'Get Ready!'
    time.sleep(1)


    # Compte a rebours de 5 a 2
    """ for i in reversed( range(5, 2) ):
        # Allume la led jaune
        GPIO.output( LED_YELLOW , True)

        # Mise a jour du output
        camera.annotate_text = str(i+2)
        time.sleep(1)

        # Eteint la led jaune
        GPIO.output( LED_YELLOW, False)
        time.sleep(1) """


    # Compte a rebours de 2 a 1
    """ for i in reversed( range(3) ):
        GPIO.output( LED_YELLOW, True)

        camera.annotate_text = str(i)
        time.sleep(.25)

        GPIO.output( LED_YELLOW, False)
        time.sleep(.25) """

    #camera.annotate_text = ''

    # Play sound
    #playSound()

    # Nom du fichier
    filename = PATH + "capture/" + time.strftime( "%Y%m%d-%H%M%S") + ".jpg"
    camera.capture( filename )

    #camera.stop_preview() #stop preview
    camera.annotate_text = 'Photo prise!'
    print ('Photo prise!')

    imgSurf= pygame.image.load( filename )
    screen = pygame.display.set_mode( imgSurf.get_size(), pygame.FULLSCREEN )
    pygame.display.flip()

    ###################
    # Upload sur Tumblr
    ###################
    camera.annotate_text = ' Envoi de la photo '
    uploadFile ( filename )
    camera.annotate_text = 'Encore'

    pygame.quit()

################





######################
# Configuration GPIO #
######################
def config_gpio():

    ## GPIO.cleanup()

    # tell the GPIO module that we want to use the
    # chip's pin numbering scheme
    GPIO.setmode(GPIO.BCM)
    #GPIO.setwarnings(False)


    # Button Snap Pin
    GPIO.setup( BUTTON_SNAP, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
    #GPIO.setup(18, GPIO.IN)


    # Button Animation Pin
    GPIO.setup( BUTTON_ANIMATION, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)


    # Yellow Led Pin
    GPIO.setup( LED_YELLOW, GPIO.OUT)
    GPIO.output( LED_YELLOW, GPIO.LOW)    

    # Red Led Pin
    GPIO.setup( LED_RED, GPIO.OUT)
    GPIO.output( LED_RED, GPIO.LOW)
################################


################################
# Overlay Image function
################################
def overlay_image():
    # Load the image
    img = Image.open( PATH + 'overlay_logo.png')

    # Create an image padded to the required size with mode RGB
    pad = Image.new('RGB', (
        ((img.size[0] + 31) // 32) * 32,
        ((img.size[1] + 15) // 16) * 16,
    ))

    # Paste the original image into the padded one
    pad.paste(img, (0,0), img)

    # Add the overlay with the padded image as the source,
    # but the original image's dimensions
    o = camera.add_overlay(pad.tostring(), size=img.size)

    # By default the overlay is in layer 0, beneath the preview (whic default layer is 2)
    # Here we make the new overlay semi transparent,  then move it above the previex
    o.alpha = 235
    o.layer = 3
################################


################################
# Fonction principale
################################
def main():
    # Configuration GPIO
    config_gpio()

    # Configuraton Camera
    camera_setup()

    camera.start_preview()

    # Overlay image
    #overlay_image()

    #display text over preview screen
    #camera.annotate_text = 'Une photo?'

    old_button_status=GPIO.input(BUTTON_SNAP)
    OLD=BUTTON_STATUS=0

    #blink_led( LED_RED, 10, .1 )

    print ("GPIO du bouton 18")
    print (GPIO.input(BUTTON_SNAP))

    #try:

    while 1:
        button_status=GPIO.input( BUTTON_SNAP )

        if old_button_status != button_status:

            # Snap Button
            if button_status == True:
                # the button isn't being pressed, so turn off the green LED
                # and turn on the red LED
                GPIO.output( LED_YELLOW, False)
                GPIO.output( LED_RED, True)
                #print "Nothing"

            # Animation Button
            #elif GPIO.input( BUTTON_ANIMATION ):
                # Animation!
                #animation()

        # Nothing
        else:
            print ("snap")
            # Snap!
            snap()
            print ("snap")

        old_button_status=button_status               

    time.sleep(1)

    GPIO.cleanup()

    #except KeyboardInterrupt:
    #    print('Program stopped')
##################################




## Lancement
if __name__=="__main__":
    ## GPIO.cleanup()
    print ("PhotoBooth Last ? by Ctrl Art Suppr")
    main()
