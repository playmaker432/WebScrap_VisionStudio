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
import tkinter as tkinter
from tkinter import messagebox
import shutil

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

def fileExistOrCreate(path):
    if(os.path.exists(path) == False):
        print(f'Path: {path} does not exist, now creating the directories...')
        os.makedirs(path)
        print(f'Path: {path} is created successfully!')
    else:
        print(f'Path: {path} exists!')

def upload_file(driver, file_path):
    try:
        button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div/main/div/div[2]/div[2]/div[5]/div/div[2]/div/div[1]/div[2]/button[1]")))
        button.click()

        time.sleep(1)
        typewrite(file_path)
        time.sleep(1)
        press('enter')
        time.sleep(3)

        json_text = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "pre"))).text
        json_text = json_text[1:-1]
        json_data = json.loads(json_text)['lines']
        return json_data
    except Exception as e:
        tkinter.messagebox.showinfo('Error', f'Error processing file {file_path}: {e}\n The program is terminated.')
        driver.quit()
        print('The program is terminated...')
        exit()

# The 5 series are used to store the data
chinese_address_series, english_address_series, telephone_series, contact_series, page_series = pd.Series(), pd.Series(), pd.Series(), pd.Series(), pd.Series()
root = tkinter.Tk()
root.withdraw()
path = ''
address_path = ''
contact_path = ''

while True:
    username = input('Enter your username: ')
    userpath = os.path.join(r'C:\Users', username)
    path = os.path.join(r'C:\Users', username, 'Pictures\Greenshots_input')
 
    if(os.path.exists(userpath) == False):
        print(f'Username: \'{username}\' does not exist!')
        continue

    if os.path.exists(path):
        break
    else:
        fileExistOrCreate(path)
        address_path = os.path.join(path, f'Greenshots_address')
        contact_path = os.path.join(path, f'Greenshots_contact')
        if(os.path.exists(address_path) == False):
            fileExistOrCreate(address_path)
            shutil.copy('demoAddress_1.png', address_path)
            shutil.copy('demoAddress_2.png', address_path)
        
        if(os.path.exists(contact_path) == False):
            fileExistOrCreate(contact_path)
            shutil.copy('demoContact_1.png', contact_path)
            shutil.copy('demoContact_2.png', contact_path)

        break
 
try:    
    address_path = os.path.join(path, f'Greenshots_address')
    contact_path = os.path.join(path, f'Greenshots_contact')

    if(os.path.exists(address_path) == False):
       fileExistOrCreate(address_path)
    
    if(os.path.exists(contact_path) == False):
        fileExistOrCreate(contact_path)

    address_files = os.listdir(address_path)
    contact_files = os.listdir(contact_path)

    if (len(address_files) == 0 and len(contact_files) == 0):
        tkinter.messagebox.showinfo('Error', f'Please input photos in the address & contact folders.')
        exit()
    elif(len(address_files) != len(contact_files)):
        confirm = messagebox.askquestion('Confirmation', "The number of files in the address folder and contact folder are not the same!\nConfirm to proceed?")
        if confirm == 'no':
            print("Exit the program...")
            exit()
    
    print('Files in the Address folder:\n', address_files)
    print('\nFiles in the Contact folder:\n', contact_files)

    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    driver.get('https://portal.vision.cognitive.azure.com/demo/extract-text-from-images')

    button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div/main/div/div[2]/div[2]/div[5]/div/div[3]/div/div[2]/div/div[1]/button[2]"))) 
    button.click()
    
    try:
        for file in address_files:
            print('\nUploading the file: ' + file)
            file_path = os.path.join(address_path, file)
            json_data = upload_file(driver, file_path)
            chinese_address_series, english_address_series = separate_address(json_data, chinese_address_series, english_address_series)

    except Exception as e:
        tkinter.messagebox.showinfo('Error', f'Error occurs: {e}\n The program is terminated.')
        driver.quit()
        exit()
        
    try:
        for file in contact_files:
            print('\nUploading the file: ' + file)
            file_path = os.path.join(contact_path, file)
            json_data = upload_file(driver, file_path)
            telephone_series, contact_series = separate_contact(json_data, telephone_series, contact_series)
    
    except Exception as e:
        tkinter.messagebox.showinfo('Error', f'Error occurs: {e}\n The program is terminated.')
        driver.quit()
        exit()

    driver.quit()

    address_df = pd.concat([chinese_address_series, english_address_series, contact_series, telephone_series, page_series], axis=1)
    if address_df.empty:
        tkinter.messagebox.showinfo('Error', f'No data is generated!\n The program is terminated.')
        print('The program is terminated...')
        exit()

    address_df.columns = ['Chinese Address', 'English Address', 'Contact', 'Telephone Number', 'Page']

    for i in range(len(address_df)):
        page_series = page_series._append(pd.Series([int(i/30)+1]), ignore_index=True)
        
    address_df['Page'] = page_series

    name = 'Result' + time.strftime("%Y%m%d-%H%M%S") + '.xlsx'

    output_path = os.path.join(r'C:\Users', username, f'Pictures\Greenshots_output')
    output_file_path = os.path.join(r'C:\Users', username, f'Pictures\Greenshots_output', name)
    
    if not os.path.exists(output_path):
        fileExistOrCreate(output_path)

    address_df.to_excel(output_file_path, index=False)

    Popen(output_file_path, shell=True)

    print(f'\nThe program finishes! Output file: {name} is generated!')
    tkinter.messagebox.showinfo('Information', f'The program finishes! Output file: {name} is generated!') 

except Exception as e:
    tkinter.messagebox.showinfo('Error', f'Error occurs: {e}\n The program is terminated.')
    driver.quit()
    exit()
