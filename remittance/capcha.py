import os

import pytesseract
from PIL import Image


class Capcha(object):

    def __init__(self,driver):
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        self.driver = driver

    def deleteFile(self, path):
        if os.path.isfile(path) or os.path.islink(path):
            os.remove(path)  # remove the file
        pass

    # select course
    def readCapchaFromImage(self):
        name = 'capcha.png'
        file_name = self.dir_path + "/" + name
        print(file_name)
        self.deleteFile(file_name)

        self.take_screenshot(name)
        image_element = self.driver.find_element_by_xpath(
            "//span[contains(@class, 'Form-itemText t-Form-itemText--post')]/div")

        location = image_element.location
        size = image_element.size
        self.crop_image(name, location, size)
        text = self.recover_text(name).strip()  # capture image text

    # taking screenshot
    def take_screenshot(self, name):
        self.driver.save_screenshot(name)

    # cropping image
    def crop_image(self, name, location, size):
        image = Image.open(name)
        x, y = location['x'], location['y']
        w, h = size['width'], size['height']
        image.crop((x, y, x + w, y + h)).save(name)

    # retrieving text
    def recover_text(self, filename):
        image = Image.open(filename)
        r, g, b, a = image.split()  # removing the alpha channel
        image = Image.merge('RGB', (r, g, b))
        return pytesseract.image_to_string(image)
    pass