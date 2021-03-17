#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  8 00:25:21 2021

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
driver.get("https://zoskinhealth.com/zo-near-you")


search_box = driver.find_element_by_class_name("stockist-search-field")
button_go = driver.find_element_by_class_name("stockist-feature-bg-color")

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
                    data = veri.find_element_by_class_name(tür)
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
        driver.execute_script('document.getElementByClassName("stockist-feature-bg-color").click()')
        sleep(25)
        storelist = driver.find_element_by_class_name("stockist-result-list")
        storelist = storelist.find_elements_by_class_name("stockist-result stockist-list-result")
        for i in range(len(storelist)):
            #Title, Address, Phone
            title = dene(storelist[i], "stockist-result-name stockist-feature-color")
            address = dene(storelist[i], "stockist-result-address")
            phone = dene(storelist[i], "stockist-result-details")
            ws.append([title, address, phone, city])
        search_box.clear()
    
    wb.save("res.xlsx")
    driver.quit()
