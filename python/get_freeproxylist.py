from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import pandas as pd
import csv
import requests

def get_proxies(fmt = None, n = None, https = True, 
        method = "selenium", savename = "./proxies/free-proxy-list"):

    url = "https://free-proxy-list.net/"
    if method == "selenium":
        options = Options()
        ua = UserAgent()
        userAgent = ua.random
        options.add_argument(f"user-agent={userAgent}")
        driver = uc.Chrome(options=options, use_subprocess=True)
        driver.get(url)
        WebDriverWait(driver, 10).until( \
                EC.presence_of_element_located((By.CLASS_NAME, "table")))
        html = driver.page_source
        driver.quit()
    elif method == "requests":
        html = requests.get(url).content
    else:
        print("Expected method = selenium or method = requests.")

    soup = BeautifulSoup(html)
    table = soup.find_all("table")[0]
    rows = table.find_all("tr")

    table_data = []
    for row in rows:
        data = [td.text for td in row]
        if https:
            data = [d for d in data if data[6] == "yes"]
        if len(data) != 0:
            table_data.append(data)

    if n:
        table_data = table_data[1:n+1]
    else:
        table_data = table_data[1:]

    if fmt == "csv":
        with open (f"{savename}.csv", "w") as f:
            writer = csv.writer(f)
            writer.writerow( \
                    ["ip", "port", "code", "country", \
                    "anonymity","google", "https", "last checked"])
            for row in table_data[1:]:
                writer.writerow(row)
    elif fmt == "txt":
        with open (f"{savename}.txt", "w") as f:
            for row in table_data:
                f.write(f"{row[0]}:{str(row[1])}\n")
    elif fmt is None:
        pass
    else:
        print("Expected fmt=csv or fmt=txt, or fmt=None.")


    return table_data

if __name__ == "__main__":
    get_proxies(method="requests", n=25, fmt="txt")
    get_proxies(method="requests", n=25, fmt="csv")
