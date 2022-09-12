from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
import undetected_chromedriver as uc
from selenium_stealth import stealth
from selenium import webdriver

options = Options()
#ua = UserAgent()
#userAgent = ua.random

userAgent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"

options.add_argument(f"user-agent={userAgent}")

driver = uc.Chrome(options=options, use_subprocess=True)
#driver = webdriver.Chrome(options=options)

# get stealth options from bot.sannysoft.com
#stealth(driver,
#        languages=["en-US", "en"],
#        vendor="Google Inc.",
#        platform="Linux x86_64",
#        webgl_vendor="Google Inc. (AMD)",
#        renderer="ANGLE (AMD, AMD Radeon RX 550 / 550 Series (polaris12 LLVM 14.0.6), OpenGL 4.6)",
#        fix_hairline=False,
#        )

# test on sannysoft
#driver.get("https://bot.sannysoft.com")

# test on coinfaucet
driver.get("https://coinfaucet.eu")
