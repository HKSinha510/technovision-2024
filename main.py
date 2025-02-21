import sys
import time
from pathlib import Path
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QLabel, 
                           QVBoxLayout, QHBoxLayout, QWidget, QMenu, QMenuBar,
                           QAction, QInputDialog)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl

class CircleButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setFixedSize(100, 100)
        # Fixed stylesheet syntax by removing comments and fixing property values
        self.setStyleSheet("""
            QPushButton {
                background-color: white;
                border-radius: 50px;
                color: black;
                font-weight: bold;
                font-size: 18pt;
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
        self.setWindowTitle('Timer')
        self.setStyleSheet("background-color: black;")
        self.setMinimumSize(800, 600)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(40)
        layout.setContentsMargins(50, 50, 50, 50)
        
        # Fixed menubar stylesheet
        menubar = QMenuBar()
        menubar.setStyleSheet("""
            QMenuBar {
                background-color: black;
                color: white;
                font-size: 24pt;
                padding: 10px;
            }
            QMenuBar::item:selected {
                background-color: #404040;
            }
        """)
        self.setMenuBar(menubar)
        
        # Fixed menu stylesheet
        settings_menu = QMenu('☰', self)
        settings_menu.setStyleSheet("""
            QMenu {
                background-color: black;
                color: white;
                font-size: 20pt;
                padding: 10px;
            }
            QMenu::item {
                padding: 10px 20px;
            }
            QMenu::item:selected {
                background-color: #404040;
            }
        """)
        menubar.addMenu(settings_menu)
        
        set_timer_action = QAction('Set Timer', self)
        set_timer_action.triggered.connect(self.setTimer)
        settings_menu.addAction(set_timer_action)
        
        # Timer display
        self.time_display = QLabel('00:00')
        self.time_display.setAlignment(Qt.AlignCenter)
        self.time_display.setStyleSheet("color: white;")
        self.time_display.setFont(QFont('Arial', 200, QFont.Bold))
        layout.addWidget(self.time_display)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignCenter)
        button_layout.setSpacing(50)
        
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
        
        # Timer setup
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateTimer)
        self.time_remaining = 0
        self.timer_running = False
        
        # Using QMediaPlayer instead of QSound
        self.player = QMediaPlayer()
        sound_file = Path('alarm.wav')
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile(str(sound_file.absolute()))))
        
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
                self.player.play()
                
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