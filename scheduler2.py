import tkinter as tk
from tkinter import messagebox
import json


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
    def __init__(self, root):
        self.root = root
        self.employees = []
        self.department = None

        self.root.title("Employee Scheduler")
        self.root.geometry("300x200")

        self.label = tk.Label(root, text="Employee Scheduler", font=("Arial", 20, "bold"), pady=10)
        self.label.pack()

        self.retrieve_button = tk.Button(root, text="Retrieve Records", command=self.retrieve_records)
        self.retrieve_button.pack()

        self.new_button = tk.Button(root, text="Start from Scratch", command=self.start_from_scratch)
        self.new_button.pack()

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
            messagebox.showinfo("Retrieve Records", "No records found.")
        else:
            messagebox.showinfo("Retrieve Records", "Records retrieved successfully.")

    def start_from_scratch(self):
        self.collect_department_data()

    def collect_department_data(self):
        self.clear_widgets()

        self.label.config(text="Enter Department Details")

        self.department_name_label = tk.Label(self.root, text="Department Name:")
        self.department_name_label.pack()
        self.department_name_input = tk.Entry(self.root)
        self.department_name_input.pack()

        self.budget_label = tk.Label(self.root, text="Budget:")
        self.budget_label.pack()
        self.budget_input = tk.Entry(self.root)
        self.budget_input.pack()

        self.submit_department_button = tk.Button(self.root, text="Submit", command=self.insert_department)
        self.submit_department_button.pack()

    def insert_department(self):
        department_name = self.department_name_input.get()
        budget = float(self.budget_input.get())

        self.department = Department(department_name)
        self.department.budget = budget

        self.department_name_input.delete(0, tk.END)
        self.budget_input.delete(0, tk.END)

        messagebox.showinfo("Department Added", "Department details added successfully.")

        self.collect_employee_data()

    def collect_employee_data(self):
        self.clear_widgets()

        self.label.config(text="Enter Employee Details")

        self.name_label = tk.Label(self.root, text="Name:")
        self.name_label.pack()
        self.name_input = tk.Entry(self.root)
        self.name_input.pack()

        self.hourly_pay_label = tk.Label(self.root, text="Hourly Pay:")
        self.hourly_pay_label.pack()
        self.hourly_pay_input = tk.Entry(self.root)
        self.hourly_pay_input.pack()

        self.open_hours_label = tk.Label(self.root, text="Open Hours:")
        self.open_hours_label.pack()
        self.open_hours_input = tk.Entry(self.root)
        self.open_hours_input.pack()
        self.open_hours_note = tk.Label(self.root, text="(e.g., 9 AM - 5 PM)")
        self.open_hours_note.pack()

        self.submit_employee_button = tk.Button(self.root, text="Submit", command=self.insert_employee)
        self.submit_employee_button.pack()

    def insert_employee(self):
        name = self.name_input.get()
        hourly_pay = float(self.hourly_pay_input.get())
        open_hours = self.open_hours_input.get()

        employee = Employee(name, hourly_pay, open_hours)
        self.employees.append(employee)

        self.name_input.delete(0, tk.END)
        self.hourly_pay_input.delete(0, tk.END)
        self.open_hours_input.delete(0, tk.END)

        messagebox.showinfo("Employee Added", "Employee details added successfully.")

        if len(self.employees) >= 2:
            self.collect_budget_data()

    def collect_budget_data(self):
        self.clear_widgets()

        self.label.config(text="Enter Budget")

        self.budget_label = tk.Label(self.root, text="Budget:")
        self.budget_label.pack()
        self.budget_input = tk.Entry(self.root)
        self.budget_input.pack()

        self.submit_budget_button = tk.Button(self.root, text="Submit", command=self.generate_schedule)
        self.submit_budget_button.pack()

    def generate_schedule(self):
        budget = float(self.budget_input.get())

        schedule_data = {
            "department": {"name": self.department.name, "budget": self.department.budget},
            "employees": [
                {"name": employee.name, "hourly_pay": employee.hourly_pay, "open_hours": employee.open_hours.split(" - ")}
                for employee in self.employees
            ],
            "budget": budget,
        }

        with open("employees.json", "w") as file:
            json.dump(schedule_data, file, indent=4)

        messagebox.showinfo("Schedule Generated", "Schedule generated successfully.")

    def clear_widgets(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def run(self):
        self.root.protocol("WM_DELETE_WINDOW", self.save_records)
        self.root.mainloop()

    def save_records(self):
        if self.department and self.employees:
            budget = float(self.budget_input.get()) if self.budget_input.get() else 0

            schedule_data = {
                "department": {"name": self.department.name, "budget": self.department.budget},
                "employees": [
                    {"name": employee.name, "hourly_pay": employee.hourly_pay, "open_hours": employee.open_hours.split(" - ")}
                    for employee in self.employees
                ],
                "budget": budget,
            }

            with open("employees.json", "w") as file:
                json.dump(schedule_data, file, indent=4)

        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = ScheduleApp(root)
    app.run()
