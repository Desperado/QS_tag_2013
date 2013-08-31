from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest, time, re

class Untitled(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://www.qs-tag.de/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_untitled(self):
        driver = self.driver
        driver.get(self.base_url + "/home/")
        driver.find_element_by_link_text("07. November 2013").click()
        driver.find_element_by_xpath("//div[@id='c16188']/div/div/div[3]/p/a/strong").click()
        self.assertEqual("Full Featured Test Automation using Selenium Grid and CI (Jenkins)", driver.find_element_by_css_selector("h1").text)
        self.assertEqual("07.11.2013, 14:00 - 15:30 / Ruslan Strazhnyk, Maven Research Inc.", driver.find_element_by_css_selector("p").text)
        driver.find_element_by_link_text("Veranstaltungsinfo").click()
        self.assertEqual("Software-QS-Tag Archiv", driver.find_element_by_link_text("Software-QS-Tag Archiv").text)
    
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException, e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
