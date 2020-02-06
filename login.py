import os

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver import ActionChains
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from pytesseract import image_to_string, pytesseract
from PIL import Image
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

dir_path = os.path.dirname(os.path.realpath(__file__))
BROWSER_EXE = '/usr/bin/firefox'
GECKODRIVER = dir_path + '/geckodriver'
FIREFOX_BINARY = FirefoxBinary(BROWSER_EXE)

#  Code to disable notifications pop up of Chrome Browser

PROFILE = webdriver.FirefoxProfile()
# PROFILE.DEFAULT_PREFERENCES['frozen']['javascript.enabled'] = False
PROFILE.set_preference("dom.webnotifications.enabled", False)
PROFILE.set_preference("app.update.enabled", False)
PROFILE.update_preferences()


class CollectInfoFrom(object):

        def init(self):
            self.browser = webdriver.Firefox(executable_path=GECKODRIVER, firefox_binary=FIREFOX_BINARY,
                                             firefox_profile=PROFILE, )

        def simple(self):
            self.browser.get(url='https://www.google.com/recaptcha/api2/demo')

            # find iframe
            captcha_iframe = WebDriverWait(self.browser, 10).until(
                ec.presence_of_element_located(
                    (
                        By.TAG_NAME, 'iframe'
                    )
                )
            )

            ActionChains(self.browser).move_to_element(captcha_iframe).click().perform()

            # click im not robot
            captcha_box = WebDriverWait(self.browser, 10).until(
                ec.presence_of_element_located(
                    (
                        By.ID, 'g-recaptcha-response'
                    )
                )
            )

            self.browser.execute_script("arguments[0].click()", captcha_box)


        def get_captcha_text(location, size):
            pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract'
            im = Image.open('screenshot.png')  # uses PIL library to open image in memory

            left = location['x']
            top = location['y']
            right = location['x'] + size['width']
            bottom = location['y'] + size['height']

            im = im.crop((left, top, right, bottom))  # defines crop points
            im.save('screenshot.png')
            captcha_text = image_to_string(Image.open('screenshot.png'))
            return captcha_text


        def login_to_website(self):
            url = 'https://esearchigr.maharashtra.gov.in/testingesearch/Login.aspx'
            self.browser.get(url)
            self.browser.set_window_size(1120, 550)
            element = self.browser.find_element_by_xpath('//*[@id="form1"]/center/div[2]/div[3]/div[2]/div[2]/div/table/tbody/tr[3]/td[1]/img')  # find part of the page you want image of
            location = element.location
            size = element.size
            self.browser.save_screenshot('screenshot.png')
            user_id = self.browser.find_element_by_xpath('//*[@id="txtUserid"]')
            user_id.clear()
            user_id.send_keys('user-id')
            password = self.browser.find_element_by_xpath('//*[@id="txtPswd"]')
            password.clear()
            password.send_keys('password')
            captcha = self.browser.find_element_by_xpath('//*[@id="txtcaptcha"]')
            captcha.clear()
            captcha_text = self.get_captcha_text(location, size)
            captcha.send_keys(captcha_text)
            self.browser.find_element_by_xpath('//*[@id="btnLogin"]').click()

if __name__== "__main__":
        print("Hello World")
        c = CollectInfoFrom()
        c.simple()