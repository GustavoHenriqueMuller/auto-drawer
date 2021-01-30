# AutoDrawer
A program made in Python 3.7 that automatically draws an image using OpenCV and Pynput. Made to work with Paint, but it can also work with other drawing tools. The project is being developed in Visual Studio 2019 (Community Edition).

# How to use
<img src="https://github.com/GustavoMuller2019/AutoDrawer/blob/master/examples/interfaceExample.png?raw=true">
<img width="400" height="200" src="https://github.com/GustavoMuller2019/AutoDrawer/blob/master/examples/example.png?raw=true">

* Open CMD in the project folder and run "pip install -r requirements.text" to install all the libraries needed.<br>
* Run "main.py".<br>
* Customize all the drawing parameters.<br>
* Once you're satisfied, click the draw button. After clicking, the program will start drawing in 3 seconds, so make sure you already have Paint opened up beforehand in the background.<br>
* After the 3 seconds, the program will record the position of your mouse. That position will be the top left corner of the image.<br>
* Finally, the program will minimize and will start to simulate mouse presses/movements to draw on the screen.<br>
<br><b>Press [ESC] to stop drawing during runtime.</b>

# Libraries Used
Contour Recognition: OpenCV<br>
Interface: PySimpleGUI<br>
Drawing: Pynput<br>

Other libraries:<br>
Time, Winsound, Numpy, Urrlib, Keyboard

# Learn more
If you don't understand what all of the image parameters are, make sure you read about them at https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_setup/py_intro/py_intro.html#intro.
