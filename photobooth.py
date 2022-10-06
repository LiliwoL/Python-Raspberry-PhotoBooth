#!/usr/bin/env python

"""
 ____        _   _                    ____ ____ ___ ___  
|  _ \ _   _| |_| |__   ___  _ __    / ___|  _ \_ _/ _ \ 
| |_) | | | | __| '_ \ / _ \| '_ \  | |  _| |_) | | | | |
|  __/| |_| | |_| | | | (_) | | | | | |_| |  __/| | |_| |
|_|    \__, |\__|_| |_|\___/|_| |_|  \____|_|  |___\___/ 
       |___/                                             
"""
"""
    Important!

    Connecter le bouton aux PIN
        3 et 6
    cf. https://pinout.xyz/#
"""


import time
import RPi.GPIO as GPIO
# PiCamera
import picamera
from picamera import Color
# Image
import pygame
# Text Overlay
from PIL import Image, ImageDraw, ImageFont
# Dir
import os



########################
# Constantes
########################
BUTTON_SNAP = 23
BUTTON_ANIMATION = 18
LED_RED = 5
LED_YELLOW = 13
PATH = "/home/pi/Téléchargements/PhotoBooth/"
VIDEO_HEIGHT = 0
VIDEO_WIDTH = 0
OVERLAY= "FIRST"

# Configuration de l'app
LEDS_ON = False
SEND_MAIL = False
UPLOAD_FILE = False

########################
# Create a Dir function
########################
def mkdir_p(path):
    import os, errno

    try:
        os.makedirs(path)
    except OSError as error:  # Python >2.5
        if error.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise
########################


######################
# Configuration GPIO #
######################
def config_gpio():
    # https://pinout.xyz/#

    ## GPIO.cleanup()

    # tell the GPIO module that we want to use the
    # chip's pin numbering scheme
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    # Button Snap Pin
    GPIO.setup( BUTTON_SNAP, GPIO.IN, pull_up_down = GPIO.PUD_UP)

    # Button Animation Pin
    GPIO.setup( BUTTON_ANIMATION, GPIO.IN, pull_up_down = GPIO.PUD_UP)

    # Yellow Led Pin
    GPIO.setup( LED_YELLOW, GPIO.OUT)
    GPIO.output( LED_YELLOW, GPIO.LOW)    

    # Red Led Pin
    GPIO.setup( LED_RED, GPIO.OUT)
    GPIO.output( LED_RED, GPIO.LOW)

################################

################
# Camera Setup #
################
def camera_setup():
    global camera
    global VIDEO_HEIGHT
    global VIDEO_WIDTH

    # Activation Camera
    camera = picamera.PiCamera()

    # Resolution
    # WIDTH doit être un multiple de 32
    # HEIGHT doit être un mutiple de 16
    VIDEO_WIDTH = 640
    VIDEO_HEIGHT = 480
    #camera.resolution = (VIDEO_WIDTH, VIDEO_HEIGHT)

    #camera.resolution = (2592, 1944) # 4/3
    #camera.resolution = (1296, 730) # 16/9
    #camera.resolution = (1296, 972) # 4/3
    camera.resolution = (640, 480) # 4/3

    # Reglages de limage
    #camera.brightness = 50
    #camera.sharpness = 10
    #camera.contrast = 30

    # Effets
    #camera.image_effect = 'cartoon'

    # Texte d'annotation
    #camera.annotate_text_size = 55
    #camera.annotate_background = Color('blue')
    #camera.annotate_foreground = picamera.Color(y=0.2, u=0, v=0)

    # Données EXIF
    camera.exif_tags['IFD0.Artist'] = 'Ctrl Art Suppr!'
    camera.exif_tags['IFD0.Copyright'] = 'Copyrights are killing creativity'

    # Preview camera
    camera.start_preview( alpha=255, fullscreen=True)
################

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

########################################
# Uploads to tumblr
########################################
def uploadFile( file ):
    from threading import Thread
    import upload

    upload.uploadToTumblr( file )
######################################

######################################
# Play a Sound
######################################
def playSound( sound = False ):
    import random, os, pygame

    SOUND_ASSETS_DIR = os.getcwd() + "/assets"
    
    pygame.mixer.init()

    if ( sound ):
        asset = sound
    else:
        # Liste des assets sounds
        assets = os.listdir( SOUND_ASSETS_DIR )
        asset = random.choice( assets )

    pygame.mixer.music.load( SOUND_ASSETS_DIR + "/" + asset )
    pygame.mixer.music.play()
######################################


def displayPicture( filename = False ):
    global camera

    if filename:
        # Load the arbitrarily sized image
        img = Image.open( filename )
        # Create an image padded to the required size with
        # mode 'RGB'
        pad = Image.new('RGB', (
            ((img.size[0] + 31) // 32) * 32,
            ((img.size[1] + 15) // 16) * 16,
            ))
        # Paste the original image into the padded one
        pad.paste(img, (0, 0))

        # Add the overlay with the padded image as the source,
        # but the original image's dimensions
        o = camera.add_overlay( pad.tobytes(), size=img.size )

        #o.fullscreen = false
        o.window = (0, 0, 750, 400)

        # By default, the overlay is in layer 0, beneath the
        # preview (which defaults to layer 2). Here we make
        # the new overlay semi-transparent, then move it above
        # the preview
        o.alpha = 32
        o.layer = 3

        time.sleep(3)

        camera.remove_overlay( o )
        


################
# Take a snap! #
################
def snap():
    global SURFACE

    # Play a random sound
    playSound()

    # Text on screen
    #camera.annotate_text = 
    displayText('Get Ready!')
    time.sleep(1)
    #camera.annotate_text = '3'
    displayCounter('3')
    time.sleep(1)
    #camera.annotate_text = '2'
    displayCounter('2')
    time.sleep(1)
    #camera.annotate_text = '1'
    displayCounter('1')
    time.sleep(1)

    # Nom du fichier
    # Création du dossier si inexistant
    mkdir_p( PATH + "capture/" + time.strftime( "%Y%m%d")  )

    filename = PATH + "capture/" + time.strftime( "%Y%m%d")  + "/" + time.strftime( "%Y%m%d-%H%M%S") + ".jpg"

    # Erase text on screen
    displayText('')
    #camera.annotate_text = ""

    # Petit flash pour montrer que la photo a été prise
    camera.brightness = 60
    time.sleep(.01)
    camera.brightness = 80
    time.sleep(.01)
    camera.brightness = 100
    time.sleep(.01)
    camera.brightness = 80
    time.sleep(.01)
    camera.brightness = 60
    time.sleep(.01)
    # Son du déclenchement
    playSound("snap.mp3")

    # Capture
    camera.capture( filename )

    # Text on screen
    #camera.annotate_text = 'Photo prise!'
    displayText( 'Photo prise!' )

    time.sleep(2)

    displayText( 'Photo -> Rouge Animation -> Jaune' )

    # Affiche l'image prise
    #displayPicture ( filename )

    ###################
    # Upload sur Tumblr
    ###################
    if UPLOAD_FILE:
        uploadFile ( filename )

    ###################
    # Send Email
    ###################
    if SEND_MAIL:
        sendMail ( filename )

###############################

########################################
# Animation
########################################
def animation():
    start = time.time()

    animation_path = PATH + "capture/" + time.strftime( "%Y%m%d")
    mkdir_p( animation_path )

    # Text on screen
    #camera.annotate_text = 'Get Ready for the anim!'
    displayText( 'Get Ready for the anim!' )
    time.sleep(1)
    #camera.annotate_text = '3'
    displayCounter( '3' )
    time.sleep(1)
    #camera.annotate_text = '2'
    displayCounter( '2' )
    time.sleep(1)
    #camera.annotate_text = '1'
    displayCounter( '1' )
    time.sleep(1)

    # Erase text on screen
    displayText("")

    for filename in camera.capture_continuous( animation_path + '/img{counter:03d}.jpg' ):
        print( 'Captures %s' % filename )
        time.sleep( 1 )

        # Affichage d'un flash
        

        # Arret au bout de 5 secondes
        if time.time() - start > 10:
            break

    print ('Generate a GIF')
    gif = makeAGif ( animation_path, time.strftime( "%H%M") )

    # Text on screen
    displayText( 'Anim prise!' )
    time.sleep(2)
    displayText( 'Photo -> Rouge Animation -> Jaune' )
            
    ###################
    # Upload sur Tumblr
    ###################
    if UPLOAD_FILE:
        displayText( ' Envoi de l\'animation ' )
        uploadFile ( gif )

########################################

########################################
# Generate a GIF from images in a folder
########################################
def makeAGif(path, name):
    import os

    os.system( 'convert -delay 20 -loop 0 ' + path + '/*.jpg ' + path + "/" + name + '.gif' )
    return ( path + "/" + name + '.gif' )
########################################

###########################
# Execute a shell command #
###########################
def exec_cmd():
    # Pour exécuter une commande bash
    import os

    # Commande à exécuter
    CMD = "sox -t mp3 /home/pi/Documents/RadioPirate/sounds/radioRambo.mp3 -t wav - speed 2.0 | sudo /home/pi/Documents/RadioPirate/PiFmRds/src/pi_fm_rds -freq 87.7 -ps Toto -audio -"

    os.system ( CMD )
############################


#############
# Send Mail #
#############
def sendMail( filename ):

    # Pour envoyer un mail
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.base import MIMEBase
    from email import encoders

    fromaddr = "moi@liliwol.fr"
    toaddr = "test@liliwol.fr"

    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Un test?"
    body = 'Une photo'
    msg.attach(MIMEText(body, 'plain'))

    # Pièce jointe
    attachment = open( filename , "rb")

    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= {}".format(filename))
    msg.attach(part)

    server = smtplib.SMTP('ssl0.ovh.net', 465)
    server.starttls()
    server.login("niko@liliwol.fr", "Ni2nIMaitre")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()
###############################

##################
# Display a Text #
##################
def displayText( text ):
    # Video Resolution
    global VIDEO_HEIGHT
    global VIDEO_WIDTH
    global camera
    global OVERLAY

    import textwrap

    img = Image.new("RGB", (VIDEO_WIDTH, VIDEO_HEIGHT))
    # On passe un objet Image
    #img_obj = Image.open('./images/t.png')
    
    # A l'initialisation on crée un premier OVERLAY
    if (OVERLAY == "FIRST"):        
        OVERLAY = camera.add_overlay(img.tobytes(), layer = 3, alpha = 100)    

    draw = ImageDraw.Draw(img)
    draw.font = ImageFont.truetype("./fonts/SpaceOut.ttf", 70)
    #draw.text((30, 300), text, (255, 255, 0))

    text_color = (255, 255, 0)
    image_width, image_height = img.size
    y_text = 20

    lines = textwrap.wrap(text, width=20)
    for line in lines:
        line_width, line_height = draw.font.getsize(line)
        draw.text(
            ((image_width - line_width) / 2, y_text), 
            line, fill=text_color
            )
        y_text += line_height
    
    # Mise à jour de l'overlay
    if (OVERLAY != "FIRST"):
        OVERLAY.update(img.tobytes())
###############################


##################
# Display a Counter au centre de l'écran #
##################
def displayCounter( count ):
    # Video Resolution
    global VIDEO_HEIGHT
    global VIDEO_WIDTH
    global camera
    global OVERLAY

    import textwrap

    img = Image.new("RGB", (VIDEO_WIDTH, VIDEO_HEIGHT))    
    
    # A l'initialisation on crée un premier OVERLAY
    if (OVERLAY == "FIRST"):        
        OVERLAY = camera.add_overlay(img.tobytes(), layer = 3, alpha = 100)    

    draw = ImageDraw.Draw(img)
    draw.font = ImageFont.truetype("./fonts/SpaceOut.ttf", 100)
    #draw.text((30, 300), text, (255, 255, 0))

    text_color = (255, 255, 0)
    image_width, image_height = img.size
    y_text = 50

    lines = textwrap.wrap(count, width=20)
    for line in lines:
        line_width, line_height = draw.font.getsize(line)
        draw.text(
            ((image_width - line_width) / 2, y_text), 
            line, fill=text_color
            )
        y_text += line_height
    
    # Mise à jour de l'overlay
    if (OVERLAY != "FIRST"):
        OVERLAY.update(img.tobytes())
###############################

# Configuration du GPIO
config_gpio()

# Etat des boutons
OLD_SNAP_BUTTON_STATUS = GPIO.input(BUTTON_SNAP)
OLD_ANIMATION_BUTTON_STATUS = GPIO.input(BUTTON_ANIMATION)

# Configuraton Camera
camera_setup()

# Text on screen
displayText( 'Photo -> Rouge Animation -> Jaune' )

if LEDS_ON:
    blink_led( LED_YELLOW, 10, .1 )

try:
    while 1:
        SNAP_BUTTON_STATUS = GPIO.input( BUTTON_SNAP )
        ANIMATION_BUTTON_STATUS = GPIO.input( BUTTON_ANIMATION )

        # GPIO.output(LED_RED, button_status)
        # print ("Bouton snap status " + str(SNAP_BUTTON_STATUS) )

        # Cas du SNAP
        if OLD_SNAP_BUTTON_STATUS != SNAP_BUTTON_STATUS:

            # Nothing
            if SNAP_BUTTON_STATUS == True:
                print("Snap Button not pressed")
                #displayText( 'Photo -> Rouge Animation -> Jaune' )

                if LEDS_ON:
                    blink_led( LED_RED, 10, .1 )

            # Snap Button
            else:
                print("Snap Button pressed")
                # Lance la commande
                # exec_cmd()

                if LEDS_ON:
                    blink_led( LED_YELLOW, 10, .1 )

                snap()

                # Pour gérer le rebond (bouncing) on ajoute un délai
                time.sleep(.7)

            OLD_SNAP_BUTTON_STATUS=SNAP_BUTTON_STATUS
        
        # Cas de l'ANIM
        if OLD_ANIMATION_BUTTON_STATUS != ANIMATION_BUTTON_STATUS:

            # Nothing
            if ANIMATION_BUTTON_STATUS == True:
                print("Anim Button not pressed")
                #displayText( 'Photo -> Rouge Animation -> Jaune' )

                if LEDS_ON:
                    blink_led( LED_RED, 10, .1 )

            # Anim Button
            else:
                print("Anim Button pressed")
                # Lance la commande
                # exec_cmd()

                if LEDS_ON:
                    blink_led( LED_YELLOW, 10, .1 )

                animation()

                # Pour gérer le rebond (bouncing) on ajoute un délai
                time.sleep(.7)

            OLD_ANIMATION_BUTTON_STATUS=ANIMATION_BUTTON_STATUS

    

except KeyboardInterrupt:
    print ('program stopped')
    GPIO.cleanup()