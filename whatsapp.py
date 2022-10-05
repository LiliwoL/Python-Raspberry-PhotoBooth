#!/usr/bin/env python
import pywhatkit as pwk

try:
    pwk.sendwhatmsg("+33633821119", "Hey", 22, 38)

    print ("Message sent")

except:
    print ("Error")