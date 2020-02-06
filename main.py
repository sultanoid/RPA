import os
import sys
import traceback
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary


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


class CollectInfoFromRemittance(object):

    def __init__(self):
        self.browser = webdriver.Firefox(executable_path=GECKODRIVER, firefox_binary=FIREFOX_BINARY, firefox_profile=PROFILE, )

    def get_all_data(self):
        noOfRows = len(self.browser.find_elements_by_xpath("//tr"))
        noOfColumns = len(self.browser.find_elements_by_xpath("//tr[2]/td"))
        allData = []

        for i in range(2, noOfRows):
            ro = []
            for j in range(1, noOfColumns):
                ro.append(self.browser.find_element_by_xpath("//tr[" + str(i) + "]/td[" + str(j) + "]").text)
            allData.append(ro)

        return allData

    def login(self, email, password):
        self.browser.get("http://10.11.200.84:8085/remittance/index.jsp")
        self.browser.maximize_window()

        self.browser.find_element_by_name('inputEmail').send_keys(email)
        self.browser.find_element_by_name('inputPassword').send_keys(password)
        self.browser.find_element_by_id('loginbutton').click()
        time.sleep(1)

        present = True
        alert_dialog = self.browser.find_elements_by_class_name("login")
        if len(alert_dialog) <= 0:
            present = False

        if present:
            print("There's some error in log in.")
            print(sys.exc_info()[0])
            self.browser.close()
            exit()
        else:
            print("Login is successfull")
            return

    def logout(self):
        time.sleep(2)
        element = self.browser.find_element_by_id("lgout")
        element.click()
        time.sleep(3)
        self.browser.close()

if __name__ == "__main__":

    email = "remit"  # input("Enter your email/username : ")
    password = "remit"  # getpass.getpass(prompt='Enter Password:')

    try:
        C = CollectInfoFromRemittance()
        C.login(email, password)
        row_list_data = C.get_all_data()
        for row in row_list_data:
            fullname = row[1]+" "+row[2]
            print(row)
        C.logout()

    except Exception as e:
        print("type error: " + str(e))
        print(traceback.format_exc())
