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



def main():
    global automation_thread
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    pyautogui.press('F4')
# Screenshoting the page
    pyautogui.moveTo(1186, 1010, duration = 0.5)
    pyautogui.dragTo(830, 255, duration=2.5)
    time.sleep(0.5)

if __name__ == "__main__":
    main()
