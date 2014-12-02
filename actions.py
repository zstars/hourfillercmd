

from collections import OrderedDict
import json
from selenium.webdriver import FirefoxProfile
import config


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException


import time
import os

START_URL = "https://apex.deusto.es/pls/apex/f?p=162:5:7554643543408::NO:6::"
LOGIN_URL = "https://loginp.deusto.es/sso/prueba/login.jsp"

class TimeoutException(Exception):
    pass

class Action(object):

    def __init__(self):

        if config.USE_HEADLESS:
            self.driver = webdriver.PhantomJS()
        else:
            self.profile = FirefoxProfile()
            self.profile.set_preference("security.tls.version.fallback-limit", 0)
            self.profile.set_preference("security.tls.version.min", 0)
            self.driver = webdriver.Firefox(self.profile)

        self.driver.set_window_size(1600, 1200)
        self.driver.implicitly_wait(30)

        self.verificationErrors = []
        self.accept_next_alert = True

    def _close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True

    def _wait_for_element_id(self, id):
        sofar = 0
        while True:
            try:
                self.driver.find_element_by_id(id)
            except:
                time.sleep(0.5)
                sofar += 0.5
                if sofar > 20:
                    raise TimeoutException
            else:
                break

    def _wait_for_not_visible(self, id):
        sofar = 0
        while True:
            try:
                elem = self.driver.find_element_by_id(id)
                if not elem.is_displayed():
                    break
                else:
                    time.sleep(0.5)
                    sofar += 0.5
                    if sofar > 20:
                        raise TimeoutException
            except:
                pass

    def is_at_home(self):
        """
        Checks whether we are currently in the app home page, and thus able to start adding entries.
        :return: True if we are in the app home page, false otherwise.
        :rtype: bool
        """
        try:
            self.driver.find_element_by_id("B16381221745222794")  # Add new button
        except:
            return False
        else:
            return True

    def wait_for_home(self):
        """
        Waits until we are at the home screen and thus able to add new entries.
        :return:
        """
        self._wait_for_element_id("B16381221745222794")

    def login(self):
        """
        Logins to the app if not alaready logged in.
        :return:
        """
        print "Logging in... "

        driver = self.driver
        driver.get(START_URL)
        driver.find_element_by_name("ssousername").clear()
        driver.find_element_by_name("ssousername").send_keys(config.DEUSTO_USERNAME)
        driver.find_element_by_name("password").clear()
        driver.find_element_by_name("password").send_keys(config.DEUSTO_PASSWORD)
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()

        self._wait_for_element_id("B16381221745222794")

        print " done."

    def add_entry(self, project, unit, concept, date, hours):

        print "Adding entry... "

        driver = self.driver

        # Click the add new btn
        driver.find_element_by_id("B16381221745222794").click()
        Select(driver.find_element_by_id("P6_PA_COD_PROYECTO")).select_by_visible_text(project)
        Select(driver.find_element_by_id("P6_PA_COD_AREA_ACTIVIDAD")).select_by_visible_text(unit)
        Select(driver.find_element_by_id("P6_PA_COD_TIPO_TRABAJO")).select_by_visible_text(concept)
        driver.find_element_by_css_selector("img.ui-datepicker-trigger").click()
        driver.find_element_by_css_selector("span.ui-icon.ui-icon-circle-triangle-w").click()
        driver.find_element_by_css_selector("span.ui-icon.ui-icon-circle-triangle-w").click()
        driver.find_element_by_css_selector("span.ui-icon.ui-icon-circle-triangle-w").click()
        driver.find_element_by_css_selector("span.ui-icon.ui-icon-circle-triangle-w").click()
        driver.find_element_by_id("P6_PA_FECHA").clear()
        driver.find_element_by_id("P6_PA_FECHA").send_keys(date)
        driver.find_element_by_css_selector("div.uRegionContent.clearfix").click()
        driver.find_element_by_id("P6_HORAS").clear()
        driver.find_element_by_id("P6_HORAS").send_keys(hours)
        driver.find_element_by_id("B16375215916222755").click()

        self.wait_for_home()

        print " done."

    def add_entries(self, entries):
        """
        Massively adds the specified entries.
        Entries is a list of dicts.
        Example:
               [
                {
                    "project": "GO-LAB",
                    "unit": "Unidad Internet",
                    "concept": "I+D Desarrollo Proyecto",
                    "date": "1/1/2014",
                    "hours": "1"
                }
               ]
        :param entries:
        :return:
        """
        for entry in entries:
            self.add_entry(**entry)  # TO-DO: Not too pretty, improve this, add some error-tolerance.

    def add_entries_safe(self, entries, progress_file):
        """
        Massively adds the specified entries, just like add_entries.
        Successfully added entries are removed from the dictionary,
        and saved to progress_file (path).
        :param entries:
        :param progress_file: Path to the file in which to save remaining entries.
        :return:
        """

        total = len(entries)
        fails = 0
        added = 0

        # Remember each entry in a dict.
        i = 0
        d = OrderedDict()
        for entry in entries:
            d[i] = entry
            i += 1

        i = 0
        for entry in entries:
            try:
                self.add_entry(**entry)  # TO-DO: Not too pretty, improve this, add some error-tolerance.
                print "[SUCCESS] Registered entry: %r" % (entry)
                added += 1
            except:
                print "[FAIL] FAILED TO ADD ENTRY: %r" % (entry)
                fails += 1
            else:
                del d[i]
                # Save the current remaining dictionary to disk.
                raw = json.dumps({"entries": d.values()})
                f = file(progress_file, "w")
                f.write(raw)
                f.close()
            i += 1
            print "[PROGRESS]: %d out of %d. Errors: %d" % (added, total, fails)

    def remove_all_existing(self):
        """
        Removes every existing entry.
        :return:
        """
        driver = self.driver

        # This is mainly to support this function in PhantomJS (which doesn't support confirms)
        driver.execute_script("window.confirm = function(msg) { return true; }")

        # Display every single entry in one page.
        driver.execute_script("gReport.search('SEARCH', 1000000)")

        self._wait_for_not_visible("apexir_LOADER")

        # Mark them all for deletion.
        driver.execute_script("""$("input[type=checkbox]").attr("checked", "checked")""")

        self._wait_for_element_id("B24879923011698259")
        driver.find_element_by_id("B24879923011698259").click()

        # self._close_alert_and_get_its_text()

        self.wait_for_home()