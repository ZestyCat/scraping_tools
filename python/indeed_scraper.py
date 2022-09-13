import time
from fake_useragent import UserAgent
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc

import proxy_tools as pt
import selenium_functions as sf

""" USER INPUT """
job_search = "environmental modeling"
location = "San Diego, CA"
""" END USER INPUT """

sd = pt.StealthDriver(countries="US")

# get indeed. Callback used to check whether page loads correctly
sd.proxy_get("https://www.indeed.com/", \
        callback = sf.check_loaded, by=By.ID, element="indeed-globalnav-logo")

sf.fill_form(sd.driver, job_search, "text-input-what", by=By.ID)
sf.fill_form(sd.driver, location, "text-input-where", by=By.ID)
sf.click_item(sd.driver, \
                "yosegi-InlineWhatWhere-primaryButton", by=By.CLASS_NAME)

time.sleep(5)

sd.driver.quit()
