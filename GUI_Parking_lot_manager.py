import sys
import csv
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QListWidget, QListWidgetItem, QPushButton, QHBoxLayout, QStackedWidget
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QColor
from datetime import datetime, timedelta  # Added timedelta for time calculation


class MyApp(QWidget):
    def __init__(self):
        super().__init__()

        # Set up the main window
        self.setGeometry(100, 100, 730, 530)
        self.setWindowTitle('Parking Lot Manager (Hourly rate: $5.00)')

        main_layout = QVBoxLayout(self)

        button_layout = QHBoxLayout()

        self.entry_management_button = QPushButton('Entry Management', self)
        self.entry_management_button.clicked.connect(self.show_entry_management)
        button_layout.addWidget(self.entry_management_button)

        self.empty_space_management_button = QPushButton('Empty Space Management', self)
        self.empty_space_management_button.clicked.connect(self.show_empty_space_management)
        button_layout.addWidget(self.empty_space_management_button)

        main_layout.addLayout(button_layout)

        self.stacked_widget = QStackedWidget(self)
        main_layout.addWidget(self.stacked_widget)

        self.entry_management_screen = QWidget()
        self.setup_entry_management_screen()
        self.stacked_widget.addWidget(self.entry_management_screen)

        self.empty_space_management_screen = QWidget()
        self.setup_empty_space_management_screen()
        self.stacked_widget.addWidget(self.empty_space_management_screen)

        self.csv_refresh_timer = QTimer(self)
        self.csv_refresh_timer.timeout.connect(self.update_csv_data)
        self.csv_refresh_timer.start(50)

        # Show the GUI
        self.show()

    def calculate_time_spent(self, entry_datetime):
        if entry_datetime:
            entry_time = datetime.strptime(entry_datetime, '%Y-%m-%d %H:%M:%S.%f')

            current_time = datetime.now()
            time_spent = current_time - entry_time
            return str(time_spent).split(".")[0]  # Format as %H:%M

        return "N/A"

    def setup_entry_management_screen(self):
        # Load data from the CSV file
        data = self.load_csv_data('license_plates.csv')

        # Create a vertical layout for the Entry Management screen
        layout = QVBoxLayout(self.entry_management_screen)

        # Create a QListWidget to display the data
        list_widget = QListWidget(self.entry_management_screen)
        layout.addWidget(list_widget)

        # Populate the QListWidget with data
        for car_id, (license_number, score, entry_datetime) in data.items():
            # Calculate time spent in the parking lot
            time_spent = self.calculate_time_spent(entry_datetime)

            item_text = f"Car ID: {car_id}, License Number: {license_number}, Score: {score}, Entry Time: {entry_datetime[:-7]}, Time Spent: {time_spent}, Cost:{0}"
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
                    entry_datetime = row.get('datetime', '')  # Added datetime column

                    if car_id not in data or score > data[car_id][1]:
                        data[car_id] = (license_number, score, entry_datetime)
        except Exception as e:
            print(f"Error loading CSV file: {e}")


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

        for car_id, (license_number, score, entry_datetime) in data.items():
            # Calculate time spent in the parking lot
            time_spent = self.calculate_time_spent(entry_datetime)

            date_string = entry_datetime


            date_format = "%Y-%m-%d %H:%M:%S.%f"

            date_object = datetime.strptime(date_string, date_format)

            formatted_date = date_object.strftime("%Y-%m-%d %H:%M")


            dollars = 0
            input_string = time_spent
            split_values = input_string.split(':')
            if len(split_values) == 3:
                result = int(split_values[0]) * 5
                dollars = result
            else:
                dollars = 0

            item_text = f"Car ID: {car_id}, License Number: {license_number}, Score: {score}, Entry Time: {formatted_date}, Time Spent: {time_spent}, Cost: ${dollars}"
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
