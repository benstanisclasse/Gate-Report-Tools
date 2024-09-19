import sys
import csv
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QFileDialog, QLabel, QWidget,
    QLineEdit, QCompleter, QFileSystemModel, QVBoxLayout, QHBoxLayout,
    QTreeWidget, QTreeWidgetItem, QInputDialog, QMenuBar, QAction,
    QMessageBox, QSizePolicy
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QDir, QDate, Qt


class FileDialogDemo(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up the user interface
        self.initUI()

    def initUI(self):
        # Set the window title
        self.setWindowTitle('Kings Point')

        # Create the central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create a vertical layout for the central widget
        main_layout = QVBoxLayout()

        # Create the menu bar
        menu_bar = QMenuBar(self)
        self.setMenuBar(menu_bar)

        # Add Gate Report, User Adds, and Combine Files options to the menu
        gate_report_action = QAction("Gate Report", self)
        user_adds_action = QAction("User Adds", self)
        combine_files_action = QAction("Combine Files", self)
        menu_bar.addAction(gate_report_action)
        menu_bar.addAction(user_adds_action)
        menu_bar.addAction(combine_files_action)

        # Connect menu actions to functions
        gate_report_action.triggered.connect(self.show_gate_report)
        user_adds_action.triggered.connect(self.user_adds)
        combine_files_action.triggered.connect(self.combine_files)

        # Create a horizontal layout for the top row
        top_layout = QHBoxLayout()

        # Add the Kings Point logo to the top left corner
        logo_label = QLabel(self)
        pixmap = QPixmap('logo.png')

        if pixmap.isNull():
            QMessageBox.warning(self, "Error", "Logo image not found.")
        else:
            pixmap = pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo_label.setPixmap(pixmap)

        # Create a label to show selected file path
        self.label = QLabel("No file selected", self)
        self.label.setFixedHeight(30)

        # Create a vertical layout to hold the logo and label together
        logo_and_label_layout = QVBoxLayout()
        logo_and_label_layout.addWidget(logo_label)
        logo_and_label_layout.addWidget(self.label)

        # Create a line edit for inputting the file path
        self.path_input = QLineEdit(self)
        self.path_input.setPlaceholderText("Paste or type file path here...")
        self.path_input.setFixedHeight(30)
        self.path_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # Set up the QCompleter for auto-completion of file paths
        file_system_model = QFileSystemModel(self)
        file_system_model.setRootPath(QDir.rootPath())
        completer = QCompleter(file_system_model, self)
        completer.setCompletionMode(QCompleter.PopupCompletion)
        completer.setCaseSensitivity(False)
        self.path_input.setCompleter(completer)

        # Create a smaller button to open the file dialog
        self.btn = QPushButton('Browse', self)
        self.btn.setFixedSize(80, 30)  # Set fixed size for the button
        self.btn.clicked.connect(self.showFileDialog)  # Connect the button click to the file dialog

        # Add widgets to the top layout
        top_layout.addLayout(logo_and_label_layout)  # Add the logo and label layout to the top layout
        top_layout.addWidget(self.path_input)
        top_layout.addWidget(self.btn)

        # Add the top layout to the main layout
        main_layout.addLayout(top_layout)

        # Create a QTreeWidget for displaying the processed data
        self.my_game = QTreeWidget(self)
        self.my_game.setColumnCount(5)
        self.my_game.setHeaderLabels(['Gate', 'Total', 'Daily Avg', 'RFID', 'Barcode'])
        self.my_game.setColumnWidth(0, 120)  # Set column widths as needed

        # Add the QTreeWidget to the main layout
        main_layout.addWidget(self.my_game)

        # Set the layout for the central widget
        central_widget.setLayout(main_layout)

        # Set the window size
        self.setGeometry(100, 100, 800, 600)  # width: 800, height: 600

    def resizeEvent(self, event):
        # Automatically resize the text input and button as the window resizes
        window_width = self.width()
        self.path_input.setFixedWidth(window_width - self.btn.width() - 40 - self.label.width())
        super().resizeEvent(event)

    def showFileDialog(self):
        # Open the file dialog and get the selected file path
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        fileName, _ = QFileDialog.getOpenFileName(self, "Select a File", "", "CSV Files (*.csv);;All Files (*)", options=options)
        
        if fileName:
            # Show the selected file path on the label and in the input field
            self.label.setText(fileName)
            self.path_input.setText(fileName)
            # Load and display gate data from the file
            self.load_gate_data(fileName)

    def load_gate_data(self, filepath):
        data = process_gate_data(filepath)
        
        # Clear existing data in the QTreeWidget
        self.my_game.clear()

        # Populate the QTreeWidget with new data
        for record in data:
            QTreeWidgetItem(self.my_game, [
                record['Gate'], 
                str(record['Total']), 
                str(record['Daily Avg']), 
                str(record['RFID']), 
                str(record['Barcode'])
            ])

    def show_gate_report(self):
        self.label.setText("Select a CSV file for the Gate Report.")
        self.my_game.clear()

    def user_adds(self):
        # Select a CSV file to edit
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Select a CSV File", "", "CSV Files (*.csv);;All Files (*)", options=options)
        
        if not fileName:
            return

        # Ask for the range of numbers to add
        start, ok1 = QInputDialog.getInt(self, "Input Range", "Enter the starting number:")
        end, ok2 = QInputDialog.getInt(self, "Input Range", "Enter the ending number:")
        
        if not (ok1 and ok2):
            return
        
        if start > end:
            QMessageBox.warning(self, "Invalid Range", "The starting number must be less than or equal to the ending number.")
            return

        # Prompt the user to select the Department
        department_options = ["Residents", "RFID tag"]
        department, ok_dep = QInputDialog.getItem(self, "Select Department", "Choose a Department:", department_options, 0, False)
        if not ok_dep:
            return

        # Prompt the user to select the Access level
        access_level_options = ["Normandy Bathroom", "Std Gate Hours"]
        access_level, ok_acc = QInputDialog.getItem(self, "Select Access Level", "Choose an Access Level:", access_level_options, 0, False)
        if not ok_acc:
            return

        current_date = QDate.currentDate().toString("yyyy-MMM-dd")  # Format date as "1999-Jan-01"

        # Load the CSV file
        rows = []
        with open(fileName, mode='r', newline='', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            fieldnames = reader.fieldnames
            
            if "Surname" not in fieldnames:
                QMessageBox.warning(self, "Error", "'Surname' column not found in the CSV file.")
                return

            rows = list(reader)

        # Find the first empty line (where the 'Surname' field is empty)
        first_empty_index = len(rows)
        for i, row in enumerate(rows):
            if not row.get('Surname'):  # Checking for empty 'Surname' cells
                first_empty_index = i
                break

        # Add the new rows starting from the first empty index
        for number in range(start, end + 1):
            new_row = {
                "Surname": str(number),
                "First name": "",
                "Middle name": "",
                "Card Number": f"0#{number}",
                "PIN": "",
                "Department": department,  # Use selected Department
                "Access level": access_level,  # Use selected Access Level
                "Telephone": "",
                "Extension": "",
                "Fax": "",
                "Activation date": current_date,
                "Expiration date": "",
                "Address 1": "",
                "Address 2": "",
                "Town": "",
                "County": "",
                "Post code": "",
                "Home telephone": "",
                "Home Fax": "",
                "Mobile": "",
                "Email": "",
                "Position": "",
                "Start date": "",
                "Car registration": "",
                "Notes": "",
                "Personnel number": "",
                "User ID": ""
            }
            
            if first_empty_index < len(rows):
                rows.insert(first_empty_index, new_row)
            else:
                rows.append(new_row)
            first_empty_index += 1

        # Save the updated CSV file
        with open(fileName, mode='w', newline='', encoding='utf-8-sig') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

        QMessageBox.information(self, "Success", f"Added numbers {start} to {end} to the CSV file.")

    def combine_files(self):
        # Select the first CSV file
        options = QFileDialog.Options()
        fileName1, _ = QFileDialog.getOpenFileName(self, "Select the First CSV File", "", "CSV Files (*.csv);;All Files (*)", options=options)
        
        if not fileName1:
            return

        # Select the second CSV file
        fileName2, _ = QFileDialog.getOpenFileName(self, "Select the Second CSV File", "", "CSV Files (*.csv);;All Files (*)", options=options)
        
        if not fileName2:
            return

        # Load the first CSV file
        rows1 = []
        with open(fileName1, mode='r', newline='', encoding='utf-8-sig') as file1:
            reader1 = csv.DictReader(file1)
            fieldnames1 = reader1.fieldnames
            rows1 = list(reader1)

        # Load the second CSV file
        rows2 = []
        with open(fileName2, mode='r', newline='', encoding='utf-8-sig') as file2:
            reader2 = csv.DictReader(file2)
            fieldnames2 = reader2.fieldnames
            rows2 = list(reader2)

        # Check if the fieldnames match
        if fieldnames1 != fieldnames2:
            QMessageBox.warning(self, "Error", "The two CSV files have different column headers and cannot be combined.")
            return

        # Combine the rows from both files
        combined_rows = rows1 + rows2

        # Prompt the user to save the combined file
        saveFileName, _ = QFileDialog.getSaveFileName(self, "Save Combined CSV File", "", "CSV Files (*.csv);;All Files (*)", options=options)
        
        if not saveFileName:
            return

        # Save the combined CSV file
        with open(saveFileName, mode='w', newline='', encoding='utf-8-sig') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames1)
            writer.writeheader()
            writer.writerows(combined_rows)

        QMessageBox.information(self, "Success", "The CSV files have been successfully combined and saved.")

def process_gate_data(filepath):
    # Initialize gate counts and RFID counts
    gate_counts = {
        'Burgundy': {'gate': 0, 'rfid': 0}, 
        'Flanders': {'gate': 0, 'rfid': 0}, 
        'Atlantic': {'gate': 0, 'rfid': 0}, 
        'Monaco': {'gate': 0, 'rfid': 0}, 
        'Normandy': {'gate': 0, 'rfid': 0}, 
        'Saxony': {'gate': 0, 'rfid': 0}
    }

    # Read data from the CSV file
    with open(filepath, mode='r', newline='', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        for row in reader:
            cellValue = row['Where']  # Use the "Where" column to determine gate location

            if cellValue == 'BurgGate (Barcode)':
                gate_counts['Burgundy']['gate'] += 1
            elif cellValue == 'BurgGate (RFID)':
                gate_counts['Burgundy']['rfid'] += 1 
            elif cellValue == 'FlanGate (RFID)':
                gate_counts['Flanders']['gate'] += 1
            elif cellValue == 'FlanGate (Barcode)':
                gate_counts['Flanders']['rfid'] += 1
            elif cellValue == 'MonaGate (Barcode)':
                gate_counts['Monaco']['gate'] += 1
            elif cellValue == 'MonaGate (RFID)':
                gate_counts['Monaco']['rfid'] += 1
            elif cellValue == 'MainGate (Barcode)':
                gate_counts['Atlantic']['gate'] += 1
            elif cellValue == 'MainGate (RFID)':
                gate_counts['Atlantic']['rfid'] += 1
            elif cellValue == 'NormGate (Barcode)':
                gate_counts['Normandy']['gate'] += 1
            elif cellValue == 'NormGate (RFID)':
                gate_counts['Normandy']['rfid'] += 1
            elif cellValue == 'SaxoGate (RFID)':
                gate_counts['Saxony']['rfid'] += 1
            elif cellValue == 'SaxoGate (Barcode)':
                gate_counts['Saxony']['gate'] += 1

    # Prepare the processed data for return
    processed_data = []
    for gate, counts in gate_counts.items():
        gate_total = counts['gate'] + counts['rfid']
        daily_avg = round(counts['gate'] / 30.5)  # Assuming 30.5 days in a month
        processed_data.append({
            'Gate': gate,
            'Total': gate_total,
            'Daily Avg': daily_avg,
            'RFID': counts['rfid'],
            'Barcode': counts['gate']
        })
    
    return processed_data

def main():
    # Create the application object
    app = QApplication(sys.argv)
    
    # Create the main window
    ex = FileDialogDemo()
    
    # Show the main window
    ex.show()
    
    # Execute the application
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
