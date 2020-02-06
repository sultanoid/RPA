import time

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from remittance.capcha import Capcha

class Remittance(object):

    def __init__(self,driver):
        self.driver = driver
        self.capcha = Capcha(driver)
        time.sleep(2)

    def login(self,username, password):
        self.driver.get('http://10.88.1.21:7777/amluat/f?p=GUMS:101:0')
        self.driver.find_element_by_name("P101_USERNAME").send_keys(username)
        self.driver.find_element_by_name("P101_PASS").send_keys(password)

        time.sleep(2)
        capchaText = self.capcha .readCapchaFromImage()
        print(capchaText)
        capchaText = input('Please enter the capcha ')
        capchaField = self.driver.find_element_by_id("P101_CAPTCHA").send_keys(capchaText)
        self.driver.find_element_by_id('B72277838335750912').click()  # submit login form

    def remittanceCollection(self):
        WebDriverWait(self.driver, 10).until_not(EC.presence_of_element_located((By.CLASS_NAME, "t-Card-wrap")))
        self.driver.find_element_by_link_text("Conventional Agent Banking").click();

