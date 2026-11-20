import csv

def bonus(salary, rate=0.1, *extras, **options):
    result = salary * rate + sum(extras)

    if "cap" in options:
        result = min(result, options["cap"])

    return result


class InvalidSalaryError(Exception):
    pass



class Employee:

    def __init__(self, name, salary):

        if salary < 0:
            raise InvalidSalaryError(f"Invalid salary: {salary}")

        self.name = name
        self.salary = salary

    def annual_salary(self):
        return self.salary * 12

    def get_details(self):
        return f"Name: {self.name}, Salary: {self.salary}"



class Manager(Employee):

    def __init__(self, name, salary, team_size):
        super().__init__(name, salary)
        self.team_size = team_size

    def get_details(self):
        return (
            f"Name: {self.name}, Salary: {self.salary}, "
            f"Team Size: {self.team_size}"
        )



bonus(50000, 0.1, 1000, 500)
bonus(50000, 0.1, 1000, cap=4000)

emp = Employee("Arun", 30000)
emp.annual_salary()
emp.get_details()

manager = Manager("Priya", 60000, 5)
manager.get_details()



with open("employees.csv", "r") as file:
    reader = csv.DictReader(file)
    employees = list(reader)



above_50000 = [
    emp["name"]
    for emp in employees
    if int(emp["salary"]) > 50000
]

print("Above 50000:", above_50000)


salaries = [int(emp["salary"]) for emp in employees]

new_salaries = list(
    map(lambda salary: round(salary * 1.10, 2), salaries)
)



chennai_employees = list(
    filter(
        lambda emp: emp["city"] == "Chennai",
        employees
    )
)

chennai_names = [
    emp["name"]
    for emp in chennai_employees
]

print("Chennai:", chennai_names)


salary_list = [30000, 0, 45000, 60000, 75000, 90000, 52000]

for salary in salary_list:

    if salary == 0:
        continue

    if salary > 85000:
        break


try:
    emp = Employee("Test", -500)

except InvalidSalaryError as e:
    print("Error:", e)

finally:
    print("Transaction finished")
