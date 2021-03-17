#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  7 18:43:45 2021

@author: op
"""

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
driver.get("http://vivaceexperience.com/find-physician/")


search_box = driver.find_element_by_id("wpsl-search-input")
button_go = driver.find_element_by_id("wpsl-search-btn")

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
        driver.execute_script('document.getElementById("wpsl-search-btn").click()')
        sleep(50)
        storelist = driver.find_element_by_id("wpsl-stores")
        storelist = storelist.find_elements_by_class_name("wpsl-store-location")
        for i in range(len(storelist)):
            title = dene(storelist[i], "strong")
            address = dene(storelist[i], "span")
            ws.append([title, address, city])
        search_box.clear()
    
    wb.save("resvivace.xlsx")
    driver.quit()
