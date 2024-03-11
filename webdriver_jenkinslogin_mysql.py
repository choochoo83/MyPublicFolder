from selenium import webdriver
import time, os, re
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pytest
os.system("cls")


def test_jenkins_login(username, password):
    driver = webdriver.Chrome()
    driver.get("http://127.0.0.1:8080/login")
    driver.implicitly_wait(5)

    username_box = driver.find_element(By.ID, "j_username")
    username_box.send_keys(username)
    password_box = driver.find_element(By.ID, "j_password")
    password_box.send_keys(password)
    driver.find_element(By.CSS_SELECTOR, "button[name='Submit']").click()
    time.sleep(1)

    check_logout_button = len(driver.find_elements(By.CSS_SELECTOR, "body > header:nth-child(2) > div:nth-child(3) > a:nth-child(4) > span:nth-child(2)"))
    if check_logout_button > 0:
        logout = driver.find_element(By.CSS_SELECTOR, "body > header:nth-child(2) > div:nth-child(3) > a:nth-child(4) > span:nth-child(2)")
        logout.click()
        print("Login is successful: " + username + " " + password)
    else:
        print("Login is failed: " + username + " " + password)
    driver.quit()


import mysql.connector
# mysql> use mydatabase;
# mysql> show tables;
# mysql> select * from <table>;
# mysql> select distinct * from <table>;
# mysql> select * from myjenkins where username like "s%";


# [1] Create database - only need to execute one time and one database can have multiple tables 
# mydb = mysql.connector.connect(host="localhost", user="root", password="3967067")
# mydb.cursor().execute("CREATE DATABASE mydatabase")

# [2] Connect to existing database
mydb = mysql.connector.connect(host="localhost", user="root", password="3967067", database="mydatabase")

# [3] Create new table - when it is needed
# mydb.cursor().execute("CREATE TABLE jenkins (username VARCHAR(255), password VARCHAR(255))")

# [4] Write to the existing table 
# c = mydb.cursor()
# c.execute("INSERT INTO jenkins(username, password) VALUES ('aaa', '111'), ('bbb', '222'), ('ccc', '333'), ('ddd', '444'), ('sk', '123'), ('eee', '555'), ('fff', '666'), ('ggg', '777'), ('hhh', '888'), ('iii', '999') ")

# [5] Read from the existing table 
c = mydb.cursor()
c.execute("SELECT DISTINCT * FROM jenkins")
rows = c.fetchall()
for row in rows:
    un = row[0]
    pw = row[1]
    test_jenkins_login(un, pw)
    time.sleep(1)

c.close()
mydb.close()