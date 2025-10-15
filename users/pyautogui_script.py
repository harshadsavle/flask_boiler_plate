import pyautogui
import pandas as pd

import time

def fill_signup_form(username,email,password,address):
    time.sleep(3)
    pyautogui.moveTo(846, 464, duration=0)
    pyautogui.click()
    pyautogui.write(username, interval=0.05)
    pyautogui.hotkey('tab')
    pyautogui.write(email, interval=0.05)
    pyautogui.hotkey('tab')
    pyautogui.write(password, interval=0.05)
    pyautogui.hotkey('tab')
    pyautogui.write(address, interval=0.05)
    pyautogui.hotkey('tab')
    pyautogui.hotkey('enter')
    time.sleep(2)


df = pd.read_csv("register_users.csv")
for index, row in df.iterrows():
    username = row['username']
    email = row['email']
    password = row['password']
    address = row['address']

    fill_signup_form(username,email,password,address)
    





