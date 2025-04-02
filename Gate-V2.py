import sys
import csv
import pandas as pd
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
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Kings Point')
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()

        # Create menu bar
        self._create_menu_bar()

        # Create top layout with logo, label, input field and button
        top_layout = self._create_top_layout()
        main_layout.addLayout(top_layout)

        # QTreeWidget for displaying processed data
        self.my_game = QTreeWidget(self)
        self.my_game.setColumnCount(5)
        self.my_game.setHeaderLabels(['Gate', 'Total', 'Daily Avg', 'RFID', 'Barcode'])
        self.my_game.setColumnWidth(0, 120)
        main_layout.addWidget(self.my_game)
        
        central_widget.setLayout(main_layout)
        self.setGeometry(100, 100, 800, 600)

    def _create_menu_bar(self):
        """Create and set up the menu bar with actions"""
        menu_bar = QMenuBar(self)
        self.setMenuBar(menu_bar)
        
        # Create actions
        actions = {
            "Gate Report": self.show_gate_report,
            "User Adds": self.user_adds,
            "Combine Files": self.combine_files
        }
        
        # Add actions to menu bar
        for action_name, action_handler in actions.items():
            action = QAction(action_name, self)
            action.triggered.connect(action_handler)
            menu_bar.addAction(action)

    def _create_top_layout(self):
        """Create and return the top horizontal layout"""
        top_layout = QHBoxLayout()
        
        # Logo
        logo_label = QLabel(self)
        pixmap = QPixmap('logo.png')
        if not pixmap.isNull():
            pixmap = pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo_label.setPixmap(pixmap)
        else:
            logo_label.setText("Logo")  # Simple fallback

        # File path label
        self.label = QLabel("No file selected", self)
        self.label.setFixedHeight(30)
        
        # Combine logo and label
        logo_and_label_layout = QVBoxLayout()
        logo_and_label_layout.addWidget(logo_label)
        logo_and_label_layout.addWidget(self.label)

        # File path input field with auto-complete
        self.path_input = QLineEdit(self)
        self.path_input.setPlaceholderText("Paste or type file path here...")
        self.path_input.setFixedHeight(30)
        self.path_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        # Set up completer for path input
        file_system_model = QFileSystemModel(self)
        file_system_model.setRootPath(QDir.rootPath())
        completer = QCompleter(file_system_model, self)
        completer.setCompletionMode(QCompleter.PopupCompletion)
        completer.setCaseSensitivity(False)
        self.path_input.setCompleter(completer)

        # Browse button
        self.btn = QPushButton('Browse', self)
        self.btn.setFixedSize(80, 30)
        self.btn.clicked.connect(self.showFileDialog)
        
        # Add widgets to top layout
        top_layout.addLayout(logo_and_label_layout)
        top_layout.addWidget(self.path_input)
        top_layout.addWidget(self.btn)
        
        return top_layout

    def resizeEvent(self, event):
        """Handle window resize to adjust path input field width"""
        window_width = self.width()
        self.path_input.setFixedWidth(window_width - self.btn.width() - 40 - self.label.width())
        super().resizeEvent(event)

    def showFileDialog(self):
        """Show file dialog and process selected file"""
        options = QFileDialog.Options() | QFileDialog.ReadOnly
        file_filter = "Excel Files (*.xlsx *.xls);;CSV Files (*.csv);;All Files (*)"
        fileName, _ = QFileDialog.getOpenFileName(self, "Select a File", "", file_filter, options=options)
        
        if fileName:
            self.label.setText(fileName)
            self.path_input.setText(fileName)
            self.load_gate_data(fileName)

    def load_gate_data(self, filepath):
        """Load and display gate data from file"""
        # Process data based on file type
        if filepath.lower().endswith(('.xlsx', '.xls')):
            data = process_excel_data(filepath)
        else:
            data = process_gate_data(filepath)
            
        # Display data in tree widget
        self.my_game.clear()
        for record in data:
            QTreeWidgetItem(self.my_game, [
                record['Gate'], 
                str(record['Total']), 
                str(record['Daily Avg']), 
                str(record['RFID']), 
                str(record['Barcode'])
            ])

    def show_gate_report(self):
        """Show gate report interface"""
        self.label.setText("Select a CSV or Excel file for the Gate Report.")
        self.my_game.clear()

    def user_adds(self):
        """Handle user adds functionality"""
        # Get file to modify
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Select a CSV File", "", 
                                                "CSV Files (*.csv);;All Files (*)", options=options)
        if not fileName:
            return

        # Get range of numbers to add
        start, ok1 = QInputDialog.getInt(self, "Input Range", "Enter the starting number:")
        end, ok2 = QInputDialog.getInt(self, "Input Range", "Enter the ending number:")
        if not (ok1 and ok2):
            return
        if start > end:
            QMessageBox.warning(self, "Invalid Range", "The starting number must be less than or equal to the ending number.")
            return

        # Get department selection
        department_options = ["Residents", "RFID tag"]
        department, ok_dep = QInputDialog.getItem(self, "Select Department", "Choose a Department:", 
                                                department_options, 0, False)
        if not ok_dep:
            return

        # Get access level selection
        access_level_options = ["Normandy Bathroom", "Std Gate Hours"]
        access_level, ok_acc = QInputDialog.getItem(self, "Select Access Level", "Choose an Access Level:", 
                                                   access_level_options, 0, False)
        if not ok_acc:
            return

        self._add_user_records(fileName, start, end, department, access_level)

    def _add_user_records(self, fileName, start, end, department, access_level):
        """Add user records to CSV file"""
        current_date = QDate.currentDate().toString("yyyy-MMM-dd")
        
        # Read existing CSV file
        try:
            with open(fileName, mode='r', newline='', encoding='utf-8-sig') as file:
                reader = csv.DictReader(file)
                fieldnames = reader.fieldnames
                if "Surname" not in fieldnames:
                    QMessageBox.warning(self, "Error", "'Surname' column not found in the CSV file.")
                    return
                rows = list(reader)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to read CSV file: {str(e)}")
            return

        # Find first empty row index
        first_empty_index = len(rows)
        for i, row in enumerate(rows):
            if not row.get('Surname'):
                first_empty_index = i
                break

        # Create new user records
        for number in range(start, end + 1):
            new_row = {key: "" for key in fieldnames}  # Initialize with empty values
            new_row.update({
                "Surname": str(number),
                "Card Number": f"0#{number}",
                "Department": department,
                "Access level": access_level,
                "Activation date": current_date
            })
            
            if first_empty_index < len(rows):
                rows.insert(first_empty_index, new_row)
            else:
                rows.append(new_row)
            first_empty_index += 1

        # Write updated data back to CSV
        try:
            with open(fileName, mode='w', newline='', encoding='utf-8-sig') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)
            QMessageBox.information(self, "Success", f"Added numbers {start} to {end} to the CSV file.")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to write to CSV file: {str(e)}")

    def combine_files(self):
        """Combine two CSV files into one"""
        options = QFileDialog.Options()
        
        # Get first file
        fileName1, _ = QFileDialog.getOpenFileName(self, "Select the First CSV File", "", 
                                                 "CSV Files (*.csv);;All Files (*)", options=options)
        if not fileName1:
            return
            
        # Get second file
        fileName2, _ = QFileDialog.getOpenFileName(self, "Select the Second CSV File", "", 
                                                 "CSV Files (*.csv);;All Files (*)", options=options)
        if not fileName2:
            return

        try:
            # Read the first file
            with open(fileName1, mode='r', newline='', encoding='utf-8-sig') as file1:
                reader1 = csv.DictReader(file1)
                fieldnames1 = reader1.fieldnames
                rows1 = list(reader1)

            # Read the second file
            with open(fileName2, mode='r', newline='', encoding='utf-8-sig') as file2:
                reader2 = csv.DictReader(file2)
                fieldnames2 = reader2.fieldnames
                rows2 = list(reader2)

            # Check if headers match
            if fieldnames1 != fieldnames2:
                QMessageBox.warning(self, "Error", "The two CSV files have different column headers and cannot be combined.")
                return

            # Combine the rows
            combined_rows = rows1 + rows2
            
            # Get output file name
            saveFileName, _ = QFileDialog.getSaveFileName(self, "Save Combined CSV File", "", 
                                                        "CSV Files (*.csv);;All Files (*)", options=options)
            if not saveFileName:
                return

            # Write combined data
            with open(saveFileName, mode='w', newline='', encoding='utf-8-sig') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames1)
                writer.writeheader()
                writer.writerows(combined_rows)

            QMessageBox.information(self, "Success", "The CSV files have been successfully combined and saved.")
        
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error combining files: {str(e)}")

def process_gate_data(filepath):
    """Process CSV gate data"""
    # Define gate mapping dictionary - maps 'Where' column values to (gate, type) tuples
    gate_mapping = {
        'BurgGate (Barcode)': ('Burgundy', 'gate'),
        'BurgGate (RFID)': ('Burgundy', 'rfid'),
        'FlanGate (RFID)': ('Flanders', 'gate'),
        'FlanGate (Barcode)': ('Flanders', 'rfid'),
        'MonaGate (Barcode)': ('Monaco', 'gate'),
        'MonaGate (RFID)': ('Monaco', 'rfid'),
        'MainGate (Barcode)': ('Atlantic', 'gate'),
        'MainGate (RFID)': ('Atlantic', 'rfid'),
        'NormGate (Barcode)': ('Normandy', 'gate'),
        'NormGate (RFID)': ('Normandy', 'rfid'),
        'SaxoGate (RFID)': ('Saxony', 'rfid'),
        'SaxoGate (Barcode)': ('Saxony', 'gate')
    }
    
    # Initialize counts for each gate
    gate_counts = {
        gate: {'gate': 0, 'rfid': 0} 
        for gate in ['Burgundy', 'Flanders', 'Atlantic', 'Monaco', 'Normandy', 'Saxony']
    }
    
    try:
        # Read and process CSV file
        with open(filepath, mode='r', newline='', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            for row in reader:
                cell_value = row.get('Where', '')
                if cell_value in gate_mapping:
                    gate, count_type = gate_mapping[cell_value]
                    gate_counts[gate][count_type] += 1
                    
        # Prepare output data
        return [
            {
                'Gate': gate,
                'Total': counts['gate'] + counts['rfid'],
                'Daily Avg': round(counts['gate'] / 30.5),  # Assuming 30.5 days per month
                'RFID': counts['rfid'],
                'Barcode': counts['gate']
            }
            for gate, counts in gate_counts.items()
        ]
    except Exception as e:
        print(f"Error processing CSV file: {e}")
        return []

def process_excel_data(filepath):
    """Process Excel gate data"""
    # Define the mapping from category strings to (gate, type)
    category_mapping = {
        "1-1 PNL 1 RD1 Normandy Gate RFID": ("Normandy", "RFID"),
        "1-2 PNL 1 RD2 Normandy Gate Barcode": ("Normandy", "Barcode"),
        "2-1 PNL 2 RD1 Flanders Gate RFID": ("Flanders", "RFID"),
        "3-2 PNL 3 RD2 Burgandy Gate Barcode": ("Burgundy", "Barcode"),
        "4-1 PNL 4 RD1 Saxony Gate RFID": ("Saxony", "RFID"),
        "5-1 PNL 5 RD1 Atlantic Gate RFID": ("Atlantic", "RFID"),
        "5-2 PNL 5 RD2 Atlantic Gate Barcode": ("Atlantic", "Barcode"),
        "6-1 PNL 6 RD1 Monaco Gate Barcode": ("Monaco", "Barcode"),
        "6-2 PNL 6 RD2 Monaco Gate RFID": ("Monaco", "RFID")
    }
    
    # Initialize counts for each gate
    gate_counts = {
        gate: {'gate': 0, 'rfid': 0} 
        for gate in ['Burgundy', 'Flanders', 'Atlantic', 'Monaco', 'Normandy', 'Saxony']
    }
    
    try:
        # Read the Excel file
        df = pd.read_excel(filepath)
        
        # Get the column to analyze (column E or 5th column)
        col_data = df['E'] if 'E' in df.columns else df.iloc[:, 4]
        
        # Process each value
        for value in col_data:
            if pd.notna(value):  # Check if value is not NaN
                value_str = str(value).strip()
                if value_str in category_mapping:
                    gate, type_str = category_mapping[value_str]
                    count_type = 'rfid' if type_str == "RFID" else 'gate'
                    gate_counts[gate][count_type] += 1
        
        # Prepare output data
        return [
            {
                'Gate': gate,
                'Total': counts['gate'] + counts['rfid'],
                'Daily Avg': round(counts['gate'] / 30.5),  # Using Barcode count for daily average
                'RFID': counts['rfid'],
                'Barcode': counts['gate']
            }
            for gate, counts in gate_counts.items()
        ]
    except Exception as e:
        print(f"Error processing Excel file: {e}")
        return []

def main():
    app = QApplication(sys.argv)
    ex = FileDialogDemo()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()