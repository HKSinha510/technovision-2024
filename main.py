import sys
import time
from pathlib import Path
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QLabel, 
                           QVBoxLayout, QHBoxLayout, QWidget, QMenu, QMenuBar,
                           QAction, QInputDialog)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont, QPainter
from PyQt5.QtMultimedia import QSound

class CircleButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setFixedSize(60, 60)
        self.setStyleSheet("""
            QPushButton {
                background-color: white;
                border-radius: 30px;
                color: black;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """)

class TimerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        # Set window properties
        self.setWindowTitle('Timer')
        self.setStyleSheet("background-color: black;")
        self.setMinimumSize(400, 300)
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Create menu bar
        menubar = QMenuBar()
        menubar.setStyleSheet("""
            QMenuBar {
                background-color: black;
                color: white;
            }
            QMenuBar::item:selected {
                background-color: #404040;
            }
        """)
        self.setMenuBar(menubar)
        
        # Create settings menu
        settings_menu = QMenu('☰', self)
        settings_menu.setStyleSheet("""
            QMenu {
                background-color: black;
                color: white;
            }
            QMenu::item:selected {
                background-color: #404040;
            }
        """)
        menubar.addMenu(settings_menu)
        
        # Add set timer action
        set_timer_action = QAction('Set Timer', self)
        set_timer_action.triggered.connect(self.setTimer)
        settings_menu.addAction(set_timer_action)
        
        # Create timer display
        self.time_display = QLabel('00:00')
        self.time_display.setAlignment(Qt.AlignCenter)
        self.time_display.setStyleSheet("color: white;")
        self.time_display.setFont(QFont('Arial', 72))
        layout.addWidget(self.time_display)
        
        # Create button layout
        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignCenter)
        
        # Create control buttons
        self.start_button = CircleButton('Start')
        self.pause_button = CircleButton('Pause')
        self.reset_button = CircleButton('Reset')
        
        self.start_button.clicked.connect(self.startTimer)
        self.pause_button.clicked.connect(self.pauseTimer)
        self.reset_button.clicked.connect(self.resetTimer)
        
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.pause_button)
        button_layout.addWidget(self.reset_button)
        
        layout.addLayout(button_layout)
        
        # Initialize timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateTimer)
        self.time_remaining = 0
        self.timer_running = False
        
        # Set up sound
        sound_file = Path('alarm.wav')  # Make sure to have this file in the same directory
        self.alarm_sound = QSound(str(sound_file))
        
    def setTimer(self):
        minutes, ok = QInputDialog.getInt(self, 'Set Timer', 
                                        'Enter minutes:', min=0)
        if ok:
            self.time_remaining = minutes * 60
            self.updateDisplay()
            
    def startTimer(self):
        if not self.timer_running and self.time_remaining > 0:
            self.timer.start(1000)
            self.timer_running = True
            self.start_button.setEnabled(False)
            
    def pauseTimer(self):
        if self.timer_running:
            self.timer.stop()
            self.timer_running = False
            self.start_button.setEnabled(True)
            
    def resetTimer(self):
        self.timer.stop()
        self.timer_running = False
        self.time_remaining = 0
        self.updateDisplay()
        self.start_button.setEnabled(True)
        
    def updateTimer(self):
        if self.time_remaining > 0:
            self.time_remaining -= 1
            self.updateDisplay()
            if self.time_remaining == 0:
                self.timer.stop()
                self.timer_running = False
                self.start_button.setEnabled(True)
                self.alarm_sound.play()
                
    def updateDisplay(self):
        minutes = self.time_remaining // 60
        seconds = self.time_remaining % 60
        self.time_display.setText(f'{minutes:02d}:{seconds:02d}')

def main():
    app = QApplication(sys.argv)
    timer = TimerApp()
    timer.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()