from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
import undetected_chromedriver as uc
from selenium_stealth import stealth
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import pandas as pd

options = Options()
ua = UserAgent()
userAgent = ua.random

options.add_argument(f"user-agent={userAgent}")

driver = uc.Chrome(options=options, use_subprocess=True)

stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )

for page in range(1, 11):

    url = f"https://www.freeproxylists.net/?page={page}"

    driver.get(url)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "DataGrid")))

    html = driver.page_source

    soup = BeautifulSoup(html)

    table = soup.find_all("table")[1]

    rows = table.find_all("tr")

    table_data = []
    for row in rows:
        data = [td.text for td in row]
        table_data.append(data)

    df = pd.DataFrame(table_data, columns=["ip", "port", "protocol", "anonymity", \
                "country", "region", "city", "uptime", "response", "transfer"])

    with open ("./proxies/freeproxylist.csv", "a") as f:
        df.to_csv("./proxies/freeproxylist.csv", header=f.tell()==0)
