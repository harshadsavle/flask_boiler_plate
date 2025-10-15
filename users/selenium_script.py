from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time
import random
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()  
actions = ActionChains(driver)

def fill_signup_form(username, email, password, address):
    driver.get("http://localhost:3000/signup")  

    time.sleep(2)

    driver.find_element(By.NAME, "username").send_keys(username)
    driver.find_element(By.NAME, "email").send_keys(email)
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.NAME, "address").send_keys(address)

    driver.find_element(By.XPATH, "//button[@type='submit']").click()

    time.sleep(3)

def login_user(username, password):
    driver.get("http://localhost:3000")
    time.sleep(2)

    driver.find_element(By.NAME, "username").send_keys(username)
    driver.find_element(By.NAME, "password").send_keys(password)
    time.sleep(1)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()

    time.sleep(3)

def logout_user():
    driver.find_element(By.NAME, "logout-button").click()


def automate_buy():
    items = ['pen', 'mobile', 'laptop', 'bag', 'pc', 'refrigerator']
    position = random.randrange(5)
    search_keyword = items[position]
    driver.find_element(By.NAME, "search").send_keys(search_keyword)
    driver.find_element(By.NAME, "submit-search").click()
    time.sleep(3)
    cart_or_buy = random.choice([0, 1])
    if cart_or_buy == 1:
        driver.find_element(By.NAME, "buy-now").click()
        alert = driver.switch_to.alert
        alert.send_keys("Yes")
        alert.accept()
    
    else:
        driver.find_element(By.NAME, "add-to-cart").click()
    time.sleep(2)


def signup_users():
    df = pd.read_csv("register_users.csv")
    for index, row in df.iterrows():
        username = row['username']
        email = row['email']
        password = row['password']
        address = row['address']

        fill_signup_form(username, email, password, address)

df = pd.read_csv("login_users.csv")
for index,row in df.iterrows():
    username = row['username']
    password = row['password']
    login_user(username, password)
    automate_buy()
    logout_user()

driver.quit()
