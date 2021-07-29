

def init_driver():
	from selenium import webdriver
	from selenium.webdriver.firefox.options import Options
	from selenium.common.exceptions import NoSuchElementException,StaleElementReferenceException
	
	#from pandas import read_csv
	#from time import sleep
	from openpyxl import load_workbook
	
	options = Options()
	options.headless = False
	return webdriver.Firefox(options=options, executable_path=r"geckodriver")