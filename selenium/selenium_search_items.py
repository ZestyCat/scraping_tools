import csv
import time
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# web driver
browser = webdriver.Firefox()

# fill search form
def fill_search_form(driver, location):
    loc_xpath = '//*[@id="locationInput"]'
    loc_input = WebDriverWait(driver, 10) \
        .until(EC.element_to_be_clickable((By.XPATH, loc_xpath)))
    print("filling form...")
    loc_input.clear()
    loc_input.send_keys([l for l in location])
    time.sleep(2)
    # click in the field, select first entry
    browser.execute_script("arguments[0].click();", loc_input)
    time.sleep(2)
    loc_input.send_keys(Keys.ARROW_DOWN)
    time.sleep(2)
    loc_input.send_keys(Keys.ENTER)
    
# click search button
def click_item(driver, item, find_by = "xpath"):
    if find_by == "xpath":
        btn = WebDriverWait(driver, 10) \
            .until(EC.element_to_be_clickable((By.XPATH, item)))
    elif find_by == "class":
        btn = WebDriverWait(driver, 10) \
            .until(EC.element_to_be_clickable((By.CLASS_NAME, item)))
    elif find_by == "css_selector":
        btn = WebDriverWait(driver, 10) \
            .until(EC.element_to_be_clickable((By.CSS_SELECTOR, item)))
    elif find_by == "element":
        btn = item
    print("clicking button...")
    browser.execute_script("arguments[0].click();", btn)
    
def get_elements_by_class(driver, class_name):
    WebDriverWait(driver, 10) \
        .until(EC.presence_of_element_located((By.CLASS_NAME, class_name)))
    eles = browser.find_elements(By.CLASS_NAME, class_name)
    return eles

def get_element_text(driver, selector):
    WebDriverWait(driver, 3) \
        .until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
    ele = browser.find_element(By.CSS_SELECTOR, selector)
    return ele.text
