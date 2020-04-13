import cv2 as cv

# GLOBAL VARIABLES
TITLE = "AutoDrawer"
VERSION = 1.3

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
