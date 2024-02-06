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
import re
import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox
import subprocess


user = None
stop_automation = False
page_cnt = 1
photo_cnt = 1
query_cnt = 1
query_list = ["香港", "九龍", "新界"]
query_name = ""

class User:
    def printUserInformation(self):
        print(f'Username: {self.username}')
        print(f'Input path: {self.input_path}')
        print(f'Address path: {self.address_path}')
        print(f'Contact path: {self.contact_path}')
        print(f'Output path: {self.output_path}')
        print(f'Fullscreen path: {self.fullscreen_path}')
        
    
    def __init__(self, username):
        self.username = username
        self.input_path = os.path.join(r'C:\Users', username, 'Pictures\Greenshots_input')
        self.address_path = os.path.join(r'C:\Users', username, 'Pictures\Greenshots_input', f'Greenshots_address')
        self.contact_path = os.path.join(r'C:\Users', username, 'Pictures\Greenshots_input', f'Greenshots_contact')
        self.output_path = os.path.join(r'C:\Users', username, f'Pictures\Greenshots_output')
        self.fullscreen_path = os.path.join(r'C:\Users', username, 'Pictures\Greenshots_input', f'Greenshots_fullscreen')

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

def separate_contact(json_data, telephone_series, contact_series, page_series):
    global photo_cnt

    for i in range(0, json_data.__len__()): 
        content = json_data[i]['text']
        print(content)
        # If the first 8 characters are digits, or the content is "NIL", it is a telephone number
        if(content[:8].isdigit() or content == "NIL") and len(content) >= 8:
            telephone_series = telephone_series._append(pd.Series([content]), ignore_index=True)
            # page series append the current page number, where the iteration of the loop
            page_series = page_series._append(pd.Series([photo_cnt]), ignore_index=True)
            
    return telephone_series, contact_series, page_series

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
        tkinter.messagebox.showinfo('Error', f'Error processing file {file_path}: {e}\n The program is terminated.', parent = root)
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

    root = tkinter.Tk()

    address_files = os.listdir(user.address_path)
    contact_files = os.listdir(user.contact_path)

    print('Files in the Address folder:\n', address_files)
    print('\nFiles in the Contact folder:\n', contact_files)

    if (len(address_files) == 0 and len(contact_files) == 0):
        tkinter.messagebox.showinfo('Error', f'Please input photos in the address & contact folders.', parent = root)
        exit()
    elif(len(address_files) != len(contact_files)):
        confirm = messagebox.askquestion('Confirmation', "The number of files in the address folder and contact folder are not the same!\nConfirm to proceed?", parent = root)
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

    clone_file(user.address_path, os.path.join(user.input_path, f'Greenshots_address_backup_{current_time()}'))
    clone_file(user.contact_path, os.path.join(user.input_path, f'Greenshots_contact_backup_{current_time()}'))
    clone_file(user.fullscreen_path, os.path.join(user.input_path, f'Greenshots_fullscreen_backup_{current_time()}'))
    
    print(f'\nThe program finishes! Output file: {fileName} is generated!')
    tkinter.messagebox.showinfo('Information', f'The program finishes! Output file: {fileName} is generated!')

def build_outputDF(chinese_address_series, english_address_series, contact_series, telephone_series, page_series):
    address_df = pd.concat([chinese_address_series, english_address_series, contact_series, telephone_series, page_series], axis=1)
            
    if address_df.empty:
        tkinter.messagebox.showinfo('Error', f'No data is generated!\n The program is terminated.')
        print('The program is terminated...')
        exit()

    address_df.columns = ['Chinese Address', 'English Address', 'Contact', 'Telephone Number', 'Page']

    # This part is HARD CODED, need to be changed if the number of pages is changed
    # for i in range(len(address_df)):
    #     page_series = page_series._append(pd.Series([int(i/30)+1]), ignore_index=True)
        
    address_df['Page'] = page_series
    return address_df

def driver_setup():
    global photo_cnt
    root = tkinter.Tk()

    # Create a new tab of https://portal.vision.cognitive.azure.com/demo/extract-text-from-images
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    driver.execute_script(f"document.body.style.zoom='80%';")
    driver.get('https://portal.vision.cognitive.azure.com/demo/extract-text-from-images')

    button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div/main/div/div[2]/div[2]/div[5]/div/div[3]/div/div[2]/div/div[1]/button[2]"))) 
    button.click()

    chinese_address_series, english_address_series, telephone_series, contact_series, page_series = pd.Series(), pd.Series(), pd.Series(), pd.Series(), pd.Series()

    try:            
        address_files = os.listdir(user.address_path)
        contact_files = os.listdir(user.contact_path)
        print(contact_files)

        check_inputLens()

        try:
            # address_files_sorted = sorted(address_files,key=lambda x: int(os.path.splitext(x)[0]))
            address_files_sorted = sorted(address_files, key=lambda x: int(re.search(r'\d+', os.path.splitext(x)[0]).group()))
            for file in address_files_sorted:
                print('\nUploading the file: ' + file)
                file_path = os.path.join(user.address_path, file)
                json_data = upload_file(driver, file_path)
                chinese_address_series, english_address_series = separate_address(json_data, chinese_address_series, english_address_series)

        except Exception as e:
            tkinter.messagebox.showinfo('Error', f'Error occurs: {e}\n The program is terminated.', parent = root)
            # driver.quit()
            exit()
            
        try:
            # contact_files_sorted = sorted(contact_files,key=lambda x: int(os.path.splitext(x)[0]))
            # contact_files_sorted = sorted(contact_files, key=lambda x: int(re.search(r'\d+', os.path.splitext(x)[0]).group()))
            for file in contact_files:
                print('\nUploading the file: ' + file)
                file_path = os.path.join(user.contact_path, file)
                json_data = upload_file(driver, file_path)
                telephone_series, contact_series, page_series = separate_contact(json_data, telephone_series, contact_series, page_series)
                photo_cnt += 1
        
        except Exception as e:
            tkinter.messagebox.showinfo('Error', f'Error occurs: {e}\n The program is terminated.', parent = root)
            exit()

        address_df = build_outputDF(chinese_address_series, english_address_series, contact_series, telephone_series, page_series)
        print(address_df)
        generate_output(address_df)

    except Exception as e:
        tkinter.messagebox.showinfo('Error', f'Error occurs: {e}\n The program is terminated.', parent = root)

def driver_eprc():
    desired_zoom_level = 1.5
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    driver.execute_script(f"document.body.style.zoom='80%';")
    driver.get('https://eprc.com.hk/eprcLogin.html')
    
class SimpleUI:
    global user


    def __init__(self, master):
        self.master = master
        master.title("Simple UI")

        # Set a larger font size
        font_size = 12

        self.label = tk.Label(master, text="Choose an option:", pady=10, font=("Arial", font_size))
        self.label.pack()

        self.button4 = tk.Button(master, text="1. Open Input Folder", command=self.open_input_folder, pady=5, font=("Arial", font_size))
        self.button4.pack(pady=5)

        self.button5 = tk.Button(master, text="2. Open Output Folder", command=self.open_output_folder, pady=5, font=("Arial", font_size))
        self.button5.pack(pady=5)

        self.button1 = tk.Button(master, text="3. Check/Change Username", command=self.check_change_username, pady=5, font=("Arial", font_size))
        self.button1.pack(pady=5)

        self.button2 = tk.Button(master, text="4. Open EPRC Website", command=self.driver_eprc, pady=5, font=("Arial", font_size))
        self.button2.pack(pady=5)

        self.button3 = tk.Button(master, text="5. Screenshot EPRC", command=self.eprc_Screenshot, pady=5, font=("Arial", font_size))
        self.button3.pack(pady=5)

        self.button4 = tk.Button(master, text="6. OCR by Vision Studio", command=driver_setup, pady=5, font=("Arial", font_size))
        self.button4.pack(pady=5)

        # When the simpleUI is closed, ask the user first if they want to close the program
        master.protocol("WM_DELETE_WINDOW", self.on_closing)

    def driver_eprc(self):
        # Disable the button to prevent multiple clicks during the operation
        self.master.withdraw()
        driver_eprc()
        self.master.deiconify()
    
    def eprc_Screenshot(self):
        global stop_automation
        global page_cnt
        global user
        global query_name

        # Use a suer input dialog to get the query name
        query_name = simpledialog.askstring("Query Name", "Enter a query name:")

        tkinter.messagebox.showinfo('Information', 'Start Searching in EPRC.')
        self.master.withdraw()

        pyautogui.click()

        while not stop_automation:
            time.sleep(3.0)

            print("Page " + str(page_cnt) + ":")

            pyautogui.press('F4')

            # Screenshoting the page
            pyautogui.moveTo(1100, 1010, duration = 0.5)
            pyautogui.dragTo(830, 255, duration=2.5)
            
            time.sleep(0.5)
            pyautogui.typewrite(user.contact_path + f"\\Greenshots_contact_{page_cnt}.png")
            time.sleep(0.5)
            pyautogui.press('enter')

            time.sleep(2.0)

            # press the control + print scrn button to capture the full screen
            pyautogui.hotkey('ctrl', 'printscreen')
            time.sleep(0.5)
            pyautogui.typewrite(user.input_path + f"\\Greenshots_fullscreen\\{page_cnt}.png")
            pyautogui.press('enter')
            

            time.sleep(2.0)

            # Cancel the message box in the corner
            pyautogui.click(1873, 969)
            time.sleep(0.5)

            # Click the 'Next Page' button
            pyautogui.moveTo(1795, 1025, duration=0.5)
            cursor = win32gui.GetCursorInfo()
            print(cursor)
            
            if cursor[1] == 65567 or cursor[1] == 65597:
                pyautogui.click()
                print('Clicked the \'Next Page\' button!')
                page_cnt += 1
            else:
                print('Cannot find any \'Next Page\' button!')
                break

        print(f'\nFinished. There are {page_cnt} pages in total.')
        self.master.deiconify()

    def driver_setup(self):
        # Disable the button to prevent multiple clicks during the operation
        self.master.withdraw()
        driver_setup()
        self.master.deiconify()

    def check_change_username(self):
        current_username = readTxt("username.txt").strip()
        userpath = os.path.join(r'C:\Users', current_username)

        # Show the current username
        messagebox.showinfo('Current Username', f'Current Username: {current_username}')

        # Ask the user if they want to change it
        change_username = messagebox.askyesno('Change Username', 'Do you want to change the username?')

        if not change_username:
            return

        # Prompt for a new username
        new_username = simpledialog.askstring("Change Username", "Enter a new username:")

        if not new_username:
            messagebox.showwarning('Warning', 'Username cannot be empty.')
            return

        # Check if the new username exists in the syste
        new_userpath = os.path.join(r'C:\Users', new_username)
        if os.path.exists(new_userpath):
            with open("username.txt", "w") as f:
                f.write(new_username)
            messagebox.showinfo('Username Changed', f'Username changed to: {new_username}')
        else:
            messagebox.showwarning('Warning', f'Username {new_username} does not exist.')

    def open_input_folder(self):
        try:
            subprocess.run(['explorer', user.input_path], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error opening directory: {e}")

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Please check that you have logged out EPRC.\nDo you want to quit?"):
            exit()
    
    def open_output_folder(self):
        # USe subprocess.Popen() to open the folder
        try:
            subprocess.run(['explorer', user.output_path], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error opening directory: {e}")
            

def check_username():
    username = readTxt("username.txt").strip()  
    userpath = os.path.join(r'C:\Users', username)
    if(os.path.exists(userpath) == False):
        print(f'Username: \'{username}\' does not exist!')
        tkinter.messagebox.showinfo('Error', f'Username: \'{username}\' does not exist!\n The program is terminated.')
        exit()
    else:
        print(f'Username: \'{username}\' exists!')
    return username

def main():
    global user

    # Set up for the alert UI
    root = tkinter.Tk()
    root.geometry("300x350")
    root.eval('tk::PlaceWindow . center')

    username = check_username()
    user = User(username)
    user.printUserInformation()
    fileExistOrCreate(user.input_path)
    fileExistOrCreate(user.fullscreen_path)
    load_samplePhotos()

    print('\n...The program is running...')

    app = SimpleUI(root)
    root.mainloop()    

    # End the program
    print('The program is terminated...')
    exit()

if __name__ == "__main__":
    main()