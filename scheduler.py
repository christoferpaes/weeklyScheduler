import sqlite3
import pandas as pd
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout, QMessageBox


class Employee:
    def __init__(self, name, hourly_pay):
        self.name = name
        self.hourly_pay = hourly_pay


class ScheduleApp(QWidget):
    def __init__(self):
        super().__init__()

        # Create or connect to the SQLite database
        self.conn = sqlite3.connect('employees.db')
        self.cursor = self.conn.cursor()

        # Create the employees table if it doesn't exist
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS employees
                              (name TEXT, hourly_pay REAL)''')

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Employee Scheduler")
        self.setGeometry(400, 200, 300, 200)

        # Create GUI elements
        self.label = QLabel("Employee Scheduler", self)
        self.label.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 20px;")

        self.retrieve_button = QPushButton("Retrieve Records", self)
        self.retrieve_button.clicked.connect(self.retrieve_records)

        self.new_button = QPushButton("Start from Scratch", self)
        self.new_button.clicked.connect(self.start_from_scratch)

        # Create layout and add elements
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.retrieve_button)
        layout.addWidget(self.new_button)
        self.setLayout(layout)

        self.show()

    def retrieve_records(self):
        self.retrieve_button.setDisabled(True)
        self.new_button.setDisabled(True)

        # Retrieve employee data from the database
        self.cursor.execute("SELECT name, hourly_pay FROM employees")
        employee_data = self.cursor.fetchall()
        employees = [Employee(name, hourly_pay) for name, hourly_pay in employee_data]

        # Close the database connection
        self.conn.close()

        self.display_schedule(employees)

    def start_from_scratch(self):
        self.retrieve_button.setDisabled(True)
        self.new_button.setDisabled(True)

        # Close the database connection
        self.conn.close()

        self.collect_employee_data()

    def collect_employee_data(self):
        self.clear_layout()

        self.label.setText("Enter Employee Details")

        self.name_label = QLabel("Name:", self)
        self.name_input = QLineEdit(self)

        self.hourly_pay_label = QLabel("Hourly Pay:", self)
        self.hourly_pay_input = QLineEdit(self)

        self.submit_button = QPushButton("Submit", self)
        self.submit_button.clicked.connect(self.insert_employee)

        layout = QVBoxLayout()
        layout.addWidget(self.label)

        form_layout = QGridLayout()
        form_layout.addWidget(self.name_label, 0, 0)
        form_layout.addWidget(self.name_input, 0, 1)
        form_layout.addWidget(self.hourly_pay_label, 1, 0)
        form_layout.addWidget(self.hourly_pay_input, 1, 1)
        layout.addLayout(form_layout)

        layout.addWidget(self.submit_button)
        self.setLayout(layout)

    def insert_employee(self):
        name = self.name_input.text()
        hourly_pay = float(self.hourly_pay_input.text())

        # Insert employee data into the employees table
        self.cursor.execute("INSERT INTO employees VALUES (?, ?)", (name, hourly_pay))
        self.conn.commit()

        self.name_input.clear()
        self.hourly_pay_input.clear()

        QMessageBox.information(self, "Success", "Employee record added successfully!")

    def display_schedule(self, employees):
        self.clear_layout()

        self.label.setText("Enter Scheduling Details")

        self.hours_label = QLabel("Hours Available (5am-10pm):", self)
        self.hours_input = QLineEdit(self)
        self.hours_input.setText("17")  # Adjusted for 5am to 10pm (17 hours)

        self.coverage_label = QLabel("Coverage Requirements:", self)
        self.coverage_input = QLineEdit(self)

        self.budget_label = QLabel("Budget:", self)
        self.budget_input = QLineEdit(self)

        self.submit_button = QPushButton("Generate Schedule", self)
        self.submit_button.clicked.connect(lambda: self.generate_schedule(employees))

        layout = QVBoxLayout()
        layout.addWidget(self.label)

        form_layout = QGridLayout()
        form_layout.addWidget(self.hours_label, 0, 0)
        form_layout.addWidget(self.hours_input, 0, 1)
        form_layout.addWidget(self.coverage_label, 1, 0)
        form_layout.addWidget(self.coverage_input, 1, 1)
        form_layout.addWidget(self.budget_label, 2, 0)
        form_layout.addWidget(self.budget_input, 2, 1)
        layout.addLayout(form_layout)

        layout.addWidget(self.submit_button)
        self.setLayout(layout)

    def generate_schedule(self, employees):
        hours_available = float(self.hours_input.text())
        coverage_requirements = {}  # Placeholder for coverage requirements
        budget = float(self.budget_input.text())

        # Calculate the schedule based on adjusted time frame and hourly pay
        hourly_pay_schedule = hours_available * len(employees)
        total_budget = budget * hourly_pay_schedule

        # Display the schedule using pandas DataFrame
        schedule_data = {
            'Employee': [emp.name for emp in employees],
            'Salary': [emp.hourly_pay * hours_available for emp in employees]
        }
        schedule_df = pd.DataFrame(schedule_data)
        schedule_df['Total Salary'] = schedule_df['Salary'] * 30  # Assuming 30 days per month

        QMessageBox.information(self, "Generated Schedule", f"\nGenerated Schedule:\n\n{schedule_df.to_string(index=False)}\n\n"
                                                            f"Hourly Pay Schedule: {hourly_pay_schedule}\n"
                                                            f"Total Budget: {total_budget}")

        # Exit the application
        QApplication.quit()

    def clear_layout(self):
        while self.layout().count():
            child = self.layout().takeAt(0)
            if child.widget():
                child.widget().deleteLater()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    schedule_app = ScheduleApp()
    sys.exit(app.exec_())
