#====-------------------------------------------------------------------------====#
# MIT License

# Copyright (c) 2020 GustavoMuller2019

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#====-------------------------------------------------------------------------====#

import drawer
import functions
from globals import *

import PySimpleGUI as sg

preview = False
previewType = "" # Image, Threshold or Contours
usesAdaptiveThreshold = False
imagePath = ""
startupTime = 3 # Seconds
delay = 0 # Seconds

simpleThreshold = 0
simpleThresholdMaxValue = 0
simpleThresholdType = ""
simpleThresholdContourApproximationMethod = ""

blockSize = 0
c = 0
adaptiveThresholdMaxValue = 0
adaptiveThresholdType = ""
adaptiveThresholdMethod = ""
adaptiveThresholdContourApproximationMethod = ""

sg.theme(PROGRAM_THEME)
layout = [ # Row 1
           [sg.Text(TITLE, font=STD_HEADER_FONT, size=(PROGRAM_WIDTH,1), justification="center")],
           # Row 2
           [sg.Text("Image URL/Path:", font=STD_FONT), sg.InputText(key="-imagePath-", font=STD_FONT, text_color="blue"), sg.FileBrowse(key="-fileBrowser-", font=STD_FONT, size=(10,1), file_types=(("All Files", "*"), ("PNG Files", "*.png"), ("JPG Files", "*.jpg"), ("JPEG Files", "*.jpeg")))],
           # Row 3
           [sg.Text("_" * PROGRAM_WIDTH * 2)],
           # Row 4
           [sg.Text("Simple Threshold Type:", font=STD_FONT), sg.InputOptionMenu(key="-simpleThresholdType-", values=list(THRESHOLD_TYPES.keys()), default_value=list(THRESHOLD_TYPES.keys())[0]),
            sg.Text("Simple Threshold:", font=STD_FONT), sg.InputText("127", key="-simpleThreshold-", font=STD_FONT, size=(4,1)), sg.Button("?", key="-infoSimpleThreshold-", size=(2,1), button_color=("white", INFO_BUTTON_COLOR)),
            sg.Text("Delay:", font=STD_FONT), sg.InputText("0.0075", key="-delay-", font=STD_FONT, size=(7,1)), sg.Button("?", key="-infoDelay-", size=(2,1), button_color=("white", INFO_BUTTON_COLOR))],
           # Row 5
           [sg.Text("Simple Contour Approximation Method:", font=STD_FONT), sg.InputOptionMenu(key="-simpleThresholdContourApproximationMethod-", values=list(THRESHOLD_CONTOUR_APPROX_METHODS.keys()), default_value=list(THRESHOLD_CONTOUR_APPROX_METHODS.keys())[0]),
            sg.Text("Simple Max Value:", font=STD_FONT), sg.InputText("255", key="-simpleThresholdMaxValue-", font=STD_FONT, size=(4,1)),
            sg.Button("?", key="-infoSimpleThresholdMaxValue-", size=(2,1), button_color=("white", INFO_BUTTON_COLOR))],
           # Row 6
           [sg.Text("_" * PROGRAM_WIDTH * 2)],
           # Row 7
           [sg.Checkbox("Use adaptive threshold instead of simple", key="-adaptiveThreshold-", font=STD_FONT),
            sg.Button("?", key="-infoAdaptiveThreshold-", size=(2,1), button_color=("white", INFO_BUTTON_COLOR)),
            sg.Text("Blocksize:", font=STD_FONT), sg.InputText("11", key="-blockSize-", font=STD_FONT, size=(3,1)), sg.Button("?", key="-infoBlocksize-", size=(2,1), button_color=("white", INFO_BUTTON_COLOR)),
            sg.Text("C:", font=STD_FONT), sg.InputText("2", key="-c-", font=STD_FONT, size=(3,1)), sg.Button("?", key="-infoC-", size=(2,1), button_color=("white", INFO_BUTTON_COLOR))],
           # Row 8
           [sg.Text("Adaptive Threshold Type:", font=STD_FONT), sg.InputOptionMenu(key="-adaptiveThresholdType-", values=list(THRESHOLD_TYPES.keys())[0:2], default_value=list(THRESHOLD_TYPES.keys())[0]),
            sg.Text("Adaptive Max Value:", font=STD_FONT), sg.InputText("255", key="-adaptiveThresholdMaxValue-", font=STD_FONT, size=(4,1)), sg.Button("?", key="-infoAdaptiveThresholdMaxValue-", size=(2,1), button_color=("white", INFO_BUTTON_COLOR))],
           # Row 9
           [sg.Text("Adaptive Contour Approximation Method:", font=STD_FONT), sg.InputOptionMenu(key="-adaptiveThresholdContourApproximationMethod-", values=list(THRESHOLD_CONTOUR_APPROX_METHODS.keys()), default_value=list(THRESHOLD_CONTOUR_APPROX_METHODS.keys())[0]),
            sg.Text("Adaptive Threshold Method:", font=STD_FONT), sg.InputOptionMenu(key="-adaptiveThresholdMethod-", values=list(ADAPTIVE_THRESHOLD_METHODS.keys()), default_value=list(ADAPTIVE_THRESHOLD_METHODS.keys())[0])],
           # Row 10
           [sg.Text("_" * PROGRAM_WIDTH * 2)],
           # Row 11
           [sg.Button("Draw", key="-draw-", font=STD_FONT, size=(10,1)),
            sg.Button("Preview (Image)", key="-previewImage-", font=STD_FONT, size=(21,1)),
            sg.Button("Preview (Threshold)", key="-previewThreshold-", font=STD_FONT, size=(21,1)),
            sg.Button("Preview (Contours)", key="-previewContours-", font=STD_FONT, size=(21,1))],
           # Row 12
           [sg.Text("", key="-error-", font=STD_FONT, size=(PROGRAM_WIDTH,1), text_color="red", pad=((0, 0),(15,0)))],
           [sg.Text("_" * PROGRAM_WIDTH * 2)]]

# Loop and Window
window = sg.Window(TITLE, layout)
while True:
    event, values = window.read()

    # Quit
    if event is None:
        exit()

    # Info
    elif event[:5] == "-info":
        event = event[1:]; event = event[:-1]
        sg.popup(INFO_DESCRIPTION[event], title=INFO_WINDOW_NAME[event])

    # Draw or Preview
    elif event == "-draw-" or event[:8] == "-preview":
        imagePath = values["-imagePath-"]
        hasErrors, error = functions.checkErrors(values, imagePath)

        if not hasErrors:
            if event == "-draw-":
                preview = False
            else:
                preview = True
                previewType = event.replace("-", "")
                previewType = previewType.replace("preview", "")

            # Simple Threshold
            delay = float(values["-delay-"])
            simpleThreshold = int(values["-simpleThreshold-"]) 
            simpleThresholdMaxValue = int(values["-simpleThresholdMaxValue-"])
            simpleThresholdType = values["-simpleThresholdType-"]
            simpleThresholdContourApproximationMethod = values["-simpleThresholdContourApproximationMethod-"]

            # Adaptive Threshold
            usesAdaptiveThreshold = bool(values["-adaptiveThreshold-"])
            if usesAdaptiveThreshold:
                blockSize = int(values["-blockSize-"])
                c = int(values["-c-"])
                adaptiveThresholdMaxValue = int(values["-adaptiveThresholdMaxValue-"])
                adaptiveThresholdType = values["-adaptiveThresholdType-"]
                adaptiveThresholdMethod = values["-adaptiveThresholdMethod-"]
                adaptiveThresholdContourApproximationMethod = values["-adaptiveThresholdContourApproximationMethod-"]

            # Minimize
            if not preview:
                window["-error-"].update("Running...")
                window.minimize()
            else:
                window["-error-"].update("Getting image...")

            window.refresh()
            exec(open("drawer.py").read())
            window["-error-"].update("")
        else:
            window["-error-"].update(error)
