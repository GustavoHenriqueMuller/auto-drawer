#====-------------------------------------------------====#
#                         Drawer.
# This file is responsible for generating the contours
# and actually moving the mouse along their points.
#====-------------------------------------------------====#

import main
import functions

import time
import winsound
import cv2 as cv
import numpy as np
from urllib.request import urlopen
import keyboard
from pynput.mouse import Button, Controller
import PySimpleGUI as sg

delay = main.delay
scale = main.scale

mouse = Controller()
image = functions.getImage(main.imagePath)
imageGray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
imageThresholded = []
contours = []

# Getting contours
if main.usesAdaptiveThreshold:
    contours, imageThresholded = functions.generateAdaptiveContours(imageGray, main.adaptiveThresholdMaxValue, main.adaptiveThresholdMethod,
                                                  main.adaptiveThresholdType, main.blockSize, main.c, main.adaptiveThresholdContourApproximationMethod) 
else:
    contours, imageThresholded = functions.generateSimpleContours(imageGray, main.simpleThreshold, main.simpleThresholdMaxValue,
                                                main.simpleThresholdType, main.simpleThresholdContourApproximationMethod)    

# Draw
if not main.preview:
    # Startup
    time.sleep(main.startupTime)
    main.window.minimize()

    # InitX and InitY are the top-left corner of the image
    initX = mouse.position[0]
    initY = mouse.position[1]
    isDrawing = True

    for contour in contours:
        if not isDrawing:
            break

        mouse.release(Button.left)
        time.sleep(delay)

        for index, point in enumerate(contour):
            # Break
            if keyboard.is_pressed("esc"):
                mouse.release(Button.left)
                isDrawing = False
                break
            
            # Next point
            mouse.position = (initX + (point[0][0] * scale), initY + (point[0][1] * scale))
            time.sleep(delay)
            
            # New contour
            if(index == 1):
                mouse.press(Button.left)
                time.sleep(delay)

    mouse.release(Button.left)
    winsound.Beep(440, 1000)

else:
    # Preview
    if main.previewType == "Image":
        cv.drawContours(image, contours, -1, (0,255,0), 2)
        cv.imshow("Image Preview", image) # Shows image + contours

    elif main.previewType == "Threshold":        
        cv.drawContours(imageThresholded, contours, -1, (0,255,0), 2)
        cv.imshow("Threshold Preview", imageThresholded) # Shows thresholded image

    elif main.previewType == "Contours":
        blackimg = np.zeros(image.shape)

        cv.drawContours(blackimg, contours, -1, (0,255,0), 2)
        cv.imshow("Contours Preview", blackimg) # Shows only contours

    cv.waitKey(0)