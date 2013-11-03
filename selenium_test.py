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
                
        else:
            self.driver = webdriver.Remote(desired_capabilities=desired_capabilities,
                            command_executor="http://%s:%s/wd/hub" % (hostname, port))        
        self.driver.implicitly_wait(30)
        self.base_url = "http://www.imbus.de/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_imbus_site(self):
        driver = self.driver
    	driver.find_element_by_link_text("English").click()
        driver.find_element_by_link_text("An-/Abreise (D)").click()
        driver.find_element_by_link_text(u"Produktvorträge").click()
        driver.find_element_by_link_text("Software-QS-Tag Special").click()
        try: self.assertEqual("Software-QS-Tag 2013 - Software-QS-Tag Special", driver.title)
        except AssertionError as e: self.verificationErrors.append(str(e))
        self.assertEqual("Software-QS-Tag 2013 - Software-QS-Tag Special", driver.title)
        self.assertRegexpMatches(driver.find_element_by_xpath("//div[@id='c16710']/p[2]").text, "^exact:Die perfekte Mischung aus Theorie und Praxis: Verbinden Sie Ihre Konferenzteilnahme am Software-QS-Tag mit einem zusätzlichen Ein-Tages-Training zu explorativem Testen\\. \nDas Paket: Ein Tag Training Exploratives Testen + zwei Tage Software-QS-Tag für 1\\.350,00 EURO[\\s\\S]*\\. Mit der kombinierten Buchung sparen Sie über 10% gegenüber dem  Einzelpreis der Schulung und zahlen je Teilnehmer den Sonderpreis von 500 Euro \\(zzgl\\. Mwst\\.\\) je Schulung\\.$")
        self.assertEqual("1. Tag:  Schulung Exploratives Testen", driver.find_element_by_css_selector("#c16680 > h1").text)
        driver.find_element_by_link_text("Contact").click()
        self.assertTrue(self.is_element_present(By.CSS_SELECTOR, "h1"))

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
