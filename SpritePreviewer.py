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
        self.frame_label = QLabel()
        self.fps = 1
        self.fps_label = QLabel(str(self.fps))
        # Make the GUI in the setupUI method
        self.setupUI()


    def setupUI(self):
        # An application needs a central widget - often a QFrame
        frame = QFrame()

        # Add a lot of code here to make layouts, more QFrame or QWidgets, and
        # the other components of the program.
        # Create needed connections between the UI components and slot methods you define in this class.
        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        file_menu = menubar.addMenu('&File')
        pause_action = QAction('&Pause', self)
        pause_action.triggered.connect(self.pause)
        file_menu.addAction(pause_action)
        exit_action = QAction('&Exit', self)
        exit_action.triggered.connect(self.quit_program)
        file_menu.addAction(exit_action)

        pixmap = self.frames[0]

        self.frame_label.setPixmap(pixmap)

        application_layout = QVBoxLayout()  # put label in a layout

        animation_frame = QFrame()
        animation_layout = QHBoxLayout()
        animation_frame.setLayout(animation_layout)

        application_layout.addWidget(animation_frame)

        frame.setLayout(application_layout)

        animation_layout.addWidget(self.frame_label)

        slider = QSlider()
        slider.setRange(1, 100)
        slider.setValue(1)
        slider.setTickPosition(QSlider.TickPosition.TicksBothSides)
        slider.setTickInterval(20)
        slider.valueChanged.connect(self.update_fps)
        animation_layout.addWidget(slider)

        text_frame = QFrame()
        text_layout = QVBoxLayout()
        text_frame.setLayout(text_layout)

        fps_frame = QFrame()
        fps_layout = QHBoxLayout()
        fps_frame.setLayout(fps_layout)

        frames_label = QLabel("Frames per second")

        fps_layout.addWidget(frames_label)
        fps_layout.addWidget(self.fps_label)

        start_button = QPushButton("Start")

        text_layout.addWidget(fps_frame)
        text_layout.addWidget(start_button)

        application_layout.addWidget(text_frame)

        self.setCentralWidget(frame)


    # You will need methods in the class to act as slots to connect to signals
    def quit_program(self):
        self.close()

    def pause(self):
        pass

    def update_fps(self, value):
        self.fps = value
        self.fps_label.setText(str(value))
        pass

def main():
    app = QApplication([])
    # Create our custom application
    window = SpritePreview()
    # And show it
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
