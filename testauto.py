import pyautogui
import win32.win32gui as win32gui

screen_width, screen_height = pyautogui.size()
print(f"Desktop resolution: {screen_width}x{screen_height}")

# Get the current mouse position
x, y = pyautogui.position()
print(f"Mouse position on desktop: ({x}, {y})")

# Move the mouse until there are 200 pixels to the right and 200 pixels down
pyautogui.moveTo(100, 100, duration=1)
print(win32gui.GetCursorInfo())

pyautogui.moveTo(1000, 100, duration=1)
print(win32gui.GetCursorInfo())
cursor = win32gui.GetCursorInfo()





























#adsasadsadadsa