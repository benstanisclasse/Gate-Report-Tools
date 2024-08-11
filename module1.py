import sys
import csv
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QFileDialog, QLabel, QWidget,
    QLineEdit, QCompleter, QFileSystemModel, QVBoxLayout, QHBoxLayout,
    QTreeWidget, QTreeWidgetItem, QComboBox, QInputDialog, QMenuBar, QAction,
    QMessageBox
)
from PyQt5.QtCore import QDir, QDate

class FileDialogDemo(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up the user interface
        self.initUI()

    def initUI(self):
        # Create the central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create a vertical layout for the central widget
        main_layout = QVBoxLayout()

        # Create the menu bar
        menu_bar = QMenuBar(self)
        self.setMenuBar(menu_bar)

        # Add Gate Report and User Adds options to the menu
        gate_report_action = QAction("Gate Report", self)
        user_adds_action = QAction("User Adds", self)
        menu_bar.addAction(gate_report_action)
        menu_bar.addAction(user_adds_action)

        # Connect menu actions to functions
        gate_report_action.triggered.connect(self.show_gate_report)
        user_adds_action.triggered.connect(self.user_adds)

        # Create a horizontal layout for the top row
        top_layout = QHBoxLayout()

        # Create a label to show selected file path
        self.label = QLabel("No file selected", self)
        self.label.setFixedHeight(30)

        # Create a line edit for inputting the file path
        self.path_input = QLineEdit(self)
        self.path_input.setPlaceholderText("Paste or type file path here...")
        self.path_input.setFixedHeight(30)

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
        top_layout.addWidget(self.label)
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

        # Set the window title
        self.setWindowTitle('File Dialog Example')

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
        fileName, _ = QFileDialog.getOpenFileName(self, "Select a File", "", "All Files (*);;Python Files (*.py)", options=options)
        
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
        self.label.setText("Select an Excel file for the Gate Report.")
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

        department_options = ["Resident", "RFID tag"]
        access_level_option = "Normandy Bathroom"
        current_date = QDate.currentDate().toString("yyyy-MM-dd")

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
                "Department": department_options[0],  # Default to "Resident"
                "Access level": access_level_option,
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
                rows[first_empty_index] = new_row
            else:
                rows.append(new_row)
            first_empty_index += 1

        # Save the updated CSV file
        with open(fileName, mode='w', newline='', encoding='utf-8-sig') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

        QMessageBox.information(self, "Success", f"Added numbers {start} to {end} to the CSV file.")

def main():
    # Create the application object
    app = QApplication(sys.argv)
    # Create the main window
    ex = FileDialogDemo()
    ex.show()
    # Execute the application
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
