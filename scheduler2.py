import random
import json
import tkinter as tk
from tkinter import messagebox, Toplevel


class Employee:
    def __init__(self, name, hourly_pay, open_hours, days_off):
        self.name = name
        self.hourly_pay = hourly_pay
        self.open_hours = open_hours
        self.days_off = days_off


class Department:
    def __init__(self, name):
        self.name = name
        self.budget = 0
        self.employees = []


class Chromosome:
    def __init__(self, num_employees):
        self.schedule = []
        self.num_employees = num_employees
        self.days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        self.hours_of_day = 24

        for _ in range(self.num_employees):
            employee_schedule = []
            for _ in range(len(self.days_of_week)):
                shifts = []
                for _ in range(self.hours_of_day):
                    shift = random.choice(['morning', 'evening', 'night'])
                    shifts.append(shift)
                employee_schedule.append(shifts)
            self.schedule.append(employee_schedule)

    def crossover(self, other):
        child_schedule = []

        for i in range(self.num_employees):
            employee_schedule = []
            for j in range(len(self.days_of_week)):
                shifts = []
                for k in range(self.hours_of_day):
                    shift = random.choice([self.schedule[i][j][k], other.schedule[i][j][k]])
                    shifts.append(shift)
                employee_schedule.append(shifts)
            child_schedule.append(employee_schedule)

        child = Chromosome(self.num_employees)
        child.schedule = child_schedule

        return child

    def mutate(self, mutation_rate):
        for i in range(self.num_employees):
            for j in range(len(self.days_of_week)):
                for k in range(self.hours_of_day):
                    if random.random() < mutation_rate:
                        self.schedule[i][j][k] = random.choice(['morning', 'evening', 'night'])

    def calculate_fitness(self):
        # Calculate the fitness score of the chromosome
        # Add your fitness calculation logic here
        return random.randint(1, 100)

    def get_schedule(self):
        return self.schedule


class ScheduleApp:
    def __init__(self, root):
        self.root = root
        self.departments = []
        self.current_department = None
        self.current_screen = 0  # Track the current screen index

        self.root.title("Employee Scheduler")
        self.root.geometry("300x200")

        self.label = None
        self.department_name_label = None
        self.department_name_input = None
        self.employee_name_label = None
        self.employee_name_input = None
        self.hourly_pay_label = None
        self.hourly_pay_input = None
        self.open_hours_label = None
        self.open_hours_input = None
        self.days_off_label = None
        self.days_off_input = None
        self.add_employee_button = None
        self.schedule_button = None
        self.employee_list_button = None
        self.navigation_frame = None
        self.back_button = None
        self.next_button = None
        self.budget_label = None
        self.budget_input = None

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

        self.create_department_button = tk.Button(
            self.root, text="Create Department", command=self.create_department
        )
        self.create_department_button.pack()

    def create_department(self):
        department_name = self.department_name_input.get()
        budget = self.budget_input.get()

        if not department_name or not budget:
            messagebox.showerror("Error", "Please enter department name and budget.")
            return

        department = Department(department_name)
        department.budget = budget
        self.departments.append(department)
        self.save_departments_to_file()

        self.current_department = department
        self.show_employee_layout()

    def save_departments_to_file(self):
        data = {"departments": []}

        for department in self.departments:
            department_data = {
                "name": department.name,
                "budget": department.budget,
                "employees": [employee.__dict__ for employee in department.employees],
            }
            data["departments"].append(department_data)

        with open("departments.json", "w") as file:
            json.dump(data, file)

    def show_department_layout(self):
        self.clear_widgets()

        self.label = tk.Label(self.root, text="Select Department")
        self.label.pack()

        for department in self.departments:
            button = tk.Button(self.root, text=department.name, command=lambda dep=department: self.select_department(dep))
            button.pack()

        self.navigation_frame = tk.Frame(self.root)
        self.navigation_frame.pack()

        self.next_button = tk.Button(self.navigation_frame, text="Next", command=self.next_screen)
        self.next_button.pack(side=tk.RIGHT)

    def select_department(self, department):
        self.current_department = department
        self.show_employee_layout()

    def show_employee_layout(self):
        self.clear_widgets()

        self.label = tk.Label(self.root, text="Enter Employee Details")
        self.label.pack()

        self.employee_name_label = tk.Label(self.root, text="Employee Name:")
        self.employee_name_label.pack()
        self.employee_name_input = tk.Entry(self.root)
        self.employee_name_input.pack()

        self.hourly_pay_label = tk.Label(self.root, text="Hourly Pay:")
        self.hourly_pay_label.pack()
        self.hourly_pay_input = tk.Entry(self.root)
        self.hourly_pay_input.pack()

        self.open_hours_label = tk.Label(self.root, text="Open Hours:")
        self.open_hours_label.pack()
        self.open_hours_input = tk.Entry(self.root)
        self.open_hours_input.pack()

        self.days_off_label = tk.Label(self.root, text="Days Off:")
        self.days_off_label.pack()
        self.days_off_input = tk.Entry(self.root)
        self.days_off_input.pack()

        self.add_employee_button = tk.Button(self.root, text="Add Employee", command=self.add_employee)
        self.add_employee_button.pack()

        self.schedule_button = tk.Button(self.root, text="Generate Schedule", command=self.show_schedule_popup)
        self.schedule_button.pack()

        self.employee_list_button = tk.Button(self.root, text="Employee List", command=self.display_employee_list)
        self.employee_list_button.pack()

        self.navigation_frame = tk.Frame(self.root)
        self.navigation_frame.pack()

        self.back_button = tk.Button(self.navigation_frame, text="Back", command=self.previous_screen)
        self.back_button.pack(side=tk.LEFT)
        self.next_button = tk.Button(self.navigation_frame, text="Next", command=self.next_screen)
        self.next_button.pack(side=tk.RIGHT)

    def add_employee(self):
        name = self.employee_name_input.get()
        hourly_pay = self.hourly_pay_input.get()
        open_hours = self.open_hours_input.get()
        days_off = self.days_off_input.get()

        if not name or not hourly_pay or not open_hours or not days_off:
            messagebox.showerror("Error", "Please enter all employee details.")
            return

        employee = Employee(name, hourly_pay, open_hours, days_off)
        self.current_department.employees.append(employee)
        self.save_departments_to_file()

        messagebox.showinfo("Success", "Employee added successfully.")

        self.employee_name_input.delete(0, tk.END)
        self.hourly_pay_input.delete(0, tk.END)
        self.open_hours_input.delete(0, tk.END)
        self.days_off_input.delete(0, tk.END)

    def show_schedule_popup(self):
        num_employees = len(self.current_department.employees)
        population_size = 10
        mutation_rate = 0.01

        population = []

        for _ in range(population_size):
            chromosome = Chromosome(num_employees)
            population.append(chromosome)

        for chromosome in population:
            chromosome.calculate_fitness()

        best_chromosome = max(population, key=lambda x: x.fitness)

        popup = tk.Toplevel()
        popup.title("Schedule Generation")
        popup.geometry("300x200")

        label = tk.Label(popup, text="Best Schedule")
        label.pack()

        schedule_text = f"Fitness Score: {best_chromosome.fitness}"
        schedule_label = tk.Label(popup, text=schedule_text)
        schedule_label.pack()

        close_button = tk.Button(popup, text="Close", command=popup.destroy)
        close_button.pack()

    def display_employee_list(self):
        employee_list = "\n".join([employee.name for employee in self.current_department.employees])
        messagebox.showinfo("Employee List", f"Employees in {self.current_department.name}:\n{employee_list}")

    def previous_screen(self):
        self.navigation_frame.pack_forget()
        self.navigation_frame = None

        self.show_department_layout()

    def next_screen(self):
        self.navigation_frame.pack_forget()
        self.navigation_frame = None

        self.show_employee_layout()

    def clear_widgets(self):
        widgets = [
            self.label,
            self.department_name_label,
            self.department_name_input,
            self.budget_label,
            self.budget_input,
            self.employee_name_label,
            self.employee_name_input,
            self.hourly_pay_label,
            self.hourly_pay_input,
            self.open_hours_label,
            self.open_hours_input,
            self.days_off_label,
            self.days_off_input,
            self.add_employee_button,
            self.schedule_button,
            self.employee_list_button,
            self.navigation_frame,
            self.back_button,
            self.next_button,
        ]

        for widget in widgets:
            if widget:
                widget.pack_forget()


if __name__ == "__main__":
    root = tk.Tk()
    app = ScheduleApp(root)
    root.mainloop()


