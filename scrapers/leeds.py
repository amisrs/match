from bs4 import BeautifulSoup
import requests

import json
import re

uni_name = "University of Leeds"
base_url = "http://webprod3.leeds.ac.uk/catalogue/"
text = []

urls = [
    "http://webprod3.leeds.ac.uk/catalogue/modulesearch.asp?L=UG&Y=201718&F=M&E=all&N=all&S=+&A=any"
]

for url in urls:
    response = requests.get(url)

    with open("test-leeds.html", "w+") as out:
        out.write(response.content)

    links = []
    #print response.text
    uni_soup = BeautifulSoup(response.content, "html5lib")

    # The html response is messed up, there's a random /ul that stuffs up the parser
    # have to rely on hardcoding

    div = uni_soup.find("div", attrs={"id":"module-programmes"})
    print div

    tables = div.find_all("table", attrs={"width": "100%"})

    for table in tables:
        print table
        a_elements = table.find_all("a")
        for a in a_elements:
            if "LUBS" in a.get("href") or "COMP" in a.get("href"):
                links.append(a.get("href"))



    for link in links:
      print "Pulling " + base_url + link
      response = requests.get(base_url + link)

      uni_soup = BeautifulSoup(response.content, "html.parser")
      div = uni_soup.find("div", id="module-programmes")

      info = div.find("h2")
      m = re.search("([a-zA-Z]{4}[0-9]{4})\s*(.*)", info.text)
      course_code = m.group(1)
      course_title = m.group(2)

      link_obj = {
        "university": uni_name,
        "url": base_url + link,
        "course_code": course_code,
        "course_title": course_title,
        "text": str(div)
      }
      text.append(link_obj)

with open("leeds.json", "w") as outfile:
  json.dump(text, outfile)
