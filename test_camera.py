import picamera

camera = picamera.PiCamera()
#camera.resolution = (1920, 1080) # 16:9
camera.resolution = (2592, 1944) # 4/3


camera.start_preview()


# Effets
camera.brightness = 60

camera.annotate_foreground = picamera.Color (y=0.2,u=0,v=0)
camera.annotate_text = "Truc"



camera.capture('test_camera.jpg')
