# -*- coding: utf-8 -*-
u"""
Copyright 2015 Telefónica Investigación y Desarrollo, S.A.U.
This file is part of Toolium.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from toolium.driver_wrapper import DriverWrappersPool
from toolium.pageobjects.common_object import CommonObject
from toolium.visual_test import VisualTest


class PageElement(CommonObject):
    """Class to represent a web or a mobile page element

    :type locator: (selenium.webdriver.common.by.By or appium.webdriver.common.mobileby.MobileBy, str)
    :type parent: selenium.webdriver.remote.webelement.WebElement or appium.webdriver.webelement.WebElement
                  or toolium.pageelements.PageElement
                  or (selenium.webdriver.common.by.By or appium.webdriver.common.mobileby.MobileBy, str)
    :type driver_wrapper: toolium.driver_wrapper.DriverWrapper
    """

    def __init__(self, by, value, parent=None):
        """Initialize the PageElement object with the given locator components.

        If parent is not None, find_element will be performed over it, instead of
        using the driver's method, so it can find nested elements.

        :param by: locator type
        :param value: locator value
        :param parent: parent element (WebElement, PageElement or locator tuple)
        """
        self.locator = (by, value)  #: tuple with locator type and locator value
        self.parent = parent  #: element from which to find actual elements
        self.driver_wrapper = DriverWrappersPool.get_default_wrapper()  #: driver wrapper instance
        self._web_element = None

    def reset_object(self):
        """Initialize web element object"""
        self._web_element = None

    @property
    def web_element(self):
        """Find WebElement using element locator

        :returns: web element object
        :rtype: selenium.webdriver.remote.webelement.WebElement or appium.webdriver.webelement.WebElement
        """
        if not self._web_element:
            if self.parent:
                self._web_element = self.utils.get_web_element(self.parent).find_element(*self.locator)
            else:
                self._web_element = self.driver.find_element(*self.locator)
        return self._web_element

    def scroll_element_into_view(self):
        """Scroll element into view

        :returns: page element instance
        """
        y = self.web_element.location['y']
        self.driver.execute_script('window.scrollTo(0, {0})'.format(y))
        return self

    def wait_until_visible(self, timeout=10):
        """Search element and wait until it is visible

        :param timeout: max time to wait
        :returns: page element instance
        """
        self._web_element = self.utils.wait_until_element_visible(self.locator, timeout)
        return self

    def wait_until_not_visible(self, timeout=10):
        """Search element and wait until it is not visible

        :param timeout: max time to wait
        :returns: page element instance
        """
        self._web_element = self.utils.wait_until_element_not_visible(self.locator, timeout)
        return self

    def assert_screenshot(self, filename, threshold=0, exclude_elements=[], force=False):
        """Assert that a screenshot of the element is the same as a screenshot on disk, within a given threshold.

        :param filename: the filename for the screenshot, which will be appended with ``.png``
        :param threshold: percentage threshold for triggering a test failure (value between 0 and 1)
        :param exclude_elements: list of WebElements, PageElements or element locators as a tuple (locator_type,
                                 locator_value) that must be excluded from the assertion
        :param force: if True, the screenshot is compared even if visual testing is disabled by configuration
        """
        VisualTest(self.driver_wrapper, force).assert_screenshot(self.web_element, filename, self.__class__.__name__,
                                                                 threshold, exclude_elements)

    def get_attribute(self, name):
        """Get the given attribute or property of the element

        :param name: name of the attribute/property to retrieve
        :returns: attribute value
        """
        return self.web_element.get_attribute(name)
