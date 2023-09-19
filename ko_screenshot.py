# Automation of the OCR by uploading files from a specific path to online Vision Studio website and get json data and form dataframe

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

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)

# Get the pictures from the path 'C:\Users\raymondlaw\Pictures\Greenshots_input'
path = r'C:\Users\raymondlaw\Pictures\Greenshots_input'

# List the files in the path:
files = os.listdir(path)
print(files)

# Use selenium to upload the pictures to the website with the fllowing URL: https://portal.vision.cognitive.azure.com/demo/extract-text-from-images
driver = webdriver.Chrome(options=options)
driver.maximize_window()
driver.get('https://portal.vision.cognitive.azure.com/demo/extract-text-from-images')

# Wait the page is loaded and Scroll down a bit
# time.sleep(10)
# driver.execute_script("window.scrollTo(0, 500)")

# Click this element: <span class="ms-Pivot-text text-254"> JSON</span>
button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "ms-Pivot-text.text-254")))

# Upload the pictures to the website
for file in files:

    print('Uploading the file: ' + file)

    # Create a path of the file
    file_path = os.path.join(path, file)


    button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "ms-Link.upload-link.link.root-242")))
    button.click()


    # Wait the file explorer to openC:\Users\raymondlaw\Pictures\Greenshots_input\2023-09-19 11_05_46-Settings.png
    # driver.implicitly_wait(10)

    # Use pyautogui to type the path of the file
    time.sleep(1)
    typewrite(file_path)
    time.sleep(1)
    press('enter')

    time.sleep(100)

    # Get the json data from the website



print('The program finishes!')




