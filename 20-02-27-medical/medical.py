#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 19:30:07 2021
@author: Rafet Efe Gazanfer
"""

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
from openpyxl import load_workbook
from time import sleep


#                               Launching Excel
wb = load_workbook("Template-To-Enter-Data.xlsx")
ws = wb.active

#                               Launching Firefox
# a note about executable_path:
# example for windows: r'C:/Users/username/Desktop/geckodriver.exe'
# my system is linux, so i can call the geckodriver without adressing.
print("#Initiating webpage and browser")
options = Options()
options.headless = True
driver = webdriver.Firefox(options=options, executable_path=r'geckodriver')

#   Visit page
driver.get("-")

#                                Page Loading
refresh = 0
flag = True
while(flag):
    counter = 0
    driver.execute_script("window.scrollBy(0,document.body.scrollHeight)") 
    sleep(2)
    load_status = driver.find_element_by_id("wpkunaki_load").get_attribute("style")
    if(load_status == 'display: none;'):
        flag = False
    print("Page number:" + str(refresh))
    while(load_status == ""):
        print("New page is loading " + str(counter) + "/50" )
        counter = counter + 1
        sleep(1)
        load_status = driver.find_element_by_id("wpkunaki_load").get_attribute("style")
        if(counter > 50):
            break
    refresh = refresh + 1



#   Capturing Table
table = driver.find_element_by_id("wpkunaki-frontend")
table = table.find_element_by_tag_name("tbody")
rows = table.find_elements_by_tag_name("tr")
for row in rows:
    
    #List of cells in each row
    cells_of_row = row.find_elements_by_tag_name("td")
    
    #First cell, (image,name,title,email,website) | INFO 1
    info1 = cells_of_row[0].find_elements_by_tag_name("span")[1].text
    
    #Adress Cell | INFO 2
    try:
        info2 = cells_of_row[1].find_element_by_tag_name("a").text
    except NoSuchElementException:
        info2 = ""
    
    #Phone Cell | INFO 3
    info3 = cells_of_row[2].text
    
    #                        Formatting of gathered data
    
    #Cell 1
    info1 = info1.split("\n")
    name_surname_title = info1[0].split(", ")
    name_surname = name_surname_title[0].split((" "))
    
    name = " ".join(name_surname[0:-1]) #Incase of multiple names
    surname = name_surname[-1] #The last name (surname)
    title = ", ".join(name_surname_title[1:]) #Incase of multiple titles
    business_name = info1[1]
    email = info1[2]
    website = info1[3]
    
    #Cell 2
    adress = info2.replace("\n", " ")
    
    #Cell 3
    #Not gona format, since there is no universel way of writing a phone number
    phone = info3
        
    #                                Data Entry
    
# =============================================================================
#     Format:
#     
#     'List', 'Title', 'First Name', 'Last Name', 'Business Name',
#     'Address', 'Address 2', 'City', 'State', 'Zip', 'Country',
#     'Phone', 'Ext', 'Specialty', 'Email', 'Website'
# =============================================================================
    
    
    new_line = ["",#List
                title, name, surname, business_name, adress, 
                "","","","","",#Adress2,City,State,Zip,Country
                phone, "","",  #Ext,Specialty
                email, website]
    
    ws.append(new_line)
    wb.save("Results.xlsx")
    
    

driver.quit()
