import csv
import json
import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")

employees = []

with open("employees.csv", "r") as file:
    reader = csv.DictReader(file)

    for row in reader:
        employees.append(row)


with open("employees.json", "w") as file:
    json.dump(employees, file, indent=4)


high_earners = []

for employee in employees:
    if int(employee["salary"]) > 50000:
        high_earners.append(employee)

with open("high_earners.csv", "w", newline="") as file:
    writer = csv.DictWriter(
        file,
        fieldnames=employees[0].keys()
    )
    writer.writeheader()
    writer.writerows(high_earners)

print(f"Rows read: {len(employees)} | High earners: {len(high_earners)}")


url = "https://jsonplaceholder.typicode.com/users"

try:
    response = requests.get(
        url,
        headers={"X-API-Key": API_KEY} if API_KEY else {},
        timeout=5
    )
    response.raise_for_status()

    users = response.json()

    user = users[0]
    print(f'{user["id"]} - {user["name"]} - {user["email"]}')

except requests.exceptions.Timeout:
    pass
except requests.exceptions.ConnectionError:
    pass
except requests.exceptions.HTTPError:
    pass

url = "https://jsonplaceholder.typicode.com/users/9999"

try:
    response = requests.get(url, timeout=5)

    if response.status_code == 404:
        print("/users/9999 -> 404 Not found")
    else:
        response.raise_for_status()

except requests.exceptions.Timeout:
    pass
except requests.exceptions.ConnectionError:
    pass
except requests.exceptions.HTTPError:
    pass


url = "https://jsonplaceholder.typicode.com/users"

try:
    response = requests.get(url, timeout=5)
    response.raise_for_status()

    users = response.json()
    user_details = []

    for user in users:
        details = {
            "id": user.get("id"),
            "name": user.get("name"),
            "email": user.get("email"),
            "city": user.get("address", {}).get("city"),
            "company": user.get("company", {}).get("name")
        }

        user_details.append(details)

    with open("users.json", "w") as file:
        json.dump(user_details, file, indent=4)

except requests.exceptions.Timeout:
    pass
except requests.exceptions.ConnectionError:
    pass
except requests.exceptions.HTTPError:
    pass


url = "https://httpbin.org/delay/10"

try:
    response = requests.get(url, timeout=3)
    response.raise_for_status()

except requests.exceptions.Timeout:
    pass
except requests.exceptions.ConnectionError:
    pass
except requests.exceptions.HTTPError:
    pass
