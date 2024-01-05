import sys
import csv
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QListWidget, QListWidgetItem, QPushButton, QHBoxLayout, QStackedWidget
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QColor
from datetime import datetime



class MyApp(QWidget):
    def __init__(self):
        super().__init__()

        # Set up the main window
        self.setGeometry(100, 100, 600, 600)
        self.setWindowTitle('Parking Lot Manager')

        # Create a vertical layout
        main_layout = QVBoxLayout(self)

        # Create buttons for switching between screens
        button_layout = QHBoxLayout()

        self.entry_management_button = QPushButton('Entry Management', self)
        self.entry_management_button.clicked.connect(self.show_entry_management)
        button_layout.addWidget(self.entry_management_button)

        self.empty_space_management_button = QPushButton('Empty Space Management', self)
        self.empty_space_management_button.clicked.connect(self.show_empty_space_management)
        button_layout.addWidget(self.empty_space_management_button)

        main_layout.addLayout(button_layout)

        # Create a stacked widget to hold different screens
        self.stacked_widget = QStackedWidget(self)
        main_layout.addWidget(self.stacked_widget)

        # Create the Entry Management screen
        self.entry_management_screen = QWidget()
        self.setup_entry_management_screen()
        self.stacked_widget.addWidget(self.entry_management_screen)

        # Create the Empty Space Management screen
        self.empty_space_management_screen = QWidget()
        self.setup_empty_space_management_screen()
        self.stacked_widget.addWidget(self.empty_space_management_screen)

        # Set up a QTimer to refresh CSV data every 10 milliseconds
        self.csv_refresh_timer = QTimer(self)
        self.csv_refresh_timer.timeout.connect(self.update_csv_data)
        self.csv_refresh_timer.start(10)

        # Show the GUI
        self.show()

    def setup_entry_management_screen(self):
        # Load data from the CSV file
        data = self.load_csv_data('license_plates.csv')

        # Create a vertical layout for the Entry Management screen
        layout = QVBoxLayout(self.entry_management_screen)

        # Create a QListWidget to display the data
        list_widget = QListWidget(self.entry_management_screen)
        layout.addWidget(list_widget)

        # Populate the QListWidget with data
        for car_id, (license_number, score) in data.items():
            item_text = f"Car ID: {car_id}, License Number: {license_number}, Score: {score}"
            list_widget.addItem(item_text)

    def load_csv_data(self, filename):
        data = {}
        try:
            with open(filename, 'r') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    car_id = row['car_id']
                    license_number = row['license_number']
                    score = float(row['license_number_score'])

                    if car_id not in data or score > data[car_id][1]:
                        data[car_id] = (license_number, score)
        except Exception as e:
            print(f"Error loading CSV file: {e}")

        for i in range(3):
            if str(i) not in data:
                data[str(i)] = ('0', 0.0)

        return data

    def setup_empty_space_management_screen(self):
        # Load data from the "empty_spaces.txt" file
        empty_space_data = self.load_empty_space_data('empty_spaces.txt')

        # Create a vertical layout for the Empty Space Management screen
        layout = QVBoxLayout(self.empty_space_management_screen)

        # Create a QListWidget to display the empty space data
        list_widget = QListWidget(self.empty_space_management_screen)
        layout.addWidget(list_widget)

        # Populate the QListWidget with empty space data
        for parking_spot, is_full in empty_space_data.items():
            status = "Full" if is_full else "Empty"
            item_text = f"Parking Spot {parking_spot}: {status}"

            item = QListWidgetItem(item_text)
            list_widget.addItem(item)

            # Set row color based on the parking spot status
            color = QColor("red" if is_full else "green")
            item.setBackground(color)

    def load_empty_space_data(self, filename):
        empty_space_data = {}
        try:
            with open(filename, 'r') as file:
                for line in file:
                    parts = line.strip().split(':')
                    if len(parts) == 2:
                        parking_spot = parts[0].strip()
                        is_full = bool(int(parts[1].strip()))
                        empty_space_data[parking_spot] = is_full
        except Exception as e:
            print(f"Error loading empty space data: {e}")

        return empty_space_data

    def update_csv_data(self):
        # Update CSV data every 10 milliseconds
        entry_management_data = self.load_csv_data('license_plates.csv')
        empty_space_data = self.load_empty_space_data('empty_spaces.txt')

        self.update_entry_management_screen(entry_management_data)
        self.update_empty_space_management_screen(empty_space_data)

    def update_entry_management_screen(self, data):
        # Update Entry Management screen with new data
        list_widget = self.entry_management_screen.findChild(QListWidget)
        list_widget.clear()

        for car_id, (license_number, score) in data.items():
            item_text = f"Car ID: {car_id}, License Number: {license_number}, Score: {score}"
            list_widget.addItem(item_text)

    def update_empty_space_management_screen(self, empty_space_data):
        # Update Empty Space Management screen with new data
        list_widget = self.empty_space_management_screen.findChild(QListWidget)
        list_widget.clear()

        for parking_spot, is_full in empty_space_data.items():
            status = "Full" if is_full else "Empty"
            item_text = f"Parking Spot {parking_spot}: {status}"

            item = QListWidgetItem(item_text)
            list_widget.addItem(item)

            # Set row color based on the parking spot status
            color = QColor("red" if is_full else "green")
            item.setBackground(color)

    def show_entry_management(self):
        self.stacked_widget.setCurrentWidget(self.entry_management_screen)

    def show_empty_space_management(self):
        self.stacked_widget.setCurrentWidget(self.empty_space_management_screen)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_app = MyApp()
    sys.exit(app.exec_())
