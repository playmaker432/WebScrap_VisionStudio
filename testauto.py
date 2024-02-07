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

    pyautogui.moveTo(1350, 1010, duration = 0.3)

    time.sleep(3)

    # Print the screen resolution
    print(pyautogui.size())

    cursor = win32gui.GetCursorInfo()
    cursor_pos = pyautogui.position()
    print(cursor)

    # print cursor
    print(pyautogui.position())

if __name__ == "__main__":
    main()
