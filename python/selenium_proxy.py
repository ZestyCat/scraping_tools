from fake_useragent import UserAgent
from selenium.webdriver.support.wait import WebDriverWait
import undetected_chromedriver as uc

from proxy_tools import get_proxies

print("getting proxies...")
proxies = get_proxies()

url = ""

for proxy in proxies:
    try:
        ua = UserAgent()
        userAgent = ua.random

        options = uc.ChromeOptions()
        options.add_argument(f"user-agent={userAgent}")
        options.add_argument(f"--proxy-server={proxy}")

        browser = uc.Chrome(options=options, use_subprocess=True)

        print(f"using proxy {proxy}.")

        browser.get(url)
        browser.quit()
        break
    except:
        print("rotating to another proxy...")
        browser.quit()
