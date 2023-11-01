# Ref: http://www.eprc.com.hk/eprcLogin.html

from bs4 import BeautifulSoup
import selenium
import requests
import time
# Use pyautogui to take a screenshot
from pyautogui import screenshot
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
# import the actions module
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options

def current_time():
    return time.strftime("%Y%m%d-%H%M%S")

def sccreen_shot():
    # Take a screenshot
    img = screenshot()
    # Save the image
    img.save('screenshot-' + current_time() + '.png')



def main():
    # url = 'https://customer-uat-epic2.smartme.com.hk/property-list/buy/'
    url = 'http://www.eprc.com.hk/eprcLogin.html'

    service = Service(executable_path='C:\\Users\\raymondlaw\\Desktop\\SeleniumChrome\\chromedriver.exe')

    # Use selenium to take a screenshot
    options = Options()
    options.add_argument("--start-maximized")
    options.add_experimental_option("C:\\Users\\raymondlaw\\Desktop\\SeleniumChrome", "localhost:9014")

    driver = webdriver.Chrome(service = service, options=options)
    driver.get(url)

    time.sleep(5)

    # elementToBeClickable
    # <ion-toolbar _ngcontent-serverapp-c223="" mode="ios" class="content-container ion-no-padding toolbar-title-default ios in-toolbar hydrated"><ion-buttons _ngcontent-serverapp-c223="" slot="start" class="buttons-first-slot sc-ion-buttons-ios-h sc-ion-buttons-ios-s ios hydrated"><ion-button _ngcontent-serverapp-c223="" fill="clear" color="dark" class="back-button ng-star-inserted ion-color ion-color-dark ios button button-clear in-toolbar in-buttons ion-activatable ion-focusable hydrated" data-action="goBack"><ion-icon _ngcontent-serverapp-c223="" slot="start" name="chevron-back" mode="ios" aria-label="chevron back" role="img" class="ios hydrated"></ion-icon> 返回 </ion-button><!----><ion-button _ngcontent-serverapp-c223="" fill="clear" class="logo-link ios button button-clear in-toolbar in-buttons button-has-icon-only ion-activatable ion-focusable hydrated" tabindex="0"><img _ngcontent-serverapp-c223="" slot="icon-only" ngsrc="logo.png" class="logo" alt="smartME 智能地產平台" src="https://cdnprod.smartme.com.hk/smartme-general-image/logo.png?t=15010205"></ion-button></ion-buttons><ion-title _ngcontent-serverapp-c223="" class="ios title-default hydrated active"><ion-button _ngcontent-serverapp-c223="" tabindex="0" data-url="/agent-list" class="ng-star-inserted ion-color ion-color-agent ios button button-solid in-toolbar ion-activatable ion-focusable hydrated" color="agent">搵代理 </ion-button><ion-button _ngcontent-serverapp-c223="" tabindex="0" data-url="/property-list/buy" class="ng-star-inserted ion-color ion-color-sale ios button button-solid in-toolbar ion-activatable ion-focusable hydrated active" color="sale">買樓 </ion-button><ion-button _ngcontent-serverapp-c223="" tabindex="0" data-url="/property-list/rent" class="ng-star-inserted ion-color ion-color-lease ios button button-solid in-toolbar ion-activatable ion-focusable hydrated" color="lease">租樓 </ion-button><ion-button _ngcontent-serverapp-c223="" tabindex="0" data-url="/property-ad" class="ng-star-inserted ion-color ion-color-sell ios button button-solid in-toolbar ion-activatable ion-focusable hydrated" color="sell">放盤 </ion-button><!----></ion-title><ion-buttons _ngcontent-serverapp-c223="" slot="end" class="desktop sc-ion-buttons-ios-h sc-ion-buttons-ios-s ios hydrated"><ion-button _ngcontent-serverapp-c223="" routerlinkactive="active" tabindex="0" data-url="/agent" class="ng-star-inserted ion-color ion-color-dark-grey ios button button-clear in-toolbar in-buttons ion-activatable ion-focusable hydrated" color="dark-grey" fill="clear">代理專頁</ion-button><!----><!----><!----><ion-button _ngcontent-serverapp-c223="" routerlinkactive="active" tabindex="0" data-url="/news" class="ng-star-inserted ion-color ion-color-dark-grey ios button button-clear in-toolbar in-buttons ion-activatable ion-focusable hydrated" color="dark-grey" fill="clear">置 smart 資訊</ion-button><!----><!----><!----><ion-button _ngcontent-serverapp-c223="" routerlinkactive="active" tabindex="0" data-url="/estate" class="ng-star-inserted ion-color ion-color-dark-grey ios button button-clear in-toolbar in-buttons ion-activatable ion-focusable hydrated" color="dark-grey" fill="clear">屋苑專頁</ion-button><!----><!----><!----><!----><ion-button _ngcontent-serverapp-c223="" data-action="loggedInUser" class="ng-star-inserted ios button button-clear in-toolbar in-buttons ion-activatable ion-focusable hydrated" fill="clear" style="max-width: unset;"><span _ngcontent-serverapp-c223="" class="wrap-text"> HO MAN LAW </span></ion-button><!----><!----><!----><ion-button _ngcontent-serverapp-c223="" data-action="logout" class="ng-star-inserted ion-color ion-color-light ios button button-solid in-toolbar in-buttons ion-activatable ion-focusable hydrated" color="light" fill="solid" style="max-width: unset;"><span _ngcontent-serverapp-c223="" class="wrap-text"> 登出 </span></ion-button><!----><!----><!----><!----><!----><!----><!----><!----><!----><!----><!----></ion-buttons><ion-buttons _ngcontent-serverapp-c223="" slot="end" class="mobile buttons-last-slot sc-ion-buttons-ios-h sc-ion-buttons-ios-s ios hydrated"><ion-button _ngcontent-serverapp-c223="" fill="clear" color="dark" class="menu-button ion-color ion-color-dark ios button button-clear in-toolbar in-buttons ion-activatable ion-focusable hydrated" data-action="toggleMenu"><ion-icon _ngcontent-serverapp-c223="" name="menu-outline" aria-label="menu outline" role="img" class="ios hydrated"></ion-icon></ion-button></ion-buttons></ion-toolbar>
    ButtonBar = driver.find_elements(By.CLASS_NAME, 'button-solid')
    for button in ButtonBar:
        button.click()
        time.sleep(5)
        sccreen_shot()

    # Actions actions = new Actions(driver);
    # actions.moveToElement(element);
    # actions.perform();


if __name__ == '__main__':
    main()

