# DEPENDENCIES
import main
import functions

# LIBRARIES
import time
import winsound
import cv2 as cv
import numpy as np
from urllib.request import urlopen
from skimage import io
import keyboard
from pynput.mouse import Button, Controller
import PySimpleGUI as sg

# VARIABLES
mouse = Controller()
delay = main.delay
image = functions.getImage(main.imagePath)
imageGray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
imageThresholded = []
contours = []

# CONTOURS
if not main.usesAdaptiveThreshold:
    # SIMPLE
    contours, imageThresholded = functions.generateSimpleContours(imageGray, main.simpleThreshold, main.simpleThresholdMaxValue,
                                                main.simpleThresholdType, main.simpleThresholdContourApproximationMethod) 
else:
    # ADAPTIVE
    contours, imageThresholded = functions.generateAdaptiveContours(imageGray, main.adaptiveThresholdMaxValue, main.adaptiveThresholdMethod,
                                                  main.adaptiveThresholdType, main.blockSize, main.c, main.adaptiveThresholdContourApproximationMethod) 

# DRAWS ON SCREEN
if not main.preview:
    # STARTUP
    time.sleep(main.startupTime)
    main.window.minimize()

    # INITX AND INITY WILL BE THE TOP LEFT CORNER OF THE IMAGE
    initX = mouse.position[0]
    initY = mouse.position[1]
    isDrawing = True

    # DRAWS ALL POINTS
    for contour in contours:
        if not isDrawing:
            break

        mouse.release(Button.left)
        time.sleep(delay)

        for index, point in enumerate(contour):
            # BREAKS EXECUTION
            if keyboard.is_pressed("esc"):
                mouse.release(Button.left)
                isDrawing = False
                break
            
            # MOVES THE MOUSE TO THE NEXT POINT
            mouse.position = (initX + point[0][0], initY + point[0][1])
            time.sleep(delay)
            
            # STARTS DRAWING ON A NEW CONTOUR
            if(index == 1):
                mouse.press(Button.left)
                time.sleep(delay)

    # DONE
    mouse.release(Button.left)
    winsound.Beep(440, 1000)

else:
    # PREVIEWS
    if main.previewType == "Image":
        # SHOWS IMAGE + CONTOURS
        cv.drawContours(image, contours, -1, (0,255,0), 2)
        cv.imshow("Image Preview", image)
    elif main.previewType == "Threshold":
        # SHOWS THRESHOLDED IMAGE
        cv.drawContours(imageThresholded, contours, -1, (0,255,0), 2)
        cv.imshow("Threshold Preview", imageThresholded)
    elif main.previewType == "Contours":
        # SHOWS ONLY CONTOURS
        blackimg = np.zeros(image.shape)

        cv.drawContours(blackimg, contours, -1, (0,255,0), 2)
        cv.imshow("Contours Preview", blackimg)

    cv.waitKey(0)