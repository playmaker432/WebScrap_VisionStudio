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
from pyautogui import press, typewrite, hotkey

# Separate Chinese address, English address and telephone number, while the input is a json
def separate_addresses(input):
    last_slash = input.rfind('/')

    if last_slash == -1:
        print(input)
    
    else: 
        chinese_address = input[:last_slash]
        english_address = input[last_slash+1:]
        print(chinese_address + english_address)

def printDoubleLine(input):
    print('==================================================')
    print(input)
    print('==================================================')

def printSingleLine(input):
    print('--------------------------------------------------')
    print(input)
    print('--------------------------------------------------')


def handle_JsonData(json_data):
    for i in range(0,30):
        separate_addresses(json_data[i]['content'])

# Get the pictures from the path 'C:\Users\raymondlaw\Pictures\Greenshots_input'
path = r'C:\Users\raymondlaw\Pictures\Greenshots_input'
files = os.listdir(path)
print(files)

# declare lists to store the dataframe of json data
address_df = []
telephone_df = []

# Use selenium to upload the pictures to the website with the fllowing URL: https://portal.vision.cognitive.azure.com/demo/extract-text-from-images
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)
driver.maximize_window()
driver.get('https://portal.vision.cognitive.azure.com/demo/extract-text-from-images')

# Click this element: <button type="button" id="Pivot39-Tab1" class="ms-Button ms-Button--action ms-Button--command ms-Pivot-link link-261" role="tab" aria-selected="false" name="JSON" data-content="JSON" data-is-focusable="true" tabindex="-1"><span class="ms-Button-flexContainer flexContainer-257" data-automationid="splitbuttonprimary"><span class="ms-Pivot-linkContent linkContent-253"><span class="ms-Pivot-text text-254"> JSON</span></span></span></button>
button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "Pivot40-Tab1")))
button.click()

# Upload the pictures to the website
for file in files:

    print('Uploading the file: ' + file)

    # Create a path of the file
    file_path = os.path.join(path, file)

    button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "ms-Link.upload-link.link.root-243")))
    button.click()

    # Use pyautogui to type the path of the file
    time.sleep(1)
    typewrite(file_path)
    time.sleep(1)
    press('enter')
    time.sleep(3)

    # Get the json data from the website from this element: <pre tabindex="0">{...}</pre>
    json_text = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "pre"))).text
    # Delete the first '[' and ']' in the json data
    json_text = json_text[1:-1]
    # Turn this text to a json format
    json_data = json.loads(json_text)['lines']
    print(json_data)
    
    handle_JsonData(json_data)

# Close the browser
driver.quit()
print('The program finishes!')




