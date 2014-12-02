# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

class DoAddOne(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "https://apex.deusto.es/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_do_add_one(self):
        driver = self.driver
        driver.get(self.base_url + "/pls/apex/f?p=162:5:11553977739584::NO:::")
        driver.find_element_by_id("B16381221745222794").click()
        Select(driver.find_element_by_id("P6_PA_COD_PROYECTO")).select_by_visible_text("GO-LAB")
        Select(driver.find_element_by_id("P6_PA_COD_AREA_ACTIVIDAD")).select_by_visible_text("Unidad Internet")
        Select(driver.find_element_by_id("P6_PA_COD_TIPO_TRABAJO")).select_by_visible_text("I+D Desarrollo Proyecto")
        driver.find_element_by_css_selector("img.ui-datepicker-trigger").click()
        driver.find_element_by_css_selector("span.ui-icon.ui-icon-circle-triangle-w").click()
        driver.find_element_by_css_selector("span.ui-icon.ui-icon-circle-triangle-w").click()
        driver.find_element_by_css_selector("span.ui-icon.ui-icon-circle-triangle-w").click()
        driver.find_element_by_css_selector("span.ui-icon.ui-icon-circle-triangle-w").click()
        driver.find_element_by_id("P6_PA_FECHA").clear()
        driver.find_element_by_id("P6_PA_FECHA").send_keys("1/1/2014")
        driver.find_element_by_css_selector("div.uRegionContent.clearfix").click()
        driver.find_element_by_id("P6_HORAS").clear()
        driver.find_element_by_id("P6_HORAS").send_keys("1")
        driver.find_element_by_id("B16375215916222755").click()
    
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
