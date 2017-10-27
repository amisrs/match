from bs4 import BeautifulSoup
import requests

import json
import re

uni_name = "Lancaster University"
base_url = "http://www.lusi.lancaster.ac.uk"
text = []

urls = [
    "http://www.lusi.lancaster.ac.uk/CoursesHandbook/ModuleDetails/OnlineModules?yearId=000117&categoryCodeLid=000622&sortOrder=0"
]

for url in urls:
    response = requests.get(url)

    links = []
    #print response.text
    uni_soup = BeautifulSoup(response.content, "html5lib")

    # The html response is messed up, there's a random /ul that stuffs up the parser
    # have to rely on hardcoding

    div = uni_soup.find("div", attrs={"id":"accordion"})
    # print div

    # accordion_contents = div.find_all("div", attrs={"role":"tabpanel"})
    a_elements = div.find_all("a")
    for a in a_elements:

        links.append(a.get("href"))

    # for content in accordion_contents:

    print links

    for link in links:
        print "Pulling " + base_url + link
        response = requests.get(base_url + link)

        page_soup = BeautifulSoup(response.content, "html.parser")
        content = page_soup.find("div", class_="left")

        try:
            course_info = content.find("h1").text
        except Exception as e:
            continue

        m = re.search("(.*?): (.*)", course_info)
        course_code = m.group(1)
        course_title = m.group(2)

        link_obj = {
            "university": uni_name,
            "url": base_url + link,
            "course_code": course_code,
            "course_title": course_title,
            "text": str(content)
        }
        text.append(link_obj)

with open("lancaster.json", "w") as outfile:
  json.dump(text, outfile)
