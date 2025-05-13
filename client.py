import requests
import json

url = "http://127.0.0.1:5000/predict"

p_class = int(input("Enter passenger class (1, 2, or 3): "))

sex = input("Enter passenger sex (male/female): ")

age = int(input("Enter passenger age: "))

sib_sp = int(input("Enter number of siblings/spouses aboard: "))

par_ch = int(input("Enter number of parents/children aboard: "))

payload = json.dumps({"p_class": p_class, "sex": sex, "age": age, "sib_sp": sib_sp, "par_ch": par_ch})
headers = {"Content-Type": "application/json"}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
