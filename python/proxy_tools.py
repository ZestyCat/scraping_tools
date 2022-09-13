from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import csv
import random
import requests

import proxy_tools as pt

def get_proxies(fmt = None, n_proxies = None, return_fmt = "list", https = True, 
        method = "requests", countries = None, savename = "./proxies/free-proxy-list"):
    """ Get a list of proxies either using requests or selenium """
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

    soup = BeautifulSoup(html, features="lxml")
    table = soup.find_all("table")[0]
    rows = table.find_all("tr")

    table_data = []
    for row in rows:
        data = [td.text for td in row]
        if https:
            data = [d for d in data if data[6] == "yes"]
        if len(data) != 0:
            table_data.append(data)

    if countries:
        table_data = [t for t in table_data[1:] \
                if t[2] in countries or t[3] in countries]

    if n_proxies:
        table_data = table_data[1:n_proxies+1]
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

    if return_fmt == "list":
        return [f"{row[0]}:{str(row[1])}" for row in table_data]
    elif return_fmt == "dataframe":
        return table_data
    else:
        print("unrecognized return format. choose list or dataframe.")
    return []

def rotate_proxies(proxy_list, url, **kwargs):
    while True:
        try:
            p = random.randint(0, len(proxy_list) - 1)
            proxies = {"http": proxy_list[p], "https" : proxy_list[p]}
            response = requests.get(url, proxies=proxies, **kwargs)
            if response.status_code > 400:
                raise Exception(f"server returned error {response.status_code}")
            print(f"using proxy {proxy_list[p]} to access {url}")
            break
        except:
            print("error, looking for another proxy...")
    return response


class StealthDriver():
    """ Undetected chromdriver, random user agent, rotating proxies """
    def __init__(self, **kwargs):
        print("getting proxies...")
        self.proxies = pt.get_proxies(**kwargs)
    
    def init_driver(self, proxy=None):
        if hasattr(self, "driver"):
            self.driver.quit()
        ua = UserAgent()
        userAgent = ua.random
        options = uc.ChromeOptions()
        options.add_argument(f"user-agent={userAgent}")
        if proxy:
            options.add_argument(f"--proxy-server={proxy}")
        options.add_argument("--disable-javascript")
        self.driver = uc.Chrome(options=options, use_subprocess=True)

    def proxy_get(self, url, callback=None, **kwargs):
        for proxy in self.proxies:
            try:
                self.init_driver(proxy)
                self.driver.get(url)
                print(f"using proxy {proxy}.")
                if callback:
                    try:
                        callback(self.driver, **kwargs)
                        break
                    except:
                        raise Exception
                break
            except:
                print("rotating to another proxy...")
                self.driver.quit()
