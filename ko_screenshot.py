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

def printDoubleLine(input):
    print('==================================================')
    print(input)
    print('==================================================')

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
        # print(content, type(content))
        if content[0].isdigit():
            telephone_series = telephone_series._append(pd.Series([content]), ignore_index=True)
            print(content)
        else:
            contact_series = contact_series._append(pd.Series([content]), ignore_index=True)
    
    return telephone_series, contact_series

# Get the pictures from the path 'C:\Users\raymondlaw\Pictures\Greenshots_input'
path = r'C:\Users\raymondlaw\Pictures\Greenshots_input'
# address_files_path = r'C:\Users\raymondlaw\Pictures\Greenshots_input\Greenshots_contact'
address_path = path + '\Greenshots_address'
contact_path = path + '\Greenshots_contact'

address_files = os.listdir(address_path)
contact_files = os.listdir(contact_path)

print('Files in the Address folder:\n', address_files)
print('\nFiles in the Contact folder:\n', contact_files)

chinese_address_series = pd.Series()
english_address_series = pd.Series()
telephone_series = pd.Series()
contact_series = pd.Series()
page_series = pd.Series()

# Use selenium to upload the pictures to the website with the flloC:\Users\raymondlaw\Pictures\Greenshots_input\ecpr_real_oneline.pngwing URL: https://portal.vision.cognitive.azure.com/demo/extract-text-from-images
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
# options.headless = True
driver = webdriver.Chrome(options=options)
driver.maximize_window()
driver.get('https://portal.vision.cognitive.azure.com/demo/extract-text-from-images')

# Click this element: <button type="button" id="Pivot39-Tab1" class="ms-Button ms-Button--action ms-Button--command ms-Pivot-link link-261" role="tab" aria-selected="false" name="JSON" data-content="JSON" data-is-focusable="true" tabindex="-1"><span class="ms-Button-flexContainer flexContainer-257" data-automationid="splitbuttonprimary"><span class="ms-Pivot-linkContent linkContent-253"><span class="ms-Pivot-text text-254"> JSON</span></span></span></button>
button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "Pivot40-Tab1")))
button.click()

# Upload the pictures to the website
for file in address_files:
    print('\nUploading the file: ' + file)
    # Create a path of the file
    file_path = os.path.join(address_path, file)
    button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "ms-Link.upload-link.link.root-243")))
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

for file in contact_files:

    print('\nUploading the file: ' + file)

    # Create a path of the file
    file_path = os.path.join(contact_path, file)

    button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "ms-Link.upload-link.link.root-243")))
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
    
    telephone_series, contact_series = separate_contact(json_data, telephone_series, contact_series)

# After uploading all the pictures, close the browser and use ONE PANDA dataframe to store the Chinese address, English address and telephone number
driver.quit()

address_df = pd.concat([chinese_address_series, english_address_series, contact_series, telephone_series, page_series], axis=1)
address_df.columns = ['Chinese Address', 'English Address', 'Contact', 'Telephone Number', 'Page']
print(address_df)

# Page number series: 30 column as 1 page
for i in range(0, address_df.__len__()):
    page_series = page_series._append(pd.Series([int(i/30)+1]), ignore_index=True)
address_df['Page'] = page_series

# Generate the csv file by Result+time
name = 'Result' + time.strftime("%Y%m%d-%H%M%S") + '.csv'
address_df.to_csv(r'C:\Users\raymondlaw\Pictures\Greenshots_output\\' + name, index=False, encoding='utf-8-sig')
#Open the csv file
Popen(r'C:\Users\raymondlaw\Pictures\Greenshots_output\\' + name, shell=True)

print('\nThe program finishes! Output file: ' + name + ' is generated!')

