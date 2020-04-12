# DEPENDENCIES
import drawer
import functions
from globals import *

# LIBRARIES
import PySimpleGUI as sg

# VARIABLES
preview = False
previewType = "" # Image, Threshold or Contours
usesAdaptiveThreshold = False
imagePath = ""
startupTime = 3
delay = 0

# SIMPLE THRESHOLD
simpleThreshold = 0
simpleThresholdMaxValue = 0
simpleThresholdType = ""
simpleThresholdContourApproximationMethod = ""

# ADAPTIVE THRESHOLD
blockSize = 0
c = 0
adaptiveThresholdMaxValue = 0
adaptiveThresholdType = ""
adaptiveThresholdMethod = ""
adaptiveThresholdContourApproximationMethod = ""

# LAYOUT
sg.theme(PROGRAM_THEME)

layout = [ # Row 1
           [sg.Text(TITLE + " v" + str(VERSION), font=STD_HEADER_FONT, size=(PROGRAM_WIDTH,1), justification="center")],
           # Row 2
           [sg.Text("Image URL/Path:", font=STD_FONT), sg.InputText(key="-imagePath-", font=STD_FONT, text_color="blue"), sg.FileBrowse(key="-fileBrowser-", font=STD_FONT, size=(10,1), file_types=(("PNG Files", "*.png"), ("JPG Files", "*.jpg"), ("JPEG Files", "*.jpeg")))],
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

# WINDOW
window = sg.Window(TITLE + " v" + str(VERSION), layout)

# EVENT LOOP
while True:
    event, values = window.read()

    # Quits when the window closes
    if event is None:
        exit()

    # Info Simple Threshold
    elif event == "-infoSimpleThreshold-":
        sg.popup("For every pixel, the Normal Threshold value is applied.\nIf the pixel value is smaller than the threshold,\nit is set to 0, otherwise it is set to [Simple Max Value].", title="Simple Threshold")
    elif event == "-infoDelay-":
        sg.popup("Delay is the time waited between drawing each point.\nThe lower the Delay, the quicker the program will run,\nbut with less details.", title="Delay")
    elif event == "-infoSimpleThresholdMaxValue-":
        sg.popup("Simple Max Value is the value which is assigned to pixel values\nexceeding the simple threshold.", title="Simple Max Value")

    # Info Adaptive Threshold    
    elif event == "-infoBlocksize-":     
        sg.popup("Size of a pixel neighborhood that is used to calculate\na threshold value for the pixel: 3, 5, 7, and so on.", title="Blocksize")
    elif event == "-infoC-":
        sg.popup("Constant subtracted from the mean or weighted mean.\nNormally, it is positive but may be zero or negative as well.", title="C")
    elif event == "-infoAdaptiveThreshold-":
        sg.popup("In simple thresholding, the threshold value is global, i.e., it is same for all the pixels in the image.\nAdaptive thresholding is the method where the threshold value is calculated for smaller regions\nand therefore, there will be different threshold values for different regions.", title="Adaptive Threshold")
    elif event == "-infoAdaptiveThresholdMaxValue-":
        sg.popup("Adaptive Max Value is the value which is assigned to pixel values\nexceeding the adaptive threshold determined by the pixel neighborhood.", title="Adaptive Max Value")

    # Draw or preview drawing
    elif event == "-draw-" or event[:8] == "-preview":
        imagePath = values["-imagePath-"]
        hasErrors, error = functions.checkErrors(values, imagePath)
        if not hasErrors:
            # Drawing or preview
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

            # Minimizes the window
            if not preview:
                window["-error-"].update("Running...")
                window.minimize()
            else:
                window["-error-"].update("Getting image...")

            # Refreshes the window a last time before running
            window.refresh()

            # Executes the program
            exec(open("drawer.py").read())

            # Clears the warning text
            window["-error-"].update("")
        else:
            window["-error-"].update(error) # Print error
