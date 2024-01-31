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
import pyautogui
import win32.win32gui as win32gui
import keyboard
import threading
import re


user = None
stop_automation = False
class User:
    def printUserInformation(self):
        print(f'Username: {self.username}')
        print(f'Input path: {self.input_path}')
        print(f'Address path: {self.address_path}')
        print(f'Contact path: {self.contact_path}')
        print(f'Output path: {self.output_path}')
    
    def __init__(self, username):
        self.username = username
        self.input_path = os.path.join(r'C:\Users', username, 'Pictures\Greenshots_input')
        self.address_path = os.path.join(r'C:\Users', username, 'Pictures\Greenshots_input', f'Greenshots_address')
        self.contact_path = os.path.join(r'C:\Users', username, 'Pictures\Greenshots_input', f'Greenshots_contact')
        self.output_path = os.path.join(r'C:\Users', username, f'Pictures\Greenshots_output')
        # self.printUserInformation()

def readTxt(path):
    with open(path) as f:
        line = f.readline()
        return line

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
        content = json_data[i]['text']
        last_slash = content.rfind('/')

        chinese_address = content[0:last_slash]
        english_address = content[last_slash+1:]
        
        chinese_address_series = chinese_address_series._append(pd.Series([chinese_address]), ignore_index=True)
        english_address_series = english_address_series._append(pd.Series([english_address]), ignore_index=True)
        print(chinese_address, english_address)

    return chinese_address_series, english_address_series

def separate_contact(json_data, telephone_series, contact_series):
    for i in range(0, json_data.__len__()): 
        content = json_data[i]['text']
        print(content)
        # If the first 8 characters are digits, or the content is "NIL", it is a telephone number
        if(content[:8].isdigit() or content == "NIL") and len(content) >= 8:
            telephone_series = telephone_series._append(pd.Series([content]), ignore_index=True)
        # if there is no single numeric character in the content, it is a contact
        elif(not any(char.isdigit() for char in content)):
            contact_series = contact_series._append(pd.Series([content]), ignore_index=True)
        
            
        #     # if the last 8 characters are digits, it is a telephone number
        #     if(content[-8:].isdigit()):
        #         telephone_series = telephone_series._append(pd.Series([content[-8:]]), ignore_index=True)
        #         contact_series = contact_series._append(pd.Series([content[:-8]]), ignore_index=True) 
        #     else:
        #         contact_series = contact_series._append(pd.Series([content]), ignore_index=True)
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
        print(json_data)
        return json_data

    except Exception as e:
        tkinter.messagebox.showinfo('Error', f'Error processing file {file_path}: {e}\n The program is terminated.')
        driver.quit()
        print('The program is terminated...')
        exit()

def clone_file(srcPath, destPath):
    fileExistOrCreate(destPath)
    files = os.listdir(srcPath)
    for file in files:
        print(f'Copying file: {file} ...')
        shutil.copy(os.path.join(srcPath, file), destPath)
        os.remove(os.path.join(srcPath, file))

def current_time():
    return time.strftime("%Y%m%d-%H%M%S")

def check_inputLens():
    global user
    address_files = os.listdir(user.address_path)
    contact_files = os.listdir(user.contact_path)

    print('Files in the Address folder:\n', address_files)
    print('\nFiles in the Contact folder:\n', contact_files)

    if (len(address_files) == 0 and len(contact_files) == 0):
        tkinter.messagebox.showinfo('Error', f'Please input photos in the address & contact folders.')
        exit()
    elif(len(address_files) != len(contact_files)):
        confirm = messagebox.askquestion('Confirmation', "The number of files in the address folder and contact folder are not the same!\nConfirm to proceed?")
        if confirm == 'no':
            print("Exit the program...")
            exit()

def load_samplePhotos():
    global user
    if(os.path.exists(user.address_path) == False):
        fileExistOrCreate(user.address_path)
        shutil.copy('demoAddress_1.png', user.address_path)
        shutil.copy('demoAddress_2.png', user.address_path)
    
    if(os.path.exists(user.contact_path) == False):
        fileExistOrCreate(user.contact_path)
        shutil.copy('demoContact_1.png', user.contact_path)
        shutil.copy('demoContact_2.png', user.contact_path)

def check_username():
    global user
    username = readTxt("username.txt").strip()
    userpath = os.path.join(r'C:\Users', username)
    if(os.path.exists(userpath) == False):
        print(f'Username: \'{username}\' does not exist!')
        tkinter.messagebox.showinfo('Error', f'Username: \'{username}\' does not exist!\n The program is terminated.')
        exit()
    else:
        print(f'Username: \'{username}\' exists!')

    return username

def driver_setup():
    # Create a new tab of https://portal.vision.cognitive.azure.com/demo/extract-text-from-images
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    driver.execute_script(f"document.body.style.zoom='80%';")
    driver.get('https://portal.vision.cognitive.azure.com/demo/extract-text-from-images')

    button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div/main/div/div[2]/div[2]/div[5]/div/div[3]/div/div[2]/div/div[1]/button[2]"))) 
    button.click()

    return driver

def driver_eprc():
    desired_zoom_level = 1.5
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    driver.execute_script(f"document.body.style.zoom='80%';")
    driver.get('https://eprc.com.hk/eprcLogin.html')

    return driver

def eprc_Screenshot():
    global stop_automation

    page_cnt = 1  

    while not stop_automation:
        pyautogui.press('F4')
        
        # Screenshoting the page
        pyautogui.moveTo(1186, 1010, duration = 0.5)
        pyautogui.dragTo(830, 265, duration=2)
        time.sleep(0.5)

        pyautogui.typewrite(user.contact_path)
        time.sleep(0.5)
        pyautogui.press('enter')

        # Cancel the message box in the corner
        pyautogui.click(1873, 969)
        time.sleep(0.5)

        # Click the 'Next Page' button
        pyautogui.moveTo(1795, 1025, duration=0.5)
        cursor = win32gui.GetCursorInfo()
        
        if cursor[1] == 65567:
            print('Clicked the \'Next Page\' button!')
            pyautogui.click()
            page_cnt += 1
        else:
            print('Cannot find any \'Next Page\' button!')
            break

    print(f'\nFinished. There are {page_cnt} pages in total.')

def on_key_event(event):
    global stop_automation

    if event.name == 'f2':
        stop_automation = True
        print(f'Pressed \'F2\', stop_automation value is set to {stop_automation}.')

def generate_output(address_df):
    global user
    fileName = 'Result' + current_time() + '.xlsx'
    user.input_path = os.path.join(r'C:\Users', user.username, 'Pictures\Greenshots_input')
    user.output_path = os.path.join(r'C:\Users', user.username, f'Pictures\Greenshots_output')
    output_file_path = os.path.join(r'C:\Users', user.username, f'Pictures\Greenshots_output', fileName)
    
    if not os.path.exists(user.output_path):
        fileExistOrCreate(user.output_path)

    address_df.to_excel(output_file_path, index=False)

    Popen(output_file_path, shell=True)

    # clone_file(user.address_path, os.path.join(user.input_path, f'Greenshots_address_backup_{current_time()}'))
    # clone_file(user.contact_path, os.path.join(user.input_path, f'Greenshots_contact_backup_{current_time()}'))
    print(f'\nThe program finishes! Output file: {fileName} is generated!')
    tkinter.messagebox.showinfo('Information', f'The program finishes! Output file: {fileName} is generated!')

def build_outputDF(chinese_address_series, english_address_series, contact_series, telephone_series, page_series):
    address_df = pd.concat([chinese_address_series, english_address_series, contact_series, telephone_series, page_series], axis=1)
            
    if address_df.empty:
        tkinter.messagebox.showinfo('Error', f'No data is generated!\n The program is terminated.')
        print('The program is terminated...')
        exit()

    address_df.columns = ['Chinese Address', 'English Address', 'Contact', 'Telephone Number', 'Page']

    for i in range(len(address_df)):
        page_series = page_series._append(pd.Series([int(i/30)+1]), ignore_index=True)
        
    address_df['Page'] = page_series
    return address_df

def main():
    global user

    # Set up for the alert UI
    root = tkinter.Tk()
    root.withdraw()

    username = check_username()
    user = User(username)
    user.printUserInformation()
    fileExistOrCreate(user.input_path)
    load_samplePhotos()

    #============================ The start of EPRC ============================
    try: 
        eprc_driver = driver_eprc()
    
    except Exception as e:
        tkinter.messagebox.showinfo('Error', f'Error occurs: {e}\n The program is terminated.', parent = root)

    tkinter.messagebox.showinfo('Information', 'Start Searching in EPRC.')

     # Set up the key event handle  r
    keyboard.hook(on_key_event)

    # Create a thread for running the automation
    automation_thread = threading.Thread(target=eprc_Screenshot)

    automation_thread.start()
    automation_thread.join()

    # Alert dialog that tell the user to input the username and password
    tkinter.messagebox.showinfo('Information', 'Finish screenshooting.\nPLEASE REMEMBER TO LOG OUT EPRC!', parent = root)

    #============================ The end of EPRC ============================#

    # Create a new tab of https://portal.vision.cognitive.azure.com/demo/extract-text-from-images

    # The 5 series are used to store the data
    chinese_address_series, english_address_series, telephone_series, contact_series, page_series = pd.Series(), pd.Series(), pd.Series(), pd.Series(), pd.Series()

    try:            
        address_files = os.listdir(user.address_path)
        contact_files = os.listdir(user.contact_path)
        print(contact_files)

        check_inputLens()

        driver = driver_setup()
        
        try:
            # address_files_sorted = sorted(address_files,key=lambda x: int(os.path.splitext(x)[0]))
            address_files_sorted = sorted(address_files, key=lambda x: int(re.search(r'\d+', os.path.splitext(x)[0]).group()))
            for file in address_files_sorted:
                print('\nUploading the file: ' + file)
                file_path = os.path.join(user.address_path, file)
                json_data = upload_file(driver, file_path)
                chinese_address_series, english_address_series = separate_address(json_data, chinese_address_series, english_address_series)

        except Exception as e:
            tkinter.messagebox.showinfo('Error', f'Error occurs: {e}\n The program is terminated.')
            # driver.quit()
            exit()
            
        try:
            # contact_files_sorted = sorted(contact_files,key=lambda x: int(os.path.splitext(x)[0]))
            # contact_files_sorted = sorted(contact_files, key=lambda x: int(re.search(r'\d+', os.path.splitext(x)[0]).group()))
            for file in contact_files:
                print('\nUploading the file: ' + file)
                file_path = os.path.join(user.contact_path, file)
                json_data = upload_file(driver, file_path)
                # print(telephone_series, contact_series)
                telephone_series, contact_series = separate_contact(json_data, telephone_series, contact_series)
        
        except Exception as e:
            tkinter.messagebox.showinfo('Error', f'Error occurs: {e}\n The program is terminated.')
            exit()

        # finally:
        #     driver.quit()
        
        address_df = build_outputDF(chinese_address_series, english_address_series, contact_series, telephone_series, page_series)
        print(address_df)
        generate_output(address_df)

    except Exception as e:
        tkinter.messagebox.showinfo('Error', f'Error occurs: {e}\n The program is terminated.')

if __name__ == "__main__":
    main()