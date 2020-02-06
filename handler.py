import os
import time
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import pytesseract
from PIL import Image

from remittance.remittancePage import Remittance

dir_path = os.path.dirname(os.path.realpath(__file__))
BROWSER_EXE = '/usr/bin/firefox'
GECKODRIVER = dir_path + '/geckodriver'
FIREFOX_BINARY = FirefoxBinary(BROWSER_EXE)

PROFILE = webdriver.FirefoxProfile()
# PROFILE.DEFAULT_PREFERENCES['frozen']['javascript.enabled'] = False
PROFILE.set_preference("dom.webnotifications.enabled", False)
PROFILE.set_preference("app.update.enabled", False)
PROFILE.update_preferences()
dir_path = os.path.dirname(os.path.realpath(__file__))

class handler:
	def __init__(self):
		self.starting = '0842ar121011'
		self.username = 'SULTAN14'
		self.password = 'Bank@123'
		self.driver = webdriver.Firefox(executable_path=GECKODRIVER, firefox_binary=FIREFOX_BINARY, firefox_profile=PROFILE, )
		self.remittance = Remittance(self.driver)
		time.sleep(2)

	def remittanceCollection(self):
		self.remittance.remittanceCollection()
		pass

	def login(self,username,password):
		self.remittance.login(username,password)

	def process(self):
		self.login("SULTAN14", "Bank@123")
		self.remittanceCollection()


if __name__ == '__main__':
	h = handler()
	h.process()