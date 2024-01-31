import pyautogui
import time
import win32.win32gui as win32gui
import keyboard
import tkinter as tk
from tkinter import messagebox
import threading
import os
from selenium import webdriver

stop_automation = threading.Event()
automation_thread = None  # Global variable to store the thread

def automation_function():
    # Diminish the zoom level to 80% in Google Chrome (Press 'Ctrl' + '-')
    time.sleep(5)

    page_cnt = 1  
    while not stop_automation.is_set():
        pyautogui.press('F4')
        pyautogui.moveTo(1060, 1010, duration=0.5)
        pyautogui.dragTo(830, 275, duration=0.5)
        time.sleep(0.5)
        pyautogui.press('enter')

        pyautogui.moveTo(1770, 1025, duration=0.5)
        cursor = win32gui.GetCursorInfo()
        time.sleep(2)
        pyautogui.click(1873, 969)
        time.sleep(2)

        if cursor[1] == 65567:
            print('Clicked the \'Next Page\' button!')
            pyautogui.click()
            time.sleep(2)
            page_cnt += 1
        else:
            print('Cannot find any \'Next Page\' button!')
            break

    print(f'\nFinished. There are {page_cnt} pages in total.')
    messagebox.showinfo('Information', 'Finish screenshooting.\nPLEASE REMEMBER TO LOG OUT EPRC!')

def on_key_event(event):
    global automation_thread

    if event.name == 'f2':
        stop_automation.set()
        print('Pressed \'F2\'')

        # Wait for the automation thread to finish
        if automation_thread:
            automation_thread.join()

def check_thread_status():
    if automation_thread and not automation_thread.is_alive():
        messagebox.showinfo('Information', 'Finish screenshooting.\nPLEASE REMEMBER TO LOG OUT EPRC.')


def driver_eprc():
    desired_zoom_level = 1.5
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    driver.execute_script(f"document.body.style.zoom='80%';")
    driver.get('https://eprc.com.hk/eprcLogin.html')

    return driver


def main():
    global automation_thread
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    driver = driver_eprc()
    


def driver_setup():
    # Press Ctrl + T to create new tab 
    pyautogui.hotkey('ctrl', 't')

    # Open Vision Studio: https://portal.vision.cognitive.azure.com/demo/extract-text-from-images
    pyautogui.typewrite('https://portal.vision.cognitive.azure.com/demo/extract-text-from-images')
    

if __name__ == "__main__":
    main()
