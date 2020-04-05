from selenium import webdriver
from bs4 import BeautifulSoup
import csv
from csv import writer
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException        
from time import sleep


driver = webdriver.Chrome(executable_path="C:\Program Files (x86)\Google\Chrome\chromedriver.exe")
driver.get("https://www.canada.ca/en/health-canada/services/drugs-health-products/disinfectants/covid-19/hand-sanitizer.html#tbl1")
wait = WebDriverWait(driver, 5)

element = wait.until(EC.element_to_be_clickable((By.ID, 'tbl1_filter')))
element = Select(driver.find_element_by_xpath('//div[@id="tbl1_length"]//select[@name="tbl1_length"]'))
element.select_by_value('100')

xpathNext = "/html//a[@id='tbl1_next']"

with open('output.csv', 'w', encoding = "utf16", newline = '') as csv_file:
        csv_writer = writer(csv_file)
        zaglavlje = ["Drug identification number (DIN) or natural product number (NPN)", "Product name", "Company",
                     "Active ingredient(s)", "Product form"]
        csv_writer.writerow(zaglavlje)
        
        while True:
            #skrap
            soup = BeautifulSoup(driver.page_source,'html.parser')
            a = soup.find("tbody").find_all("tr")
            
            for br in range (0, len(a)):
                red = []
                for i in a[br]:
                    if (i != "\n"):
                        red.append(i.get_text())
            #skrap
                csv_writer.writerow(red)
            try:
                driver.find_element_by_xpath(xpathNext).click()
            except ElementNotInteractableException:
                break
        
        driver.quit()
