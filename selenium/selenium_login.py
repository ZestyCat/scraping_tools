from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Firefox()

# Log in to boxrec
driver.get("")

username = ""
password = ""

userfield = driver.find_element(By.ID, "username")
passfield = driver.find_element(By.ID, "password")
submit = driver.find_element(By.CLASS_NAME, "submitButton")

userfield.send_keys(username)
passfield.send_keys(password)
submit.click()

# Start scraping

url = ""

for i in range(1, 100):
    driver.get(url + str(i))
    xpath = ""
    item = driver.find_element(By.XPATH, name).text
