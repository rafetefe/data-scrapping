#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  5 15:13:15 2021

@author: op
"""

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException,StaleElementReferenceException
from pandas import read_csv
from time import sleep
from openpyxl import load_workbook

#20.00
print("Gathering city names ")
cities = read_csv("vanillacities.csv")

wb = load_workbook("empty.xlsx")
ws = wb.active

print("Initiating browser")
options = Options()
options.headless = False
driver = webdriver.Firefox(options=options, executable_path=r"geckodriver")

print("Loading webpage")
driver.get("https://hydrafacial.com/find-a-provider/?utm_source=button")

search_box = driver.find_element_by_id("storemapper-zip")
button_go = driver.find_element_by_id("storemapper-go")
#21.45
print("Website loaded, after declaring : Should call 'baslat()' now.")
#Title, Address, Phone, Website

# =============================================================================
#         while((attempts < 20) and (flag == False)):
#             try:
#                 title = storelist[i].find_element_by_class_name("storemapper-title").text
#                 address = storelist[i].find_element_by_class_name("storemapper-address").text
#                 try:
#                     phone = storelist[i].find_element_by_class_name("storemapper-phone").text
#                 except(NoSuchElementException):
#                     phone = ""
#                 try:
#                     website = storelist[i].find_element_by_class_name("storemapper-url")
#                     aa = website.find_element_by_tag_name("a")
#                     bb = aa.get_property("href")
#                 except(NoSuchElementException):
#                     bb = ""
#                 flag = True
#             except(StaleElementReferenceException):
#                 attempts = attempts + 1
# =============================================================================

def dene(veri, tür):
    deneme = 0
    flag = False
    if(tür == "storemapper-url"):
        while(flag == False and deneme < 10):
            try:
                try:
                    data = veri.find_element_by_class_name(tür)
                    data = data.find_element_by_tag_name("a")
                    data = data.get_property("href")
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
                    data= data.text
                    flag = True
                    return data
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
        driver.execute_script('document.getElementById("storemapper-go").click()')
        sleep(1)
        storelist = driver.find_element_by_id("storemapper-list")
        storelist = storelist.find_elements_by_class_name("tier")
        for i in range(len(storelist)):
            title = dene(storelist[i], "storemapper-title")
            address = dene(storelist[i], "storemapper-address")
            phone = dene(storelist[i], "storemapper-phone")
            website = dene(storelist[i], "storemapper-url")
            ws.append([title, address, phone, website, city])
        search_box.clear()
    
    wb.save("res.xlsx")
    driver.quit()
