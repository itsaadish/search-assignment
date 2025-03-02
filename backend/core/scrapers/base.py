# # backend/core/scrapers/base.py
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# class BaseScraper:
#     def __init__(self, headless=True):
#         options = webdriver.ChromeOptions()
#         if headless:
#             options.add_argument("--headless=new")
#         self.driver = webdriver.Chrome(options=options)
#         self.wait = WebDriverWait(self.driver, 20)

#     def search_product(self, parsed_query):
#         raise NotImplementedError
        
#     def get_results(self):
#         raise NotImplementedError
        
#     def close(self):
#         self.driver.quit()

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service

class BaseScraper:
    def __init__(self, headless=True, use_proxy=False):
        options = webdriver.ChromeOptions()
        # options.binary_location = "/usr/bin/chromium"  # Chromium binary path
        # options.add_argument("--no-sandbox")  # Essential for Docker
        # options.add_argument("--disable-dev-shm-usage")  # Prevent resource issues
        
        # Set a realistic user-agent
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )

        # Disable automation detection
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)

        if headless:
            options.add_argument("--headless=new")
        
        # Use a proxy if required
        if use_proxy:
            proxy = "http://YOUR_PROXY_IP:PORT"  # Replace with actual proxy
            options.add_argument(f"--proxy-server={proxy}")
        # service = Service("/usr/bin/chromedriver")  # Chromedriver path
       
        self.driver = webdriver.Chrome(
            # service=service,
            options=options)
        self.wait = WebDriverWait(self.driver, 20)

        # Further prevent detection
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    def search_product(self, parsed_query):
        raise NotImplementedError
        
    def get_results(self):
        raise NotImplementedError
        
    def close(self):
        self.driver.quit()
