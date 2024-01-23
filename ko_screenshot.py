# import json
# import pandas as pd
# import numpy as np
# import os
# import time
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.remote.webelement import WebElement
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from subprocess import Popen
# from pyautogui import press, typewrite, hotkey
# import tkinter as tkinter
# from tkinter import messagebox
# import shutil


# kfl.super
# orange

import os
import time
import json
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from subprocess import Popen
from pyautogui import press, typewrite, hotkey
import tkinter as tkinter
from tkinter import messagebox
import shutil
from bs4 import BeautifulSoup

user = None
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
        print(content)
        # If the first 8 characters are digits, or the content is "NIL", it is a telephone number
        if(content[:8].isdigit() or content == "NIL"):
            telephone_series = telephone_series._append(pd.Series([content]), ignore_index=True)
        else:
            # if the last 8 characters are digits, it is a telephone number
            if(content[-8:].isdigit()):
                telephone_series = telephone_series._append(pd.Series([content[-8:]]), ignore_index=True)
                contact_series = contact_series._append(pd.Series([content[:-8]]), ignore_index=True) 
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
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    driver.get('https://portal.vision.cognitive.azure.com/demo/extract-text-from-images')

    button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div/main/div/div[2]/div[2]/div[5]/div/div[3]/div/div[2]/div/div[1]/button[2]"))) 
    button.click()

    return driver

def driver_eprc():
    desired_zoom_level = 1.5
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    # Set the device scale factor to adjust the zoom level
    options.add_argument(f"--force-device-scale-factor={desired_zoom_level}")
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    driver.get('https://eprc.com.hk/eprcLogin.html')

    return driver

def driver_eprcDemo():
    desired_zoom_level = 1.5
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    # Set the device scale factor to adjust the zoom level
    options.add_argument(f"--force-device-scale-factor={desired_zoom_level}")
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    driver.get('http://127.0.0.1:5500/eprcLogin.html')

    return driver


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

    # Use bs4 to fetch data in eprcLogin.html <- localhost:5500/eprcLogin.html


    global user

    try:
        #=================== The start of EPRC Demo ===================
        driver = driver_eprcDemo()
        driver.implicitly_wait(3)

        username_input = driver.find_element(By.NAME, 'userName')
        password_input = driver.find_element(By.NAME, 'password')

        # Input the username and password
        username_input.send_keys('123')
        password_input.send_keys('abc')

        # You can also submit the form if needed    
        driver.find_element(By.NAME, 'LoginForm').submit()

        driver.implicitly_wait(3)
        # =============================================================






        driver = driver_eprc()

        # Wait for the page to load (you might need to adjust the wait time)
        driver.implicitly_wait(3)

        # Find the username and password input elements by name
        username_input = driver.find_element(By.NAME, 'userName')
        password_input = driver.find_element(By.NAME, 'password')

        # Input the username and password
        username_input.send_keys('123')
        password_input.send_keys('abc')

        # You can also submit the form if needed
        # driver.find_element(By.NAME, 'LoginForm').submit()

        # Use Selenium to login
        # <input type="text" name="userName" tabindex="1" value="" id="userName" class="loginC">
        # //*[@id="userName"]
        # Input the username: "kfl.super" intp the html elment above
        # username = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='userName']")))
        # username.send_keys("kfl.super")

        # <input type="password" name="password" tabindex="2" value="" id="password" class="loginC">
        # /html/body/form/table[1]/tbody/tr[3]/td[3]/input
        # Input the password: "orange" into the html element above
        # password.send_keys("orange")

        # Alert dialog that tell the user to input the username and password
        tkinter.messagebox.showinfo('Information', 'Please click this buttton AFTER you LOGIN & SEARCH.')

    except Exception as e:
        tkinter.messagebox.showinfo('Error', f'Error occurs: {e}\n The program is terminated.')
        driver.quit()
        exit()

    #============================ The start of EPRC ============================
    
    # Use BS4 to get the HTML content
    html_content = driver.page_source
    print(html_content)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Use soup to find the username and password input box
    # <input type="text" name="userName" tabindex="1" value="" id="userName" class="loginC">
    # Input the username: "kfl.super" intp the html elment above

    # <input type="password" name="password" tabindex="2" value="" id="password" class="loginC">
    # Input the password: "orange" into the html element above
    # Find the username and password input elements

    # <input type="text" name="userName" tabindex="1" value="" id="userName" class="loginC">
    # Input the username: "kfl.super" intp the html elment above
    # username = soup.find('input', attrs={'name': 'userName'})
    # username['value'] = 'kfl.super'

    # <input type="password" name="password" tabindex="2" value="" id="password" class="loginC">
    # Input the password: "orange" into the html element above
    # password = soup.find('input', attrs={'name': 'password'})
    # password['value'] = 'orange'

    # Find the button using the provided XPath
    # button_xpath = "/html/body/table/tbody/tr/td/form/table[3]/tbody/tr[3]/td/table/tbody/tr[1]/td/table/tbody/tr/td[2]/table/tbody/tr/td[4]"
    # button = driver.find_element(By.XPATH, button_xpath)

    # First, Get the total number of searched properties
    
    # Total number of searched properties xpath:    
    # <td align="RIGHT">
    #   	<font class="txtChi17 pageRecordCountColor">  	
    #       		1 - 30 (共 Total 443)	
    #     </font>
    # </td>
    # /html/body/table/tbody/tr/td/form/table[1]/tbody/tr/td[4]/font
        
    # Next button xpath:
    # /html/body/table/tbody/tr/td/form/table[3]/tbody/tr[3]/td/table/tbody/tr[1]/td/table/tbody/tr/td[2]/table/tbody/tr/td[4]/a   
    #<a href="/EprcWeb/multi/asking/newAsking.do?opyearFrom=&amp;estateType=&amp;street=&amp;newTbldgId=&amp;type=&amp;askAlertSearch=&amp;presentTbldgId=&amp;streetNoFrom=&amp;askType=&amp;negotiateAsk=&amp;floorNoTo=&amp;changeNameTbldgId=&amp;nature=R%2CB&amp;page=2&amp;streetNoType=&amp;districtShadow=&amp;updateDateTo=28%2F12%2F2023&amp;isCrossDistrict=&amp;floorNoFrom=&amp;cbldgclasskey=&amp;status=&amp;streetNoTo=&amp;hiddenSortOrder=to_char%28a.cupdon%2C%27YYYYMMDD%27%29__desc%2Cdecode%28a.cowner%2C%27O%27%2C1%2C%27A%27%2C2%2C%27B%27%2C3%2C%27T%27%2C4%2C%27I%27%2C5%2C%27E%27%2C6%2C%27D%27%2C7%2C8%29__asc%2Cround%28ROW_NUMBER%28%29OVER%28PARTITION__BY__to_char%28a.cupdon%2C%27YYYYMMDD%27%29%2Ca.cowner%2Cac.ccontactchi__ORDER__BY__ac.ccontactchi__desc%29%2F3___0.5%2C0%29__asc&amp;cstreetcd=&amp;phoneNo=&amp;unitTo=&amp;ageFrom=&amp;floor=&amp;netTo=&amp;changeNameTestateId=&amp;hiddenSortOrderName2=&amp;todayAskType=&amp;updateDateFrom=18%2F11%2F2023&amp;unitFrom=&amp;room=&amp;ageTo=&amp;hiddenSortOrderName=&amp;dateRangeType=EXACT&amp;priceFrom=&amp;refNoTo=&amp;cddname=&amp;isToday=&amp;netFrom=&amp;grossTo=&amp;mode=newAsking&amp;rentFrom=10000&amp;quickPhone3=&amp;din=&amp;priceTo=&amp;quickPhone1=&amp;quickPhone2=&amp;estateId=&amp;district=KL%2CKL-TST%2CKL-YMT%2CKL-MK%2CKL-TKT%2CKL-SKM%2CKL-SSP%2CKL-CSW%2CKL-LCK%2CKL-HH%2CKL-HMT%2CKL-KTK%2CKL-KC%2CKL-KL%2CKL-WTH%2CKL-WTS%2CKL-TWS%2CKL-DH%2CKL-SPK%2CKL-NCW%2CKL-KB%2CKL-NTK%2CKL-KT%2CKL-LT%2CKL-KYT&amp;tbldgId=&amp;building=&amp;refNoFrom=&amp;opyearTo=&amp;bldgAgeType=AGE&amp;selectBuilding=&amp;dateType=UPD&amp;updateDate=180&amp;askAlertDays=&amp;cestateId=&amp;unit=&amp;source=O&amp;refNo=&amp;grossFrom=&amp;usage=RES&amp;method=&amp;rentTo=999999&amp;negotiateRent=&amp;estate=" class="btn btn-primary rounded-corners"><img src="../../common/images/buttons/nav_next.png" border="0" width="20" height="20" style="vertical-align: middle;">下頁&nbsp;Next</a>

    # searched_total_number = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/table/tbody/tr/td/form/table[1]/tbody/tr/td[4]/font"))).text

    # Get the total number by the class = txtChi17 pageRecordCountColor
    # searched_total_number = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "txtChi17.pageRecordCountColor"))).text
    # searched_total_page = int(searched_total_number[searched_total_number.find('共 Total ')+len('共 Total '):searched_total_number.find(')')])
    
    # /html/body/table/tbody/tr/td/form/table[3]/tbody/tr[3]/td/table/tbody/tr[1]/td/table/tbody/tr/td[2]/table/tbody/tr/td[4]
    
    page_count = 1

    # Get a screenshot every page
    while(page_count <= 2):
        print(f'Processing page {page_count}...')
        # Get the screenshot of the page
        driver.save_screenshot(f'page_{page_count}.png')

        # Click the next button
        # if(page_count != searched_total_page):

        # /html/body/table/tbody/tr/td/form/table[3]/tbody/tr[3]/td/table/tbody/tr[1]/td/table/tbody/tr/td[2]/table/tbody/tr/td[4]/a
        next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/table/tbody/tr/td/form/table[3]/tbody/tr[3]/td/table/tbody/tr[1]/td/table/tbody/tr/td[2]/table/tbody/tr/td[4]/a")))
        next_button.click()

        page_count += 1

    #============================ The end of EPRC ============================#

    driver.quit()

    # The 5 series are used to store the data
    chinese_address_series, english_address_series, telephone_series, contact_series, page_series = pd.Series(), pd.Series(), pd.Series(), pd.Series(), pd.Series()

    # Set up for the alert UI
    root = tkinter.Tk()
    root.withdraw()

    username = check_username()
    user = User(username)
    user.printUserInformation()
    fileExistOrCreate(user.input_path)
    load_samplePhotos()

    try:            
        address_files = os.listdir(user.address_path)
        contact_files = os.listdir(user.contact_path)
        print(contact_files)

        check_inputLens()

        driver = driver_setup()
        
        try:
            address_files_sorted = sorted(address_files,key=lambda x: int(os.path.splitext(x)[0]))
            for file in address_files_sorted:
                print('\nUploading the file: ' + file)
                file_path = os.path.join(user.address_path, file)
                json_data = upload_file(driver, file_path)
                chinese_address_series, english_address_series = separate_address(json_data, chinese_address_series, english_address_series)

        except Exception as e:
            tkinter.messagebox.showinfo('Error', f'Error occurs: {e}\n The program is terminated.')
            driver.quit()
            exit()
            
        try:
            contact_files_sorted = sorted(contact_files,key=lambda x: int(os.path.splitext(x)[0]))
            for file in contact_files_sorted:
                print('\nUploading the file: ' + file)
                file_path = os.path.join(user.contact_path, file)
                json_data = upload_file(driver, file_path)
                # print(telephone_series, contact_series)
                telephone_series, contact_series = separate_contact(json_data, telephone_series, contact_series)
        
        except Exception as e:
            tkinter.messagebox.showinfo('Error', f'Error occurs: {e}\n The program is terminated.')
            driver.quit()
            exit()

        driver.quit()
        
        address_df = build_outputDF(chinese_address_series, english_address_series, contact_series, telephone_series, page_series)
        print(address_df)
        generate_output(address_df)
        
        exit()

    except Exception as e:
        tkinter.messagebox.showinfo('Error', f'Error occurs: {e}\n The program is terminated.')
        driver.quit()
        exit()

if __name__ == "__main__":
    main()