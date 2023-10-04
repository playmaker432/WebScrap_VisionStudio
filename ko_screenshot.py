# Automation of the OCR by uploading files from a specific path to online Vision Studio website and get json data and form dataframe
import json
import pandas as pd
import numpy as np
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from subprocess import Popen
from pyautogui import press, typewrite, hotkey

# Print the input with double lines
def printDoubleLine(input):
    print('==================================================')
    print(input)
    print('==================================================')

# Print the input with single lines
def printSingleLine(input):
    print('--------------------------------------------------')
    print(input)
    print('--------------------------------------------------')

def separate_address(json_data, chinese_address_series, english_address_series):
    for i in range(0, json_data.__len__()):
        content = json_data[i]['content']
        last_slash = content.rfind('/')

        # Use the last_logic to classify Chinese and English addresses 
        chinese_address = content[0:last_slash]
        english_address = content[last_slash+1:]
        
        chinese_address_series = chinese_address_series._append(pd.Series([chinese_address]), ignore_index=True)
        english_address_series = english_address_series._append(pd.Series([english_address]), ignore_index=True)
        print(chinese_address, english_address)

    return chinese_address_series, english_address_series

def separate_contact(json_data, telephone_series, contact_series):
    for i in range(0, json_data.__len__()):
        content = json_data[i]['content']
        if content[0].isdigit():
            telephone_series = telephone_series._append(pd.Series([content]), ignore_index=True)
            print(content)
        else:
            contact_series = contact_series._append(pd.Series([content]), ignore_index=True)
    
    return telephone_series, contact_series

while True:
    username = input('Enter your username: ')
    confirm = input(f'Confirm your username as "{username}" (yes/no): ').lower()
    if confirm != 'yes':
        print('Please re-enter your username.')
        

    path = os.path.join(r'C:\Users', username, 'Pictures\Greenshots_input')

    if os.path.exists(path):
        break
    else:
        print(f'Path: {path} does not exist, please re-enter your username.')

    
try:
    address_path = os.path.join(path, f'Greenshots_address')
    contact_path = os.path.join(path, f'Greenshots_contact')

    address_files = os.listdir(address_path)
    contact_files = os.listdir(contact_path)

    print('Files in the Address folder:\n', address_files)
    print('\nFiles in the Contact folder:\n', contact_files)

    chinese_address_series = pd.Series()
    english_address_series = pd.Series()
    telephone_series = pd.Series()
    contact_series = pd.Series()
    page_series = pd.Series()

    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    # options.headless = True
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    driver.get('https://portal.vision.cognitive.azure.com/demo/extract-text-from-images')

    # This button is clicked to Display the JSON data (The HTML element may be modified in the future)``
    # button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "Pivot40-Tab1")))
    button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "Pivot39-Tab1")))
    button.click()

    try: 
        # Upload the pictures to the website
        for file in address_files:
            print('\nUploading the file: ' + file)
            file_path = os.path.join(address_path, file)
            # button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "ms-Link.upload-link.link.root-243")))
            button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "ms-Link.upload-link.link.root-242")))
            button.click()

            # Use pyautogui to type the path of the file
            time.sleep(1)
            typewrite(file_path)
            time.sleep(1)
            press('enter')
            time.sleep(3)

            json_text = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "pre"))).text
            json_text = json_text[1:-1]
            json_data = json.loads(json_text)['lines']
            print(json_data)
            
            chinese_address_series, english_address_series = separate_address(json_data, chinese_address_series, english_address_series)

    except Exception as e:
        print(f'Error processing file {file}: {e}')
        driver.quit()
        input('Press any key to exit the program.')
        print('The program is terminated.')
        exit()

    
    try:
        for file in contact_files:

            print('\nUploading the file: ' + file)

            # Create a path of the file
            file_path = os.path.join(contact_path, file)

            # button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "ms-Link.upload-link.link.root-243")))
            button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "ms-Link.upload-link.link.root-242")))
            button.click()

            # Use pyautogui to type the path of the file
            time.sleep(1)
            typewrite(file_path)
            time.sleep(1)
            press('enter')
            time.sleep(3)

            json_text = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "pre"))).text
            print("Json", json_text)
            json_text = json_text[1:-1]
            json_data = json.loads(json_text)['lines']
            print(json_data)
            
            telephone_series, contact_series = separate_contact(json_data, telephone_series, contact_series)
    
    except Exception as e:
        print(f'Error processing file {file}: {e}')
        # Exit the program if there is an error and show an alert
        driver.quit()
        # User input anything to exit the program
        input('Press any key to exit the program.')
        print('The program is terminated.')
        exit()

    driver.quit()

    address_df = pd.concat([chinese_address_series, english_address_series, contact_series, telephone_series, page_series], axis=1)
    address_df.columns = ['Chinese Address', 'English Address', 'Contact', 'Telephone Number', 'Page']

    for i in range(len(address_df)):
        page_series = page_series._append(pd.Series([int(i/30)+1]), ignore_index=True)
        
    address_df['Page'] = page_series

    name = 'Result' + time.strftime("%Y%m%d-%H%M%S") + '.csv'
    output_path = os.path.join(r'C:\Users', username, f'Pictures\Greenshots_output', name)

    address_df.to_csv(output_path, index=False, encoding='utf-8-sig')
    Popen(output_path, shell=True)

    print(f'\nThe program finishes! Output file: {name} is generated!')

except Exception as e:

     print(f'An error occurred: {e}')