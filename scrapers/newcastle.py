from bs4 import BeautifulSoup
import requests

import json
import re


url = "https://www.ncl.ac.uk/module-catalogue/modules.php"
base_url = "https://www.ncl.ac.uk/module-catalogue/"

payload = {
    'title': '',
    'school': 'D-NUBS',
    'course': '',
    'report': 'SEARCH'
}

headers = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate, br',
    'Accept-Language':'en-GB,en-US;q=0.8,en;q=0.6',
    'Cache-Control':'no-cache',
    'Connection':'keep-alive',
    'Content-Length':'42',
    'Content-Type':'application/x-www-form-urlencoded',
    'Cookie':'_gat_crossTracking=1; _gat=1; _gat_UA-41910807-7=1; _bizo_bzid=390041b1-c2af-44c9-9185-4ecb5aa350b8; _bizo_cksm=5F6B974E8D1BC93F; _bizo_np_stats=14%3D228%2C; _ga=GA1.3.2043572719.1504934864; _gid=GA1.3.557024618.1504934864',
    'Host':'www.ncl.ac.uk',
    'Origin':'https://www.ncl.ac.uk',
    'Pragma':'no-cache',
    'Referer':'https://www.ncl.ac.uk/module-catalogue/modules.php',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
}

response = requests.request("POST", url, data=payload, headers=headers)

uni_soup = BeautifulSoup(response.text, 'html.parser')

links = []

div = uni_soup.find_all("div", class_="page")
links_element = div[0].find_all("a")
for element in links_element:
    links.append(element.get("href"))

with open("newcastleLinks.json", "w") as outfile:
    json.dump(links, outfile)

for link in links:
    # Go to stored url
    response = requests.get(base_url + link)
    # Store entire html markup
    uni_soup = BeautifulSoup(response.content, "html.parser")
    div = uni_soup.find_all("div", class_="report")
    #text.append(div[0])
    with open("newcastleText.json", "a") as outfile:
        json.dump(str(div[0]), outfile)