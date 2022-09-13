from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def fill_form(driver, text, element, by = By.ID):
    input = WebDriverWait(driver, 10).until( \
        EC.presence_of_element_located((by, element)))
    print("sending input...")
    input.clear()
    input.send_keys(text)
   
def click_item(driver, element, by = By.ID):
    btn = WebDriverWait(driver, 10).until( \
        EC.element_to_be_clickable((by, element)))
    print("clicking button...")
    driver.execute_script("arguments[0].click();", btn)
    
def get_element_text(driver, element, by = By.ID):
    WebDriverWait(driver, 10).until( \
        EC.presence_of_element_located((by, element)))
    ele = driver.find_element(By.CSS_SELECTOR, element)
    return ele.text

def check_loaded(driver, by=By.ID, element=""):
    WebDriverWait(driver, 10).until( \
            EC.presence_of_element_located((by, element)))
