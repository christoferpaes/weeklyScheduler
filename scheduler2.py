import tkinter as tk
from tkinter import messagebox
import json


class Employee:
    def __init__(self, name, hourly_pay, open_hours):
        self.name = name
        self.hourly_pay = hourly_pay
        self.open_hours = open_hours


class ScheduleApp:
    def __init__(self, root):
        self.root = root
        self.employees = []

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
                self.employees = json.load(file)
        except FileNotFoundError:
            messagebox.showinfo("Retrieve Records", "No records found.")
        else:
            messagebox.showinfo("Retrieve Records", "Records retrieved successfully.")

    def start_from_scratch(self):
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

        self.submit_button = tk.Button(self.root, text="Submit", command=self.insert_employee)
        self.submit_button.pack()

        self.calculate_button = tk.Button(self.root, text="Calculate", command=self.calculate_schedule)
        self.calculate_button.pack()
        self.calculate_button.config(state=tk.DISABLED)

    def insert_employee(self):
        name = self.name_input.get()
        hourly_pay = float(self.hourly_pay_input.get())
        open_hours = self.open_hours_input.get()

        self.employees.append(Employee(name, hourly_pay, open_hours))

        self.name_input.delete(0, tk.END)
        self.hourly_pay_input.delete(0, tk.END)
        self.open_hours_input.delete(0, tk.END)

        messagebox.showinfo("Employee Added", "Employee details added successfully.")

        if len(self.employees) >= 2:
            self.calculate_button.config(state=tk.NORMAL)

    def clear_widgets(self):
        for widget in self.root.winfo_children():
            widget.pack_forget()

    def save_records(self):
        with open("employees.json", "w") as file:
            json.dump(self.employees, file, indent=4)
        messagebox.showinfo("Save Records", "Records saved successfully.")

    def calculate_schedule(self):
        # Perform the schedule calculation
        # Placeholder code for demonstration
        messagebox.showinfo("Schedule Calculation", "Schedule calculated successfully.")

    def run(self):
        self.root.protocol("WM_DELETE_WINDOW", self.save_records)
        self.root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    app = ScheduleApp(root)
    app.run()
