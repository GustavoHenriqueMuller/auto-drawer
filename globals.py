#====-------------------------------------------------====#
#              Global variables (constants).
#====-------------------------------------------------====#
import cv2 as cv

TITLE = "AutoDrawer"
PROGRAM_THEME = "Reddit"
STD_FONT = ("Helvetica", 12)
STD_HEADER_FONT = ("Helvetica", 17, "bold")
INFO_BUTTON_COLOR = "#d6af4d"
PROGRAM_WIDTH = 52

THRESHOLD_TYPES = {"Binary": cv.THRESH_BINARY,
                   "Binary Inverted": cv.THRESH_BINARY_INV,
                   "Truncated": cv.THRESH_TRUNC,
                   "To Zero": cv.THRESH_TOZERO,
                   "To Zero Inverted": cv.THRESH_TOZERO_INV}
THRESHOLD_CONTOUR_APPROX_METHODS = {"None": cv.CHAIN_APPROX_NONE,
                                    "Simple": cv.CHAIN_APPROX_SIMPLE,
                                    "TC89_L1": cv.CHAIN_APPROX_TC89_L1,
                                    "TC89_KCOS": cv.CHAIN_APPROX_TC89_KCOS}
ADAPTIVE_THRESHOLD_METHODS = {"Mean C": cv.ADAPTIVE_THRESH_MEAN_C,
                              "Gaussian C": cv.ADAPTIVE_THRESH_GAUSSIAN_C}

INFO_WINDOW_NAME = {"infoSimpleThreshold": "Simple Threshold",
                    "infoDelay": "Delay",
                    "infoSimpleThresholdMaxValue": "Simple max value",
                    "infoBlocksize": "Blocksize",
                    "infoC": "C",
                    "infoAdaptiveThreshold": "Adaptative Threshold",
                    "infoAdaptiveThresholdMaxValue": "Adaptive max value"}

INFO_DESCRIPTION = {"infoSimpleThreshold": "For every pixel, the Normal Threshold value is applied.\nIf the pixel value is smaller than the threshold,\nit is set to 0, otherwise it is set to [Simple Max Value]",
                    "infoDelay": "Delay is the time waited between drawing each point.\nThe lower the Delay, the quicker the program will run,\nbut with less details.",
                    "infoSimpleThresholdMaxValue": "Simple Max Value is the value which is assigned to pixel values\nexceeding the simple threshold.",
                    "infoBlocksize": "Size of a pixel neighborhood that is used to calculate\na threshold value for the pixel: 3, 5, 7, and so on",
                    "infoC": "Constant subtracted from the mean or weighted mean.\nNormally, it is positive but may be zero or negative as well.",
                    "infoAdaptiveThreshold": "In simple thresholding, the threshold value is global, i.e., it is same for all the pixels in the image.\nAdaptive thresholding is the method where the threshold value is calculated for smaller regions\nand therefore, there will be different threshold values for different regions.",
                    "infoAdaptiveThresholdMaxValue": "Adaptive Max Value is the value which is assigned to pixel values\nexceeding the adaptive threshold determined by the pixel neighborhood."}