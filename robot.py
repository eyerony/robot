from sr.robot3 import *

import time

R = Robot(verbose = True)

##def UpdateMovement(mode):
##    if mode == "NONE":
##        R.motor_boards["SR0GBT"].motors[0].power = 0
##        R.motor_boards["SR0NCJ"].motors[0].power = 0
##    elif mode == "FORLEFT":
##        R.motor_boards["SR0GBT"].motors[0].power = 0
##        R.motor_boards["SR0NCJ"].motors[0].power = 0.5
##    elif mode == "FORRIGHT":
##        R.motor_boards["SR0GBT"].motors[0].power = -0.5
##        R.motor_boards["SR0NCJ"].motors[0].power = 0
##    elif mode == "FORWARD":
##        R.motor_boards["SR0GBT"].motors[0].power = -0.5
##        R.motor_boards["SR0NCJ"].motors[0].power = 0.5
##    elif mode == "BACKLEFT":
##        R.motor_boards["SR0GBT"].motors[0].power = 0
##        R.motor_boards["SR0NCJ"].motors[0].power = -0.5
##    elif mode == "BACKRIGHT":
##        R.motor_boards["SR0GBT"].motors[0].power = 0.5
##        R.motor_boards["SR0NCJ"].motors[0].power = 0
##    elif mode == "BACKWARD":
##        R.motor_boards["SR0GBT"].motors[0].power = 0.5
##        R.motor_boards["SR0NCJ"].motors[0].power = -0.5
##    elif mode == "LEFT":
##        R.motor_boards["SR0GBT"].motors[0].power = 0.25
##        R.motor_boards["SR0NCJ"].motors[0].power = 0.25
##    else:
##        R.motor_boards["SR0GBT"].motors[0].power = -0.25
##        R.motor_boards["SR0NCJ"].motors[0].power = -0.25

def UpdateMovement2(speed1, speed2):
    if speed1 >= speed2:
        turningRight = True
    else:
        turningRight = False
    R.motor_boards["SR0GBT"].motors[0].power = -speed1
    R.motor_boards["SR0NCJ"].motors[0].power = speed2

def AlteredSigmoid(x):
    return 1 / (1 + exp(2 - x / 160)) - 0.5

def Search():
    print("Searching...")
    if turningRight:
        UpdateMovement2(-0.1, 0.1)
    else:
        UpdateMovement2(0.1, -0.1)
    while True:
        time.sleep(0.1)
        if 0 in R.camera.see_ids():
            return R.camera.see()

def Coast():
    print("Coasting...")
    R.motor_boards["SR0GBT"].motors[0].power = COAST
    R.motor_boards["SR0NCJ"].motors[0].power = COAST

##for i in range(100):
##    markers = R.camera.see()
##    updateMode = "NONE"
##    for marker in markers:
##        if marker.id == 0:
##            if marker.distance > 1.5:
##                if marker.pixel_centre.x < 280:
##                    updateMode = "FORLEFT"
##                elif marker.pixel_centre.x > 360:
##                    updateMode = "FORRIGHT"
##                else:
##                    updateMode = "FORWARD"
##            elif marker.distance < 1:
##                if marker.pixel_centre.x < 240:
##                    updateMode = "BACKRIGHT"
##                elif marker.pixel_centre.x > 400:
##                    updateMode = "BACKLEFT"
##                else:
##                    updateMode = "BACKWARD"
##            else:
##                if marker.pixel_centre.x < 280:
##                    updateMode = "RIGHT"
##                elif marker.pixel_centre.x > 360:
##                    updateMode = "LEFT"
##                else:
##                    updateMode = "NONE"
##    UpdateMovement(updateMode)
##    time.sleep(0.1)

markerFound = True
blindCount = 0
turningRight = True

for i in range(100):
    if markerFound:
        markers = R.camera.see()
    markerFound = False
    for marker in markers:
        if marker.id == 0:
            markerFound = True
            blindCount = 0
            s = AlteredSigmoid(marker.pixel_centre.x)
            speed = min(marker.distance - 1, 1)
            print(s, ",   " speed)
            if speed ^ 2 < 0.01:
                speed = 0
            UpdateMovement2(speed / 2 + s / max(marker.distance, 1), speed / 2 - s / max(marker.distance, 1))
    if not markerFound:
        blindCount += 1
        if blindCount >= 3:
            blindCount = 0
            markers = Search()
            continue
        else:
            markerFound = True
            Coast()
    time.sleep(0.1)
