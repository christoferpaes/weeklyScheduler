import json
from tkinter import messagebox


class Employee:
    def __init__(self, name, hourly_pay, open_hours):
        self.name = name
        self.hourly_pay = hourly_pay
        self.open_hours = open_hours


class Department:
    def __init__(self, name):
        self.name = name
        self.budget = 0


class ScheduleApp:
    def __init__(self):
        self.employees = []
        self.department = None

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
            print("No records found.")
        else:
            print("Records retrieved successfully.")

    def start_from_scratch(self):
        self.collect_department_data()

    def collect_department_data(self):
        department_name = input("Enter Department Name: ")
        budget = float(input("Enter Budget: "))

        self.department = Department(department_name)
        self.department.budget = budget

        print("Department details added successfully.")

        self.collect_employee_data()

    def collect_employee_data(self):
        name = input("Enter Employee Name: ")
        hourly_pay = float(input("Enter Hourly Pay: "))
        open_hours = input("Enter Open Hours (e.g., 9 AM - 5 PM): ")

        employee = Employee(name, hourly_pay, open_hours)
        self.employees.append(employee)

        print("Employee details added successfully.")

        if len(self.employees) >= 2:
            self.collect_budget_data()

    def collect_budget_data(self):
        budget = float(input("Enter Budget: "))

        self.generate_schedule(budget)

    def generate_schedule(self, budget):
        schedule_data = {
            "department": {"name": self.department.name, "budget": self.department.budget},
            "employees": [
                {"name": employee.name, "hourly_pay": employee.hourly_pay, "open_hours": employee.open_hours}
                for employee in self.employees
            ],
            "budget": budget,
        }

        with open("employees.json", "w") as file:
            json.dump(schedule_data, file, indent=4)

        print("Schedule generated successfully.")

    def save_records(self):
        if self.department and self.employees:
            budget = float(input("Enter Budget: ")) if self.department.budget else 0

            schedule_data = {
                "department": {"name": self.department.name, "budget": self.department.budget},
                "employees": [
                    {"name": employee.name, "hourly_pay": employee.hourly_pay, "open_hours": employee.open_hours}
                    for employee in self.employees
                ],
                "budget": budget,
            }

            with open("employees.json", "w") as file:
                json.dump(schedule_data, file, indent=4)

        print("Records saved successfully.")

    def run(self):
        choice = input("1. Retrieve Records\n2. Start from Scratch\nEnter your choice (1 or 2): ")

        if choice == "1":
            self.retrieve_records()
        elif choice == "2":
            self.start_from_scratch()
        else:
            print("Invalid choice.")

        self.save_records()


if __name__ == "__main__":
    app = ScheduleApp()
    app.run()

