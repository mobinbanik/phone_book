"""Phonebook application."""
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTableWidget,
    QTableWidgetItem, QDockWidget, QFormLayout,
    QLineEdit, QWidget, QPushButton,
    QSpinBox, QMessageBox, QToolBar,
    QMessageBox, QLabel,
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QAction
import sys


class MainWindow(QMainWindow):
    """Main window.

    Our main window class that creates a QMainWindow.
    """

    def __init__(self, *args, **kwargs):
        """Initialize the main window."""
        super().__init__(*args, **kwargs)
        # Set some attribute for main window
        self.setWindowTitle("Phonebook")
        self.setWindowIcon(QIcon('/assets/phone-book.png'))
        self.setGeometry(100, 100, 765, 400)

        employees = [
            {'First Name': 'John', 'Last Name': 'Doe', 'Age': 25},
            {'First Name': 'Jane', 'Last Name': 'Doe', 'Age': 22},
            {'First Name': 'Alice', 'Last Name': 'Doe', 'Age': 22},
        ]
        contact_data = [
            {
                "First Name": "mobin",
                "Last Name": "banikarim",
                "Number": "09123456789",
                "Address": "Tehran, sina, p3"
            },
            {
                "First Name": "javad",
                "Last Name": "momtazan",
                "Number": "09123456789",
                "Address": "Tehran, vahid, p7"
            },
            {
                "First Name": "ali",
                "Last Name": "jahed",
                "Number": "09123456789",
                "Address": "Tehran, mehr, p2"
            },
        ]

        # Create Table
        self.table = QTableWidget(self)
        self.setCentralWidget(self.table)
        self.table.setColumnCount(4)
        self.table.setColumnWidth(0, 100)
        self.table.setColumnWidth(1, 100)
        self.table.setColumnWidth(2, 100)
        self.table.setColumnWidth(3, 200)

        # Fill table
        self.table.setHorizontalHeaderLabels(contact_data[0].keys())
        self.table.setRowCount(len(contact_data))
        row = 0
        for contact in contact_data:
            self.table.setItem(row, 0, QTableWidgetItem(contact["First Name"]))
            self.table.setItem(row, 1, QTableWidgetItem(contact["Last Name"]))
            self.table.setItem(row, 2, QTableWidgetItem(contact["Number"]))
            self.table.setItem(row, 3, QTableWidgetItem(contact["Address"]))
            row += 1

        # Add dock to the main window
        dock = QDockWidget("New Contact")
        dock.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, dock)

        # Create form to add to the dock
        form = QWidget()
        layout = QFormLayout(form)
        form.setLayout(layout)

        # Create Some widgets
        self.first_name = QLineEdit(form)
        self.first_name.setPlaceholderText("Necessary")
        self.last_name = QLineEdit(form)
        self.last_name.setPlaceholderText("Necessary")
        self.number = QLineEdit(form)
        self.number.setPlaceholderText("Necessary")
        self.address = QLineEdit(form)
        self.address.setPlaceholderText("Optional")

        # Add widgets to form layout
        layout.addRow("First Name:", self.first_name)
        layout.addRow("Last Name:", self.last_name)
        layout.addRow("Number:", self.number)
        layout.addRow("Address:", self.address)

        # Add a button to form layout
        btn_add = QPushButton("Add")
        btn_add.clicked.connect(self.add_contact)
        layout.addRow(btn_add)

        # Create toolbar and add it to the main window
        toolbar = QToolBar("main toolbar")
        toolbar.setIconSize(QSize(24, 24))
        self.addToolBar(toolbar)

        # add delete button to the toolbar
        self.delete_action = QAction(QIcon("./assets/delete.png"), "&Delete", self)
        self.delete_action.triggered.connect(self.delete)
        toolbar.addAction(self.delete_action)
        delete_label = QLabel("Delete Contact")
        toolbar.addWidget(delete_label)

        # add edit button to the toolbar
        pass

        # Add form to the dock
        dock.setWidget(form)

    def delete(self):
        """Delete Contact.

        delete selected contact in the table.
        :return: QMessageBox.warning()
        """
        current_row = self.table.currentRow()
        if current_row < 0:
            return QMessageBox.warning(self, "Warning", "Please select a record to delete")

        message = "\n".join(
         [
             "Are you sure that you want to delete the selected contact?",
             "",
             f"first name: {self.table.item(current_row, 0).text()}",
             f"last name: {self.table.item(current_row, 1).text()}",
             f"number: {self.table.item(current_row, 2).text()}",
             f"address: {self.table.item(current_row, 3).text()}",
         ]
        )
        button = QMessageBox.question(
            self,
            "Confirmation",
            message,
            QMessageBox.StandardButton.Yes |
            QMessageBox.StandardButton.No
        )
        if button == QMessageBox.StandardButton.Yes:
            self.table.removeRow(current_row)

    def valid(self):
        """Validate form.

        Checks if the form is valid and necessary fields are filled.
        :return:
        """
        first_name = self.first_name.text().strip()
        last_name = self.last_name.text().strip()
        number = self.number.text().strip()

        if not first_name:
            QMessageBox.critical(self, "Error", "Please enter the first name")
            self.first_name.setFocus()
            return False

        if not last_name:
            QMessageBox.critical(self, "Error", "Please enter the last name")
            self.last_name.setFocus()
            return False

        if not number:
            QMessageBox.critical(self, "Error", "Please enter the Number")
            self.number.setFocus()
            return False

        try:
            number = self.number.text().strip()
            digit = number.isdigit()
            if not digit:
                raise ValueError
        except ValueError:
            QMessageBox.critical(
                self,
                "Error",
                "Please enter a valid number"
            )
            self.number.setFocus()
            return False

        if not 7 < len(number) < 12:
            QMessageBox.critical(
                self,
                "Error",
                "The phone number must be between 8 and 11 digits"
            )
            return False

        return True

    def reset(self):
        """Reset form widgets."""
        self.first_name.clear()
        self.last_name.clear()
        self.number.clear()

    def add_contact(self):
        """Add new contact."""
        if not self.valid():
            return

        row = self.table.rowCount()
        self.table.insertRow(row)
        self.table.setItem(
            row,
            0,
            QTableWidgetItem(self.first_name.text().strip())
            )
        self.table.setItem(
            row,
            1,
            QTableWidgetItem(self.last_name.text())
        )
        self.table.setItem(
            row,
            2,
            QTableWidgetItem(self.number.text())
        )
        self.table.setItem(
            row,
            3,
            QTableWidgetItem(self.address.text())
        )

        self.reset()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
