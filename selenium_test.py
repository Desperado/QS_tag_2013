#!/usr/bin/env python
#coding: utf8 

from selenium import webdriver
from selenium.webdriver.common.by import By
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
        nodeName = str(config['environment']['nodeName'])
        version  = str(config['environment']['version'])

        desired_capabilities = dict(platform=platform, browserName=browser,
                            version=version, cssSelectorsEnabled=True,
                            setAcceptUntrustedCertificates=True,
                            INTRODUCE_FLAKINESS_BY_IGNORING_SECURITY_DOMAINS=True,
                           setPreference = ("network.http.phishy-userpass-length", 255))
        desired_capabilities["jenkins.nodeName"]=nodeName
            
        if browser == 'chrome_real':
            self.driver = webdriver.Chrome()
                
        else:
            self.driver = webdriver.Remote(desired_capabilities=desired_capabilities,
                            command_executor="http://%s:%s/wd/hub" % (hostname, port))        
        self.driver.implicitly_wait(30)
        self.base_url = "http://www.imbus.de/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_imbus_site(self):
        driver = self.driver
        self.assertTrue(self.is_element_present(By.CSS_SELECTOR, "img"))
        driver.find_element_by_link_text("Referenzen").click()
        driver.find_element_by_link_text("Tool-Liste").click()
        self.assertEqual(u"Softwaretest Werkzeuge im Überblick", driver.title)
        self.assertEqual("Testtool Review", driver.find_element_by_css_selector("strong").text)
        driver.find_element_by_link_text("English").click()
        self.assertEqual("A Survey on Test Tools", driver.title)
        self.assertEqual("SOFTWARE TESTING SERVICES", driver.find_element_by_xpath("//div[@id='menue']/ul/li[2]/a/span").text) 
	    
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
