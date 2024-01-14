##### It is advised to run only this file and nothing else!

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from subprocess import Popen, CREATE_NEW_CONSOLE, CREATE_NO_WINDOW
import psutil

class ParkingLotApp(QWidget):
    def __init__(self):
        super().__init__()

        self.processes = []

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Parking Lot Manager')

        # Labels
        self.label = QLabel('Parking Lot', self)
        
        # Buttons
        btn_run_processes = QPushButton('Parking Lot Empty Spaces', self)
        btn_run_processes.setFixedSize(200, 200)
        btn_run_processes.clicked.connect(self.run_processes)


        btn_parking_lot_entrance = QPushButton('Parking Lot Entrance', self)
        btn_parking_lot_entrance.setFixedSize(200, 200)
        btn_parking_lot_entrance.clicked.connect(self.run_parking_lot_entrance)


        btn_crosswalk_light_manager = QPushButton('Crosswalk Light Manager', self)
        btn_crosswalk_light_manager.setFixedSize(200, 200)
        btn_crosswalk_light_manager.clicked.connect(self.run_crosswalk_light_manager)


        btn_close_processes = QPushButton('Close Processes', self)
        btn_close_processes.setFixedSize(200, 200)
        btn_close_processes.clicked.connect(self.close_processes)

        btn_run_processes.setStyleSheet("color: black; background-image: url(parking_lot.jpg)")
        btn_parking_lot_entrance.setStyleSheet("color: white; background-image: url(parking_lot_entrance.jpg)")
        btn_crosswalk_light_manager.setStyleSheet("color: black; background-image: url(crosswalk.jpg)")
        btn_close_processes.setStyleSheet("color: black; background-image: url(red_no_symbol.png)")


        # Layout
        row_layout1 = QHBoxLayout()
        row_layout1.addWidget(btn_run_processes)
        row_layout1.addWidget(btn_parking_lot_entrance)

        row_layout2 = QHBoxLayout()
        row_layout2.addWidget(btn_crosswalk_light_manager)
        row_layout2.addWidget(btn_close_processes)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.label)
        main_layout.addLayout(row_layout1)
        main_layout.addLayout(row_layout2)

        self.setLayout(main_layout)

    def run_processes(self):
        self.processes.append(Popen(["python", "YOLO_Parking_Lot_Space_Detection.py"], creationflags=CREATE_NEW_CONSOLE))
        self.processes.append(Popen(["python", "GUI_parking_lot_manager.py"], creationflags=CREATE_NEW_CONSOLE))

    def run_parking_lot_entrance(self):
        self.processes.append(Popen(["python", "YOLO_License_Plate_Writer.py"], creationflags=CREATE_NEW_CONSOLE | CREATE_NO_WINDOW))
        self.processes.append(Popen(["python", "GUI_parking_lot_manager.py"], creationflags=CREATE_NEW_CONSOLE | CREATE_NO_WINDOW))

    def run_crosswalk_light_manager(self):
        self.processes.append(Popen(["python", "Yolo_Crosswalk_Counter.py"], creationflags=CREATE_NEW_CONSOLE))
        self.processes.append(Popen(["python", "GUI_Traffic_Light_Manager.py"], creationflags=CREATE_NEW_CONSOLE | CREATE_NO_WINDOW))

    def close_processes(self):
        for process in self.processes:
            try:
                parent = psutil.Process(process.pid)
                for child in parent.children(recursive=True):
                    child.terminate()
                parent.terminate()
            except psutil.NoSuchProcess:
                pass
        self.processes = []


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_app = ParkingLotApp()
    main_app.show()

    # aboutToQuit signal to close all processes
    app.aboutToQuit.connect(main_app.close_processes)

    sys.exit(app.exec_())