#!/usr/bin/env python
#coding: utf8 
 
from testconfig import config
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
        self.base_url = "http://www.imbus.de/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_imbus_site(self):
        driver = self.driver
	driver.get(self.base_url)
	driver.find_element_by_link_text("English").click()
    	driver.find_element_by_link_text("Innovations in Detail").click()
    	driver.find_element_by_xpath("//div[@id='menue']/ul/li[5]/a/span").click()
    	driver.find_element_by_css_selector("a.last > span").click()
    	driver.find_element_by_xpath("//div[2]/ul/li[3]/a/span").click()
    	driver.find_element_by_css_selector("a.last > span").click()
    	driver.find_element_by_xpath("//div[2]/ul/li[2]/a/span").click()
    	self.assertEqual(u"Main Office Möhrendorf", driver.find_element_by_css_selector("h4").text)
    	self.assertEqual(u"imbus Rheinland GmbH\nMaternusstraße 44\n50996 Cologne", driver.find_element_by_css_selector("#c15819 > p").text)
    	driver.find_element_by_link_text("Test Tool List").click()
    	try: self.assertEqual("A Survey on Test Tools", driver.title)
    	except AssertionError as e: self.verificationErrors.append(str(e))

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
