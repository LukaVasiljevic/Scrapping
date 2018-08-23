from bs4 import BeautifulSoup
import requests
from csv import writer

stranica = requests.get("https://soundcloud.com/charts/top")
'''
#test
Status kod:
200, ili kad pocinje na 2- DOBRO, stranica ucitana
5, 4 pocetak - GRESKA, stranica nije ucitana
'''
#print(stranica.status_code)

soup = BeautifulSoup(stranica.content, 'html.parser')

'''
izgled skinute html stranice
print(soup.prettify())
'''
with open('top50.csv','w', encoding="utf8", newline='') as csv_file:
    csv_writer = writer(csv_file)
    zaglavlje = ["Broj na listi", "Naziv Pesme", "Izvodjac"]
    csv_writer.writerow(zaglavlje)


    lista= soup.body.find(class_="sounds")
    pesma = lista.find_all('a')
    lista = [pes.get_text().replace('/n','') for pes in pesma]
    pe = lista[::2]
    iz = lista[1::2]
    for i in range(len(pe)):
        csv_writer.writerow(['#'+ str(i+1), pe[i], iz[i]])

