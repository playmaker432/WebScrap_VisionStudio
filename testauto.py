import pyautogui
import time
import os
import win32.win32gui as win32gui

# Create a directory in /Documents called "Screenshots"
new_dir = os.path.join(os.path.expanduser('~'), 'Documents', 'Screenshots')
if not os.path.exists(new_dir):
    os.makedirs(new_dir)

# Create a new directory in the Screenshots directory and name it by the current time
new_dir = os.path.join(new_dir, time.strftime('%Y-%m-%d_%H-%M-%S'))
os.makedirs(new_dir)

screen_width, screen_height = pyautogui.size()
print(f"Desktop resolution: {screen_width}x{screen_height}")

# Get the current mouse position
x, y = pyautogui.position()
print(f"Mouse position on desktop: ({x}, {y})")

# Move the mouse until there are 200 pixels to the right and 200 pixels down
pyautogui.moveTo(400, 1000, duration=1)
print(win32gui.GetCursorInfo())

#Press F4 and hold down the mouse 
pyautogui.press('F4')

time.sleep(0.5)

pyautogui.mouseDown()

# Move the mouse until there are 200 pixels to the right and 200 pixels down
pyautogui.moveTo(100, 200, duration=1)
print(win32gui.GetCursorInfo())

pyautogui.mouseUp()

# Get the current mouse position
x, y = pyautogui.position()
print(f"Mouse position on desktop: ({x}, {y})")

time.sleep(0.5)

# Paste the address of the new_dir into the file explorer
pyautogui.typewrite(new_dir)

time.sleep(0.5)

# Press enter 
pyautogui.press('enter')
pyautogui.press('enter')

cursor = win32gui.GetCursorInfo()
# pointer code: 65539































#adsasadsadadsa