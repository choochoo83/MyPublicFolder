from selenium import webdriver
import time, os, re
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pytest
os.system("cls")

@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()
    driver.get("https://artoftesting.com/samplesiteforselenium")
    driver.implicitly_wait(5)
    yield driver
    driver.quit()

def test_linkbutton(driver):
    link_box = driver.find_element(By.CSS_SELECTOR, "a[href='http://www.artoftesting.com/sampleSiteForSelenium.html']")
    link_box.click()
    assert driver.current_url == "https://artoftesting.com/samplesiteforselenium", "Incorrect link"

def test_textbox_shows_the_entered_value_dynamic_data(driver):
    text_boxes = driver.find_elements(By.ID, "fname")
    assert len(text_boxes) > 0, "Text box doesn't exist"
    text_box = driver.find_element(By.ID, "fname")
    text_box.send_keys("SKChoo")
    assert text_box.get_attribute("value") == "SKChoo", "Text reading is wrong"

def test_check_button_exists_then_click(driver):
    buttons = driver.find_elements(By.ID, "idOfButton")
    assert len(buttons) > 0, "Button doesn't exist"
    button = driver.find_element(By.ID, "idOfButton")
    button.click()

def test_double_click_button_accept_popip(driver):
    button = driver.find_element(By.ID, "dblClkBtn")
    from selenium.webdriver.common.action_chains import ActionChains
    action = ActionChains(driver)
    action.double_click(button).perform()
    alert = driver.switch_to.alert
    alert.accept()

def test_check_checkbox(driver):
    checkbox = driver.find_element(By.CSS_SELECTOR, "input[value='Automation']")
    checkbox.click()

def test_select_from_dropdown(driver):
    from selenium.webdriver.support.ui import Select
    dropdown = Select(driver.find_element(By.ID, "testingDropdown"))pytest test_webdriver_navigations.py --testngxml=order.xml
    dropdown.select_by_visible_text("Manual Testing") 

def test_drag_and_drop_from_elementA_to_elementB(driver):
    source_element = driver.find_element(By.CSS_SELECTOR, "#myImage")
    target_element = driver.find_element(By.CSS_SELECTOR, "#targetDiv")
    from selenium.webdriver.common.action_chains import ActionChains
    action = ActionChains(driver)
    action.drag_and_drop(source_element, target_element).perform()

def test_quit_url(driver):
    time.sleep(2)
    
# To execute
# cmd> pytest test_webdriver_navigations.py                         >> by normal sequence
# cmd> pytest -n 7 test_webdriver_navigations.py                    >> by parallel
# cmd> pytest test_webdriver_navigations.py --testngxml=order.xml   >> by the priority or defined test order in the xml
    