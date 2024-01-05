import csv
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setGeometry(100, 100, 800, 800)
        self.label = QLabel(self)
        self.current_pixmap = 'red_light.png'
        self.label.setPixmap(QPixmap(self.current_pixmap))
        self.label.setGeometry(0, 0, 800, 800)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(1000)  # Check every second
        self.switched_from_yellow = False

    def update(self):
        with open('people_in_polygon.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if int(row[1]) > 15 and self.current_pixmap == 'red_light.png' and not self.switched_from_yellow:
                    self.current_pixmap = 'yellow_light.png'
                    self.label.setPixmap(QPixmap(self.current_pixmap))
                    QTimer.singleShot(3000, self.switch_to_green)

    def switch_to_green(self):
        self.current_pixmap = 'green_light.png'
        self.label.setPixmap(QPixmap(self.current_pixmap))
        green_time = 20000 # 20 seconds
        QTimer.singleShot(green_time, self.switch_to_yellow)

    def switch_to_yellow(self):
        self.current_pixmap = 'yellow_light.png'
        self.label.setPixmap(QPixmap(self.current_pixmap))
        QTimer.singleShot(2000, self.switch_to_red)

    def switch_to_red(self):
        self.current_pixmap = 'red_light.png'
        self.label.setPixmap(QPixmap(self.current_pixmap))
        self.switched_from_yellow = True
        QTimer.singleShot(10000, self.reset_flag) # To make sure we don't switch to green too early

    def reset_flag(self):
        self.switched_from_yellow = False

app = QApplication([])
window = MainWindow()
window.show()
app.exec_()
