This program is a Python-based graphical user interface (GUI) application designed to manage and manipulate CSV files, specifically for a system related to gate and RFID management at a location like Kings Point. The application is built using the PyQt5 library, which allows it to have a user-friendly interface for interacting with CSV files without needing to use the command line or a text editor.
![image](https://github.com/user-attachments/assets/d696e3c5-d735-4646-a6f0-6af085c4a5dd)

### Key Features and Functions:

1. **Gate Report**:
   - This feature allows users to load a CSV file and generate a report based on the gate and RFID data contained within. The report is displayed in a table format within the application.

2. **User Adds**:

![image](https://github.com/user-attachments/assets/c2b79918-db50-4dbd-aae6-0e299619d9a9)

   - This feature enables users to add a range of user entries to a CSV file. It prompts the user for a range of numbers, which are then used to populate specific fields in the CSV file, such as "Surname" and "Card Number". The user is also prompted to select a department and access level for the new entries.
   - The new entries are either inserted at the first available empty row in the CSV file or appended to the end if no empty rows are found.

4. **Combine Files**:
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

Running the Application
This application is available as a standalone executable file, meaning you can run it without needing to have Python installed on your system or worry about setting up a Python environment.

How to Run the Executable
Download the Executable:

The executable file, gate.exe, is located in the program folder of this repository. You can run this file directly without any additional setup.
Run the Application:

Simply double-click the gate.exe file. This will launch the Kings Point application, where you can interact with the various features, such as generating gate reports, adding users to CSV files, and combining CSV files.
No Installation Required:

The executable is self-contained, meaning it has all the necessary dependencies bundled within it. You do not need to install any additional software or libraries.
Cross-Platform Considerations:

This executable is currently built for Windows. If you are using a different operating system (e.g., macOS or Linux), you will need to run the Python source code directly or use a tool like Wine to run the executable on your system.
Test the Program
To help you get started, a set of sample CSV files is provided in the Test data folder. You can use these files to test out the various functionalities of the program:

Gate Report: Generate reports based on the gate data contained in the provided CSV files.
User Adds: Add new user entries to the sample CSV files and see how the program manages the data.
Combine Files: Test how the program combines multiple CSV files into one.
Simply load these files into the program using the provided interface and explore the different features.

Benefits of the Executable
Ease of Use: Running the application as an executable simplifies the process for end-users who may not be familiar with Python or programming.
Portability: The standalone executable can be easily transferred between different machines and environments without requiring additional setup.
Efficiency: Since everything needed to run the application is included in the executable, it eliminates the need for manual dependency management, reducing the potential for errors and compatibility issues.
By providing an executable file and test data, we've made it easy to deploy and use the Kings Point application on any Windows machine with minimal hassle.



