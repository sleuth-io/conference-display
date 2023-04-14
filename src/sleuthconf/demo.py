

class Demo:

    def __init__(self):
        self.driver = None

    def start(self):
        from selenium import webdriver

        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_argument("--no-sandbox")
        chromeOptions.add_argument("--disable-setuid-sandbox")
        chromeOptions.add_argument("--disable-dev-shm-using")
        chromeOptions.add_argument("--disable-extensions")
        chromeOptions.add_argument("--start-fullscreen")
        chromeOptions.add_argument("disable-infobars")
        chromeOptions.add_experimental_option("useAutomationExtension", False)
        chromeOptions.add_experimental_option("excludeSwitches", ["enable-automation"])
        chromeOptions.add_argument("--remote-debugging-port=9222")
        driver = webdriver.Chrome(chrome_options=chromeOptions)
        driver.get('https://app.sleuth.io/sleuth/sleuth/')
        self.driver = driver

    def stop(self):
        if self.driver:
            self.driver.quit()
