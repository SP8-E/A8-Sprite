#https://github.com/SP8-E/A8-Sprite

import math

from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *

# This function loads a series of sprite images stored in a folder with a
# consistent naming pattern: sprite_# or sprite_##. It returns a list of the images.
def load_sprite(sprite_folder_name, number_of_frames):
    frames = []
    padding = math.ceil(math.log(number_of_frames - 1, 10))
    for frame in range(number_of_frames):
        folder_and_file_name = sprite_folder_name + "/sprite_" + str(frame).rjust(padding, '0') + ".png"
        frames.append(QPixmap(folder_and_file_name))
    return frames

class SpritePreview(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sprite Animation Preview")
        # This loads the provided sprite and would need to be changed for your own.
        self.num_frames = 21
        self.frames = load_sprite('spriteImages',self.num_frames)
        # Add any other instance variables needed to track information as the program runs here
        self.frame_label = QLabel()                         #label to put image pixmap on
        self.fps = 1                                        #set default fps of 1 with slider at 1
        self.fps_label = QLabel(str(self.fps))              #display current fps count on label
        self.frame_index = 0                                #frame counter for animation cycle
        self.pixmap = self.frames[self.frame_index]         #set pixmap to current sprite image
        self.start_button = QPushButton("Start")            #create Start/Stop button to keep track of text
        self.timer = QTimer()                               #create timer with delay between frames in ms
        self.delay = int(1000/self.fps)
        # Make the GUI in the setupUI method
        self.setupUI()


    def setupUI(self):
        # An application needs a central widget - often a QFrame
        frame = QFrame()
        # Add a lot of code here to make layouts, more QFrame or QWidgets, and
        # the other components of the program.
        # Create needed connections between the UI components and slot methods you define in this class.
        menubar = self.menuBar()                                    #create menu
        menubar.setNativeMenuBar(False)
        file_menu = menubar.addMenu('&File')                        #call menu File, put options inside
        pause_action = QAction('&Pause', self)              #create Pause option
        pause_action.triggered.connect(self.pause)                  #clicking Pause option runs pause function
        file_menu.addAction(pause_action)                           #put Pause option in menu
        exit_action = QAction('&Exit', self)
        exit_action.triggered.connect(self.quit_program)            #clicking Exit option closes program
        file_menu.addAction(exit_action)

        application_layout = QVBoxLayout()                          #overall app layout is vertical
        frame.setLayout(application_layout)

        animation_frame = QFrame()                                  #layout of animation and slider is horizontal
        animation_layout = QHBoxLayout()
        animation_frame.setLayout(animation_layout)

        self.frame_label.setPixmap(self.pixmap)                     #put sprite pixamp on label
        animation_layout.addWidget(self.frame_label)                #add the animation widget

        application_layout.addWidget(animation_frame)               #put the top layout within the app layout

        slider = QSlider()
        slider.setRange(1, 100)
        slider.setValue(1)                                          #create fps control slider
        slider.setTickPosition(QSlider.TickPosition.TicksBothSides)
        slider.setTickInterval(20)                                  #add tick marks for reference points
        slider.valueChanged.connect(self.update_fps)                #change the fps when the slider is moved
        animation_layout.addWidget(slider)                          #add the slider to the layout

        control_frame = QFrame()
        control_layout = QVBoxLayout()
        control_frame.setLayout(control_layout)          #vertical layout for fps message and start/stop button

        fps_frame = QFrame()
        fps_layout = QHBoxLayout()
        fps_frame.setLayout(fps_layout)                  #horizontal layout to separate text from fps number

        frames_label = QLabel("Frames per second")

        fps_layout.addWidget(frames_label)
        fps_layout.addWidget(self.fps_label)                        #add message with fps count

        control_layout.addWidget(fps_frame)
        control_layout.addWidget(self.start_button)                     #add start/stop button
        self.start_button.clicked.connect(self.start_stop_animation)    #start/stop button controls animation

        application_layout.addWidget(control_frame)                 #add button and message to app layout

        self.setCentralWidget(frame)                                #create final UI layout design

    # You will need methods in the class to act as slots to connect to signals
    def quit_program(self):
        self.close()

    def pause(self):
        self.start_button.setText("Start")                          #set button text back to Start
        self.timer.timeout.disconnect(self.switch_image)            #stop the animation from changing frames

    def update_fps(self, value):
        self.fps = value                                            #set fps to current slider value
        self.fps_label.setText(str(value))                          #update the fps count message
        self.delay = int(1000/value)
        self.timer.setInterval(self.delay)                          #set new timer delay in ms

    def start_stop_animation(self):
        if self.start_button.text() == "Start":
            self.start_button.setText("Stop")                       #if Start clicked, make Stop option available
            self.timer.timeout.connect(self.switch_image)           #animate when start is clicked/active
            self.timer.start(self.delay)                            #change the frame based on the timer
        else:
            self.pause()                                            #when stop clicked, run pause function

    def switch_image(self):
        self.pixmap = self.frames[self.frame_index % self.num_frames]       #update pixmap, allowed to loop over frame count with modulus
        self.frame_label.setPixmap(self.pixmap)                             #put new image on label
        self.repaint()                                                      #update UI screen with new frame
        self.frame_index += 1                                               #increment frame counter


def main():
    app = QApplication([])
    # Create our custom application
    window = SpritePreview()
    # And show it
    window.show()
    app.exec()

if __name__ == "__main__":
    main()
