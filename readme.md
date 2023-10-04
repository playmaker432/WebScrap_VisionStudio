# OCR Tool

## Description

This tool is used to extract text from images and output Chinese & English addresses . It uses the OCR (Azure AI Vision Audio) to perform the extraction by autiomation (Selenium).

## Progress

- (Current development): The program is expected to be run as an executable file.
- The python script has been done.
- The program can be run in the command line.

## Pre-requisites

### Python libraries

This python program will import the following libraries:

```python
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
```

### Other requirements

- The program is developed in Python 3.7.3.
- The program is developed in Windows 10.
- Before the program runs, please make sure that the following files are created: (For example)
  - 'C:\Users\raymondlaw\Pictures\Greenshots_input\Greenshots_address'
  - 'C:\Users\raymondlaw\Pictures\Greenshots_input\Greenshots_contact'
  - 'C:\Users\raymondlaw\Pictures\Greenshots_output'
- The 1st and 2nd directory is used to store the input images (address and contact separately).
- The 3rd directory is used to store the output Excel file

## How to use

### ( TBC... )

## Constraints

## OCR Website link

<a href="https://portal.vision.cognitive.azure.com/demo/extract-text-from-images">Azure AI Vision Audio</a>
