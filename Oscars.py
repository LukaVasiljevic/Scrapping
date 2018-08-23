from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
import csv
from csv import writer

start = time.time()

driver = webdriver.Chrome(executable_path="C:\Program Files (x86)\Google\Chrome\chromedriver.exe")
driver.get("http://awardsdatabase.oscars.org/search")
wait = WebDriverWait(driver, 10)
element = wait.until(EC.element_to_be_clickable((By.ID, 'btnbasicsearch')))
#initializing
category = driver.find_element_by_xpath('//*[@id="basicsearch"]/div/div[1]/div[2]/div/span/div/button')
lma = driver.find_element_by_xpath('//*[@id="basicsearch"]/div/div[1]/div[2]/div/span/div/ul/li[4]/a/label/input')
lfa = driver.find_element_by_xpath('//*[@id="basicsearch"]/div/div[1]/div[2]/div/span/div/ul/li[6]/a/label/input')
from_y = driver.find_element_by_xpath('//*[@id="basicsearch"]/div/div[2]/div[2]/div/div[1]/span/div/button')
to_y = driver.find_element_by_xpath('//*[@id="basicsearch"]/div/div[2]/div[2]/div/div[2]/span/div/button')
fy = driver.find_element_by_xpath('//*[@id="basicsearch"]/div/div[2]/div[2]/div/div[1]/span/div/ul/li[92]/a/label/input')
ty = driver.find_element_by_xpath('//*[@id="basicsearch"]/div/div[2]/div[2]/div/div[2]/span/div/ul/li[3]/a/label/input')
wo = driver.find_element_by_xpath('//*[@id="BasicSearchView_IsWinnersOnly"]')
submit = driver.find_element_by_xpath('//*[@id="btnbasicsearch"]')
#opening categories and selecting ones I want
category.click()
element = wait.until(EC.visibility_of(lma))
lma.click()
lfa.click()

#opening from(year)
from_y.click()
element = wait.until(EC.visibility_of(fy))
fy.click()

#opening to(year)
to_y.click()
element = wait.until(EC.visibility_of(ty))
ty.click()

#winners only
wo.click()
submit.click()

#explicit wait(to get results)
element = wait.until(EC.url_matches('http://awardsdatabase.oscars.org/search/results'))

#taking html to scrap
soup = BeautifulSoup(driver.page_source,'html.parser')   
driver.close()
#closing webdriver
#driver.close()

#writing response to a file
file = open("Oscars.txt","w") 
file.write(soup.prettify())
file.close()
#print(soup.prettify())  

#SCRAPING WITH SOUP

#getting years scrapped
yrs = []
years = soup.find_all(class_="result-group-header")
for i in range(len(years)):
    yrs.append(years[i].find('a').get_text())

#getting actors & actresses
actr = []
actrs = []
subgroup = soup.find_all(class_="result-subgroup subgroup-awardcategory-chron")
g=0
for i in range(len(subgroup)):
    if (subgroup[i].find(class_="result-subgroup-header").find('a').get_text() == 'ACTOR' or subgroup[i].find(class_="result-subgroup-header").find('a').get_text() == 'ACTOR IN A LEADING ROLE'):
        actr.append(subgroup[i].find(class_="awards-result-nominationstatement").get_text().replace('\n',''))
    elif (subgroup[i].find(class_="result-subgroup-header").find('a').get_text() == 'ACTRESS' or subgroup[i].find(class_="result-subgroup-header").find('a').get_text() == 'ACTRESS IN A LEADING ROLE'):
        actrs.append(subgroup[i].find(class_="awards-result-nominationstatement").get_text().replace('\n',''))

#making csv file of data we scraped
with open('Oscars.csv','w', newline='') as csv_file:
    csv_writer = writer(csv_file, delimiter=';')
    zaglavlje = ["Godina osvajanja", "Glumac", "Glumica"]
    csv_writer.writerow(zaglavlje)
    for i in range(len(actr)):
        csv_writer.writerow([yrs[i], actr[i], actrs[i]])

end = time.time()
print('Script running time: {} seconds'.format(round(end-start,3)))
