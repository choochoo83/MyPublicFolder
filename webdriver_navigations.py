from selenium import webdriver
import time, os, re
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pytest
os.system("cls")


driver = webdriver.Chrome()
driver.get("https://artoftesting.com/samplesiteforselenium")
driver.implicitly_wait(5)

# ===== click on the link button and check the linked page =====
# link_box = driver.find_element(By.CSS_SELECTOR, "a[href='http://www.artoftesting.com/sampleSiteForSelenium.html']")
# link_box.click()
# if driver.current_url == "https://artoftesting.com/samplesiteforselenium":
    # print("Passed")
# else:
    # print("Failed")

# ===== check if a text box exists then shows the entered value * dynamic data =====
# text_boxes = driver.find_elements(By.ID, "fname")
# if len(text_boxes) > 0:
    # print("Text box exists")
# else:
    # print("Text box doesn't exist")
# text_box = driver.find_element(By.ID, "fname")
# text_box.send_keys("SKChoo")
# if text_box.get_attribute("value") == "SKChoo":
    # print("Text is correct")
# else:
    # print("Text is wrong")

# ===== check a button exists then click on it ======
# buttons = driver.find_elements(By.ID, "idOfButton")
# if len(buttons) > 0:
    # print("Button exists")
# else:
    # print("Button doesn't exist")
# button = driver.find_element(By.ID, "idOfButton")
# button.click()

# ===== double click on a button then click on its popup =====
# button = driver.find_element(By.ID, "dblClkBtn")
# from selenium.webdriver.common.action_chains import ActionChains
# action = ActionChains(driver)
# action.double_click(button).perform()
# alert = driver.switch_to.alert
# alert.accept()

# ===== check a checkbox =====
# checkbox = driver.find_element(By.CSS_SELECTOR, "input[value='Automation']")
# checkbox.click()

# ===== select from a dropdown =====
# from selenium.webdriver.support.ui import Select
# dropdown = Select(driver.find_element(By.ID, "testingDropdown"))
# dropdown.select_by_visible_text("Manual Testing") 

# ===== drag and drop action from element A to element B =====
source_element = driver.find_element(By.CSS_SELECTOR, "#myImage")
target_element = driver.find_element(By.CSS_SELECTOR, "#targetDiv")
from selenium.webdriver.common.action_chains import ActionChains
action = ActionChains(driver)
action.drag_and_drop(source_element, target_element).perform()

time.sleep(2)
driver.quit()    

