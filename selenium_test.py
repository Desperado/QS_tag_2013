#!/usr/bin/env python
#coding: utf8 
 
from testconfig import config
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest, time, re

class ImbusTest(unittest.TestCase):
    def setUp(self):
	hostname = str(config['environment']['hostname'])
        port     = str(config['environment']['port'])
        browser  = str(config['environment']['browser'])
        url      = str(config['environment']['url'])
        platform = str(config['environment']['platform'])

        desired_capabilities = dict(platform=platform, browserName=browser,
                             cssSelectorsEnabled=True,
                            setAcceptUntrustedCertificates=True,
                            INTRODUCE_FLAKINESS_BY_IGNORING_SECURITY_DOMAINS=True,
                           setPreference = ("network.http.phishy-userpass-length", 255))
        if browser == 'chrome_real':
            self.driver = webdriver.Chrome()
	elif browser == 'firefox_real':
	    self.driver = webdriver.Firefox()
                
        else:
            self.driver = webdriver.Remote(desired_capabilities=desired_capabilities,
                            command_executor="http://%s:%s/wd/hub" % (hostname, port))        
        self.driver.implicitly_wait(30)
        self.base_url = "http://www.maven.co/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_maven_surveys(self):
        driver = self.driver
        driver.get(self.base_url)
        driver.find_element_by_link_text("Electronic Surveys").click()
        self.assertEqual("Survey Experts | Maven", driver.title)
        self.assertEqual("Electronic Surveys", driver.find_element_by_css_selector("h1").text)
        self.assertTrue(self.is_element_present(By.CSS_SELECTOR, "div.surveys-image"))
        self.assertEqual("How it Works", driver.find_element_by_css_selector("div.centered-content > h1").text)
        driver.find_element_by_css_selector("img[alt=\"Maven\"]").click()

    def test_maven_consultations(self):
	driver = self.driver
	driver.get(self.base_url)
        driver.find_element_by_link_text("Telephone Consultations").click()
        self.assertEqual("Consult with an Expert | Maven", driver.title)
        self.assertTrue(self.is_element_present(By.CSS_SELECTOR, "div.centered-content.general-image"))
        self.assertTrue(self.is_element_present(By.CSS_SELECTOR, "div.centered-content > h1"))
        driver.find_element_by_css_selector("img[alt=\"Maven\"]").click()
        driver.find_element_by_link_text("Intelligence Markets").click()
        self.assertTrue(self.is_element_present(By.CSS_SELECTOR, "div.right-col.markets-image"))
        self.assertEqual("Intelligence Markets | Maven", driver.title)
        self.assertEqual("", driver.find_element_by_css_selector("a.blank-window.linkedin").text)
        self.assertTrue(self.is_element_present(By.CSS_SELECTOR, "a.blank-window.google"))

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
