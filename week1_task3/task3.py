import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

marks = np.array([
    [85, 78, 92],
    [70, 88, 80],
    [90, 95, 89],
    [60, 72, 75]
])

student_avg = np.mean(marks, axis=1)
subject_avg = np.mean(marks, axis=0)

grace_marks = marks + 5

weights = np.array([0.3, 0.3, 0.4])
weighted_scores = np.dot(grace_marks, weights)

df = pd.read_csv("employees.csv")

print("Employee Data:")
print(df)

print("\nDataFrame Information:")
df.info()

print("\nStatistical Description:")
print(df.describe())

print("\nUsing loc:")
print(df.loc[0:2, ["name", "department", "salary"]])

print("\nUsing iloc:")
print(df.iloc[0:3, 0:3])

print("\nSalary above 50000:")
high_salary = df[df["salary"] > 50000]
print(high_salary[["name", "salary"]])

messy_df = df.copy()

messy_df.loc[0, "salary"] = np.nan
messy_df.loc[1, "salary"] = np.nan

messy_df = pd.concat(
    [messy_df, messy_df.iloc[[2]]],
    ignore_index=True
)

messy_df.to_csv("messy_employees.csv", index=False)

print("\nBefore Cleaning:")
print("Total rows:", len(messy_df))
print("Missing salaries:", messy_df["salary"].isnull().sum())

cleaned_df = messy_df.drop_duplicates().copy()

median_salary = cleaned_df["salary"].median()
cleaned_df["salary"] = cleaned_df["salary"].fillna(median_salary)

cleaned_df["id"] = cleaned_df["id"].astype(int)
cleaned_df["salary"] = cleaned_df["salary"].astype(int)

cleaned_df.to_csv("cleaned_employees.csv", index=False)

print("\nAfter Cleaning:")
print("Total rows:", len(cleaned_df))
print("Missing salaries:", cleaned_df["salary"].isnull().sum())
print("Duplicate rows:", cleaned_df.duplicated().sum())

department_summary = cleaned_df.groupby("department").agg(
    Headcount=("id", "count"),
    Average_Salary=("salary", "mean"),
    Maximum_Salary=("salary", "max")
)

print("\nDepartment Summary:")
print(department_summary)


departments_df = pd.read_csv("departments.csv")

inner_join = pd.merge(
    cleaned_df,
    departments_df,
    on="department",
    how="inner"
)

print("\nINNER JOIN:")
print(inner_join)

left_join = pd.merge(
    cleaned_df,
    departments_df,
    on="department",
    how="left"
)

print("\nLEFT JOIN:")
print(left_join)

outer_join = pd.merge(
    cleaned_df,
    departments_df,
    on="department",
    how="outer"
)

print("\nOUTER JOIN:")
print(outer_join)

departments_without_employees = outer_join[
    outer_join["id"].isna()
]["department"].unique()


os.makedirs("charts", exist_ok=True)


plt.figure(figsize=(8, 5))
department_summary["Headcount"].plot(
    kind="bar",
    label="Headcount"
)
plt.title("Employee Headcount by Department")
plt.xlabel("Department")
plt.ylabel("Number of Employees")
plt.legend()
plt.tight_layout()
plt.savefig("charts/department_bar.png")
plt.close()

plt.figure(figsize=(8, 5))
plt.hist(
    cleaned_df["salary"],
    bins=5,
    label="Employee Salary"
)
plt.title("Employee Salary Distribution")
plt.xlabel("Salary")
plt.ylabel("Frequency")
plt.legend()
plt.tight_layout()
plt.savefig("charts/salary_histogram.png")
plt.close()

plt.figure(figsize=(8, 5))
plt.scatter(
    cleaned_df["id"],
    cleaned_df["salary"],
    label="Employees"
)
plt.title("Employee ID vs Salary")
plt.xlabel("Employee ID")
plt.ylabel("Salary")
plt.legend()
plt.tight_layout()
plt.savefig("charts/salary_scatter.png")
plt.close()

plt.figure(figsize=(8, 5))
plt.plot(
    cleaned_df["name"],
    cleaned_df["salary"],
    marker="o",
    label="Salary"
)
plt.title("Employee Salary Comparison")
plt.xlabel("Employee Name")
plt.ylabel("Salary")
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("charts/salary_line.png")
plt.close()

headcounts = cleaned_df["department"].value_counts()

print("\nStudent averages:", student_avg)

print(
    f"Headcount: Sales {headcounts.get('Sales', 0)} | "
    f"HR {headcounts.get('HR', 0)} | "
    f"IT {headcounts.get('IT', 0)} | "
    f"Finance {headcounts.get('Finance', 0)}"
)

print("Outer join: department with no employees listed")

for department in departments_without_employees:
    print(department)
