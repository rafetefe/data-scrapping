#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  7 22:32:43 2021

@author: op
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  7 18:43:45 2021

@author: op
"""

#           TODO : LIST ELEMENT SCRAPIING

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException,StaleElementReferenceException
from pandas import read_csv
from openpyxl import load_workbook
from time import sleep

#20.00
print("Gathering city names ")
cities = read_csv("../vanillacities.csv")

wb = load_workbook("../empty.xlsx")
ws = wb.active

print("Initiating browser")
options = Options()
options.headless = False
driver = webdriver.Firefox(options=options, executable_path=r"geckodriver")

print("Loading webpage")
driver.get("https://www.xeominaesthetic.com/find-a-provider/")


search_box = driver.find_element_by_id("js-search-field")
#button_go = driver.find_element_by_id("wpsl-search-btn")

def dene(veri, tür):
    deneme = 0
    flag = False
    if(tür == "strong"):
        while(flag == False and deneme < 10):
            try:
                try:
                    data = veri.find_element_by_tag_name("strong").text
                    flag = True
                    return data
                except(NoSuchElementException):
                    return ""
            except(StaleElementReferenceException):
                deneme = deneme + 1
                if deneme == 10:
                    return ""
    else:
        while(flag == False and deneme < 3):
            try:
                try:
                    data = veri.find_elements_by_tag_name(tür)
                    adr = ""
                    for item in data:
                        adr = adr + item.get_property("innerText") + " "
                    flag = True
                    return adr
                except(NoSuchElementException):
                    return ""
            except(StaleElementReferenceException):
                deneme = deneme + 1
                if deneme == 10:
                    return ""
                
def baslat():
    print("Gathering data")
    for city in cities['Full']:
        search_box.send_keys(city)
        driver.execute_script('document.getElementsByClassName("button-primary helper-svg_primary helper-aux-hover_text_primary helper-background_primary helper-border_primary helper-color_white helper-button_shape widget-form_apply helper-font_case_button").click()')
        sleep(3)
        storelist = driver.find_element_by_class_name("widget-sidebar_tiles js-sidebar-tiles hidden-mobile")
        storelist = storelist.find_elements_by_class_name("widget-tile_content helper-background_tile")
        for i in range(len(storelist)):
            title = dene(storelist[i], "strong")
            address = dene(storelist[i], "span")
            ws.append([title, address, city])
        search_box.clear()
    
    wb.save("res.xlsx")
    driver.quit()
