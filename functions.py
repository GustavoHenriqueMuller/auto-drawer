#====-------------------------------------------------====#
#                       Functions.
# This file is responsible for functions useful for
# checking errors in the inputs present in the interface.
#====-------------------------------------------------====#

from globals import *

import cv2 as cv
import numpy as np
from urllib.request import urlopen

# Image Conversion
def pathIsURL(imagePath):
    if imagePath[:4] == "http":
        return True
    else:
        return False

def imagePathIsValid(imagePath):
    # Returns: [True/False, error message]
    if pathIsURL(imagePath):
        try:
            urlopen(imagePath)
            return True, ""
        except Exception as e:
            return False, "Error on opening URL: " + str(e) + "."
    else:
        image = cv.imread(imagePath)
        if image.all() == None:
            return False, "Error on opening local image: File doesn't exist."
        else:
            return True, ""

def getImage(imagePath):
    image = []

    if pathIsURL(imagePath):
        resp = urlopen(imagePath)
        image = np.asarray(bytearray(resp.read()), dtype="uint8")
        image = cv.imdecode(image, cv.IMREAD_COLOR)
    else:
        image = cv.imread(imagePath)
       
    return image

# Error Checking
def valueIsEmpty(values, key):
    if values["-" + key + "-"] == "":
        return True
    else:
        return False

def valueIsNumber(values, key):
    try:
        float(values["-" + key + "-"])
        return True
    except:
        return False

def valueIsEvenNumber(values, key):
    if valueIsNumber(values, key):
        if int(values["-" + key + "-"]) % 2 == 0:
            return True

    return False

def valueIsGreaterThanOne(values, key):
    if valueIsNumber(values, key):
        return int(values["-" + key + "-"]) > 1

def valueAsBoolean(values, key):
    return bool(values["-" + key + "-"])

def checkErrors(values, imagePath):
    errorState = [True, ""] # [0] is True or False, [1] is a string representing the error

    # Image URL/Path
    if valueIsEmpty(values, "imagePath"):
        errorState[1] = "Image URL/Path cannot be empty."

    # Blocksize
    elif valueIsEmpty(values, "blockSize") and valueAsBoolean(values, "adaptiveThreshold"):
        errorState[1] = "Blocksize cannot be empty."
    elif not valueIsNumber(values, "blockSize") and valueAsBoolean(values, "adaptiveThreshold"):
        errorState[1] = "Blocksize needs to be a number."
    elif valueIsEvenNumber(values, "blockSize") and valueAsBoolean(values, "adaptiveThreshold"):        
        errorState[1] = "Blocksize must be an odd number."
    elif not valueIsGreaterThanOne(values, "blockSize") and valueAsBoolean(values, "adaptiveThreshold"):        
        errorState[1] = "Blocksize must be greater than one."

    # C
    elif valueIsEmpty(values, "c") and valueAsBoolean(values, "adaptiveThreshold"):
        errorState[1] = "C property cannot be empty."
    elif not valueIsNumber(values, "c") and valueAsBoolean(values, "adaptiveThreshold"):
        errorState[1] = "C needs to be a number."

    # Simple Threshold
    elif valueIsEmpty(values, "simpleThreshold") and not valueAsBoolean(values, "adaptiveThreshold"):
        errorState[1] = "Simple Threshold property cannot be empty."
    elif not valueIsNumber(values, "simpleThreshold") and not valueAsBoolean(values, "adaptiveThreshold"):
        errorState[1] = "Simple Threshold needs to be a number."

    # Simple Threshold Max Value
    elif valueIsEmpty(values, "simpleThresholdMaxValue") and not valueAsBoolean(values, "adaptiveThreshold"):
        errorState[1] = "Simple Threshold Max Value property cannot be empty."
    elif not valueIsNumber(values, "simpleThreshold") and not valueAsBoolean(values, "adaptiveThreshold"):
        errorState[1] = "Simple Threshold Max Value needs to be a number."

    # Adaptive Threshold Max Value
    elif valueIsEmpty(values, "adaptiveThresholdMaxValue") and valueAsBoolean(values, "adaptiveThreshold"):
        errorState[1] = "Adaptive Threshold Max Value property cannot be empty."
    elif not valueIsNumber(values, "adaptiveThreshold") and valueAsBoolean(values, "adaptiveThreshold"):
        errorState[1] = "Adaptive Threshold Max Value needs to be a number."

    # Delay
    elif valueIsEmpty(values, "delay"):
        errorState[1] = "Delay property cannot be empty."
    elif not valueIsNumber(values, "simpleThreshold"):
        errorState[1] = "Delay needs to be a number."

    # If path is not valid
    pathIsValid, imageErrorMessage = imagePathIsValid(imagePath)

    if not pathIsValid:
        errorState[1] = imageErrorMessage

    # No errors
    else:
        errorState = [False, ""]

    return errorState

# Contour generation
def generateSimpleContours(imageGray, threshold, maxValue, type, approxMethod):
    thresholdAmount, imageThresholdedNormal = cv.threshold(imageGray, threshold, maxValue, THRESHOLD_TYPES[type])
    contours = cv.findContours(imageThresholdedNormal, cv.RETR_LIST, THRESHOLD_CONTOUR_APPROX_METHODS[approxMethod])[0]
    return contours, imageThresholdedNormal

def generateAdaptiveContours(imageGray, maxValue, adaptiveMethod, type, blockSize, c, approxMethod):
    imageThresholdedAdaptive = cv.adaptiveThreshold(imageGray, maxValue, ADAPTIVE_THRESHOLD_METHODS[adaptiveMethod], THRESHOLD_TYPES[type], blockSize, c)
    contours = cv.findContours(imageThresholdedAdaptive, cv.RETR_LIST, THRESHOLD_CONTOUR_APPROX_METHODS[approxMethod])[0]
    return contours, imageThresholdedAdaptive