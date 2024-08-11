This program is a Python-based graphical user interface (GUI) application designed to manage and manipulate CSV files, specifically for a system related to gate and RFID management at a location like Kings Point. The application is built using the PyQt5 library, which allows it to have a user-friendly interface for interacting with CSV files without needing to use the command line or a text editor.
![image](https://github.com/user-attachments/assets/d696e3c5-d735-4646-a6f0-6af085c4a5dd)

### Key Features and Functions:

1. **Gate Report**:
   - This feature allows users to load a CSV file and generate a report based on the gate and RFID data contained within. The report is displayed in a table format within the application.

2. **User Adds**:
   - This feature enables users to add a range of user entries to a CSV file. It prompts the user for a range of numbers, which are then used to populate specific fields in the CSV file, such as "Surname" and "Card Number". The user is also prompted to select a department and access level for the new entries.
   - The new entries are either inserted at the first available empty row in the CSV file or appended to the end if no empty rows are found.

3. **Combine Files**:
   - This feature allows the user to select two CSV files and combine them into one. The combined file can then be saved as a new CSV file. The program checks if the two files have the same column headers before combining them to ensure data integrity.

### Detailed Breakdown of the Interface:

- **Menu Bar**:
  - **Gate Report**: Loads and processes a CSV file to display gate-related data.
  - **User Adds**: Prompts the user for details to add new user entries to a CSV file.
  - **Combine Files**: Allows the user to select two CSV files and combine them into one.

- **Top Row**:
  - **Logo**: Displays the Kings Point logo (if available) on the top left.
  - **File Path Input**: A text box where users can paste or type the path of a CSV file.
  - **Browse Button**: Opens a file dialog to select a CSV file.

- **Main Area**:
  - **QTreeWidget**: Displays the processed gate data in a tabular format.

### How to Use the Application:

1. **Running the Program**:
   - The program is run as a Python script. If it's packaged as an executable using PyInstaller, simply double-click the executable to open the application.

2. **Gate Report**:
   - Click on "Gate Report" in the menu bar.
   - Use the "Browse" button or paste the path of a CSV file containing gate data into the text box.
   - The application will load the CSV file and display the processed gate data in the table below.

3. **User Adds**:
   - Click on "User Adds" in the menu bar.
   - Select the CSV file you wish to edit.
   - Enter the range of numbers you wish to add (for example, user IDs).
   - Choose the department and access level for the new entries.
   - The program will add new entries to the CSV file, filling out the "Surname" and "Card Number" columns based on the range provided, and using the selected department and access level.

4. **Combine Files**:
   - Click on "Combine Files" in the menu bar.
   - Select the first CSV file.
   - Select the second CSV file.
   - The program will combine the two files into one, ensuring that the column headers match.
   - Save the combined file by selecting a location on your system.

### Error Handling:

- **Missing Logo**: If the logo image (`logo.png`) is not found, a warning is displayed.
- **CSV File Issues**: If there are mismatches in column headers during the "Combine Files" operation or if the required columns are missing during the "User Adds" operation, the program will display appropriate error messages to the user.

### Additional Information:

- The program relies on CSV files with specific column structures, such as having columns like "Surname," "Card Number," and "Where" for gate data. 
- It is designed to work with UTF-8 encoded CSV files and can handle typical CSV file operations required in a gate and RFID management system.

This application is an example of how Python, combined with libraries like PyQt5, can be used to build a powerful yet user-friendly tool for managing data in a specific domain.
