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
        self.employees = []


class ScheduleApp:
    def __init__(self, root):
        self.root = root
        self.departments = []
        self.current_department = None

        self.root.title("Employee Scheduler")
        self.root.geometry("300x200")

        self.label = None
        self.check_first_time()

    def check_first_time(self):
        try:
            with open("departments.json", "r") as file:
                data = json.load(file)
                if "departments" in data:
                    self.departments = [
                        Department(department_data["name"]) for department_data in data["departments"]
                    ]
        except FileNotFoundError:
            pass

        if not self.departments:
            self.collect_department_data()
        else:
            self.show_department_layout()

    def collect_department_data(self):
        self.clear_widgets()

        self.label = tk.Label(self.root, text="Enter Department Details")
        self.label.pack()

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

        department = Department(department_name)
        department.budget = budget

        self.departments.append(department)

        self.department_name_input.delete(0, tk.END)
        self.budget_input.delete(0, tk.END)

        self.show_department_layout()

    def show_department_layout(self):
        self.clear_widgets()

        self.label = tk.Label(self.root, text="Select Department")
        self.label.pack()

        self.department_dropdown = tk.OptionMenu(self.root, self.current_department, *self.departments, command=self.show_employee_layout)
        self.department_dropdown.pack()

    def show_employee_layout(self, department):
        self.clear_widgets()

        self.current_department = department

        self.label = tk.Label(self.root, text="Enter Employee Details")
        self.label.pack()

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
        self.current_department.employees.append(employee)

        self.name_input.delete(0, tk.END)
        self.hourly_pay_input.delete(0, tk.END)
        self.open_hours_input.delete(0, tk.END)

        messagebox.showinfo("Employee Added", "Employee details added successfully.")

    def clear_widgets(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    app = ScheduleApp(root)
    app.run()
