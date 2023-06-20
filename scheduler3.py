import json
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox


class Employee:
    def __init__(self, name, hourly_pay, open_hours):
        self.name = name
        self.hourly_pay = hourly_pay
        self.open_hours = open_hours


class Department:
    def __init__(self, name):
        self.name = name
        self.budget = 0


class ScheduleApp(QWidget):
    def __init__(self):
        super().__init__()

        self.employees = []
        self.department = None

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Employee Scheduler")
        self.setGeometry(400, 200, 300, 200)

        self.label = QLabel("Employee Scheduler", self)
        self.label.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 20px;")

        self.retrieve_button = QPushButton("Retrieve Records", self)
        self.retrieve_button.clicked.connect(self.retrieve_records)

        self.new_button = QPushButton("Start from Scratch", self)
        self.new_button.clicked.connect(self.start_from_scratch)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.retrieve_button)
        layout.addWidget(self.new_button)
        self.setLayout(layout)

        self.show()

    def retrieve_records(self):
        try:
            with open("employees.json", "r") as file:
                data = json.load(file)
                self.employees = [
                    Employee(**employee_data) for employee_data in data["employees"]
                ]
                self.department = Department(data["department"]["name"])
                self.department.budget = data["department"]["budget"]
        except FileNotFoundError:
            QMessageBox.warning(self, "Error", "No records found.")
        else:
            QMessageBox.information(self, "Success", "Records retrieved successfully.")

    def start_from_scratch(self):
        self.collect_department_data()

    def collect_department_data(self):
        self.clear_layout()

        self.label.setText("Enter Department Details")

        self.department_name_label = QLabel("Department Name:", self)
        self.department_name_input = QLineEdit(self)

        self.budget_label = QLabel("Budget:", self)
        self.budget_input = QLineEdit(self)

        self.submit_button = QPushButton("Submit", self)
        self.submit_button.clicked.connect(self.collect_employee_data)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.department_name_label)
        layout.addWidget(self.department_name_input)
        layout.addWidget(self.budget_label)
        layout.addWidget(self.budget_input)
        layout.addWidget(self.submit_button)
        self.setLayout(layout)

    def collect_employee_data(self):
        department_name = self.department_name_input.text()
        budget = float(self.budget_input.text())

        self.department = Department(department_name)
        self.department.budget = budget

        QMessageBox.information(self, "Success", "Department details added successfully.")

        self.collect_employee_details()

    def collect_employee_details(self):
        self.clear_layout()

        self.label.setText("Enter Employee Details")

        self.name_label = QLabel("Name:", self)
        self.name_input = QLineEdit(self)

        self.hourly_pay_label = QLabel("Hourly Pay:", self)
        self.hourly_pay_input = QLineEdit(self)

        self.open_hours_label = QLabel("Open Hours:", self)
        self.open_hours_input = QLineEdit(self)

        self.submit_button = QPushButton("Submit", self)
        self.submit_button.clicked.connect(self.add_employee)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)
        layout.addWidget(self.hourly_pay_label)
        layout.addWidget(self.hourly_pay_input)
        layout.addWidget(self.open_hours_label)
        layout.addWidget(self.open_hours_input)
        layout.addWidget(self.submit_button)
        self.setLayout(layout)

    def add_employee(self):
        name = self.name_input.text()
        hourly_pay = float(self.hourly_pay_input.text())
        open_hours = self.open_hours_input.text()

        employee = Employee(name, hourly_pay, open_hours)
        self.employees.append(employee)

        QMessageBox.information(self, "Success", "Employee details added successfully.")

        self.collect_employee_details()

    def save_records(self):
        data = {
            "department": {
                "name": self.department.name,
                "budget": self.department.budget,
            },
            "employees": [
                {
                    "name": employee.name,
                    "hourly_pay": employee.hourly_pay,
                    "open_hours": employee.open_hours,
                }
                for employee in self.employees
            ],
        }

        with open("employees.json", "w") as file:
            json.dump(data, file, indent=4)

        QMessageBox.information(self, "Success", "Records saved successfully.")

    def clear_layout(self):
        while self.layout().count():
            child = self.layout().takeAt(0)
            if child.widget():
                child.widget().deleteLater()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    schedule_app = ScheduleApp()
    sys.exit(app.exec_())
