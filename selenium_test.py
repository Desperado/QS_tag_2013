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
        self.base_url = "http://www.maven.co/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_imbus_site(self):
        driver = self.driver
	driver.get(self.base_url)
	self.assertEqual("Microconsulting", driver.find_element_by_css_selector("div.subnavigation > ul > li > a.active > span").text)
        self.assertEqual("Microconsulting", driver.find_element_by_css_selector("h1").text)
        driver.find_element_by_xpath("//div[@id='white-navbar']/div/ul/li[2]/a/span").click()
        self.assertEqual("Maven's global consultant network is comprised of thousands of professionals from virtually every conceivable background in over 150 countries worldwide. Our consultant network includes:", driver.find_element_by_css_selector("p").text)
        driver.find_element_by_css_selector("li.menu-25848 > a > span").click()
        try: self.assertEqual("Access the Global Knowledge Marketplace | Maven", driver.title)
        except AssertionError as e: self.verificationErrors.append(str(e))
        self.assertEqual("Access the Global Knowledge Marketplace | Maven", driver.title)
        try: self.assertTrue(self.is_element_present(By.CSS_SELECTOR, "div.centered-content.general-image"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertEqual("Access the Global Knowledge Marketplace | Maven", driver.title)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_css_selector("li.menu-34597.last > a > span").click()
        self.assertEqual("The Business of Halloween", driver.find_element_by_link_text("The Business of Halloween").text)
        driver.find_element_by_link_text("The Business of Halloween").click()
        self.assertEqual(u"MavenBlog » Blog Archive » The Business of Halloween", driver.title)
        driver.find_element_by_link_text("FAQ").click()
        driver.find_element_by_css_selector("li.menu-34597.last > a > span").click()
        driver.find_element_by_link_text("About Maven").click()
        self.assertEqual("Profit from What You Know | Maven", driver.title)
        self.assertTrue(self.is_element_present(By.CSS_SELECTOR, "div.about-maven-logo"))

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
