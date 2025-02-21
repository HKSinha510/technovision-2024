import sys
import time
from pathlib import Path
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QLabel, 
                           QVBoxLayout, QHBoxLayout, QWidget, QMenu, QMenuBar,
                           QAction, QInputDialog, QDialog, QSpinBox, QFormLayout,
                           QMessageBox)
from PyQt5.QtCore import QTimer, Qt, QUrl
from PyQt5.QtGui import QFont
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent

class TimeInputDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Set Timer')
        self.setStyleSheet("""
            QDialog {
                background-color: black;
            }
            QLabel {
                color: white;
                font-size: 12pt;
            }
            QSpinBox {
                background-color: white;
                color: black;
                font-size: 12pt;
                padding: 5px;
            }
        """)
        
        layout = QFormLayout(self)
        
        self.hours_spin = QSpinBox()
        self.hours_spin.setRange(0, 99)
        self.minutes_spin = QSpinBox()
        self.minutes_spin.setRange(0, 59)
        self.seconds_spin = QSpinBox()
        self.seconds_spin.setRange(0, 59)
        
        layout.addRow('Hours:', self.hours_spin)
        layout.addRow('Minutes:', self.minutes_spin)
        layout.addRow('Seconds:', self.seconds_spin)
        
        buttons = QHBoxLayout()
        ok_button = QPushButton('OK')
        cancel_button = QPushButton('Cancel')
        ok_button.setStyleSheet("background-color: white; color: black; padding: 5px;")
        cancel_button.setStyleSheet("background-color: white; color: black; padding: 5px;")
        
        ok_button.clicked.connect(self.accept)
        cancel_button.clicked.connect(self.reject)
        
        buttons.addWidget(ok_button)
        buttons.addWidget(cancel_button)
        layout.addRow(buttons)

class CircleButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setFixedSize(100, 100)
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
        
        self.time_display = QLabel('00:00:00')
        self.time_display.setAlignment(Qt.AlignCenter)
        self.time_display.setStyleSheet("color: white;")
        self.time_display.setFont(QFont('Arial', 150, QFont.Bold))
        layout.addWidget(self.time_display)
        
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
        
        # Main timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateTimer)
        
        # Color flashing timer
        self.flash_timer = QTimer()
        self.flash_timer.timeout.connect(self.toggleColor)
        self.is_red = False
        
        self.time_remaining = 0
        self.timer_running = False
        self.is_paused = False
        
        # Set up media player for custom sound
        self.player = QMediaPlayer()
        self.setupSound()
        
    def setupSound(self):
        sound_files = ['alarm.mp3', 'alarm.wav', 'alarm.m4a']
        found_sound = False
        
        for sound_file in sound_files:
            file_path = Path(sound_file)
            if file_path.exists():
                self.player.setMedia(QMediaContent(QUrl.fromLocalFile(str(file_path.absolute()))))
                print(f"Found sound file: {sound_file}")
                found_sound = True
                break
        
        if not found_sound:
            print("No sound file found. Please add an alarm.mp3, alarm.wav, or alarm.m4a file.")
            
    def playSound(self):
        if self.player.media().isNull():
            self.setupSound()
        self.player.setPosition(0)
        self.player.play()
    
    def stopSound(self):
        self.player.stop()
        
    def toggleColor(self):
        self.is_red = not self.is_red
        color = "red" if self.is_red else "white"
        self.time_display.setStyleSheet(f"color: {color};")
                
    def setTimer(self):
        dialog = TimeInputDialog(self)
        if dialog.exec_():
            hours = dialog.hours_spin.value()
            minutes = dialog.minutes_spin.value()
            seconds = dialog.seconds_spin.value()
            self.time_remaining = hours * 3600 + minutes * 60 + seconds
            self.updateDisplay()
            self.time_display.setStyleSheet("color: white;")
            self.is_paused = False
            
    def startTimer(self):
        if not self.timer_running and self.time_remaining > 0:
            self.timer.start(1000)
            self.timer_running = True
            self.start_button.setEnabled(False)
            self.pause_button.setEnabled(True)
            self.is_paused = False
            self.time_display.setStyleSheet("color: white;")
            
    def pauseTimer(self):
        if self.timer_running:
            self.timer.stop()
            self.timer_running = False
            self.start_button.setEnabled(True)
            self.is_paused = True
            self.time_display.setStyleSheet("color: red;")
        elif self.time_remaining > 0 and not self.timer_running:
            self.startTimer()
            
    def resetTimer(self):
        # Stop all timers
        self.timer.stop()
        self.flash_timer.stop()
        self.timer_running = False
        self.is_paused = False
        
        # Reset display color
        self.time_display.setStyleSheet("color: white;")
        self.is_red = False
        
        # Stop sound
        self.stopSound()
        
        # Reset time
        self.time_remaining = 0
        self.updateDisplay()
        self.start_button.setEnabled(True)
        self.pause_button.setEnabled(True)
        
    def updateTimer(self):
        if self.time_remaining > 0:
            self.time_remaining -= 1
            self.updateDisplay()
            if self.time_remaining == 0:
                self.timer.stop()
                self.timer_running = False
                self.start_button.setEnabled(True)
                self.playSound()
                # Start color flashing
                self.flash_timer.start(500)  # Toggle every 500ms (half second)
                
    def updateDisplay(self):
        hours = self.time_remaining // 3600
        minutes = (self.time_remaining % 3600) // 60
        seconds = self.time_remaining % 60
        self.time_display.setText(f'{hours:02d}:{minutes:02d}:{seconds:02d}')

def main():
    app = QApplication(sys.argv)
    timer = TimerApp()
    timer.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()