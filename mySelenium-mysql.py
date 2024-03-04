from selenium import webdriver
import time, os, re
os.system("cls")

# creating test data (car model and year) in SQL then extract the data from the database
# in parallel it can be tested the commands over the mysql command line mysql> before applied into python script
# mysql> use mydatabase;
# mysql> show tables;
# mysql> select * from mycar;

import mysql.connector #python -m pip install mysql-connector-python
# mydb = mysql.connector.connect(host="localhost", user="root", password="3967067")
# mydb.cursor().execute("CREATE DATABASE mydatabase")
mydb = mysql.connector.connect(host="localhost", user="root", password="3967067", database="mydatabase")
# mydb.cursor().execute("CREATE TABLE mycar (car_model VARCHAR(255), year_number int)")
c = mydb.cursor()
c.execute("INSERT INTO mycar(car_model, year_number) VALUES ('Toyota Vios', 2024), ('Honda City', 2024), ('Mazda 2', 2024)")
# c.execute("SELECT * FROM mycar")
c.execute("SELECT * FROM mycar WHERE car_model LIKE 'Toyota%' LIMIT 1")
rows = c.fetchall()
for r in rows:
    car = r[0]
    year = str(r[1])

# using the test data (car model and year) for searching
driver = webdriver.Chrome()
driver.get("http://www.google.com/")
time.sleep(1)

from selenium.webdriver.common.by import By
ggl_search = driver.find_element(By.CSS_SELECTOR, "#APjFqb") #External chrome plugin "SelectorsHub"
from selenium.webdriver.common.keys import Keys
# ggl_search.send_keys("Toyota vios 2024 price malaysia")
ggl_search.send_keys(car + " " + year + " price malaysia")
ggl_search.send_keys(Keys.ENTER)
time.sleep(3)

info = driver.find_element(By.CSS_SELECTOR, "div[class='V3FYCf'] span[class='hgKElc']") # By SelectorsHub
print(info.text)

i = 0
price = []
for i in range(len(info.text.split(" "))):
    text = info.text.split(" ")[i]
    if re.search("RM", text):
        price.append(info.text.split(" ")[i+1])
    i += 1

print(price) # ['89,600', '95,500', '89,600']
print(min(price))  # 89,600

