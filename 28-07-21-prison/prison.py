#Rafet Efe Gazanfer 28.07 22.21

from openpyxl import load_workbook
from base import init_driver

def obtain(driver):
    facility_name = driver.find_element_by_tag_name("title").get_attribute("text")
    address = driver.find_element_by_class_name("adr").text
    email = driver.find_element_by_class_name("email").text
    phone = driver.find_element_by_class_name("tel").text.strip("Phone: ")
    fax = driver.find_element_by_id("fax").text
    gender = driver.find_element_by_id("pop_gender").text
    inmates = driver.find_element_by_id("pop_count").text
    district = driver.find_element_by_id("facl_facts").find_elements_by_tag_name("td")[7].text
    county = driver.find_element_by_id("county").text
    region = driver.find_element_by_id("region").text

    ws.append([facility_name, address, email, phone, fax, gender, inmates, district, county, region])

def get_links(driver):

    driver.get("https://www.bop.gov/locations/list.jsp")
    hrefs = driver.find_element_by_id("facil_list_cont").find_elements_by_tag_name("a")
    mem = []
    for href in hrefs:
        x = href.get_attribute("href")
        mem.append(x)
        print("Href: {}", x)
    return mem

    # # # #
    # All
    # https://www.bop.gov/locations/list.jsp
    # # # #  
    # FPC Alderson
    # https://www.bop.gov/locations/institutions/ald/
    # # # #

if __name__ == '__main__':

    wb = load_workbook("empty.xlsx")
    ws = wb.active
    ws.append(["Facility Name", "Address", "Email", "Phone", "Fax", "Gender", "Inmates", "Dıstrict", "County", "Region"])
    
    driver = init_driver()
    
    link_list = get_links(driver)

    for link in link_list:
        driver.get(link)
        print("Obtaining: {}", link)
        obtain(driver)

    driver.quit()    
    wb.save("res.xlsx")
