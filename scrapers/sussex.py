from bs4 import BeautifulSoup
import requests

import json
import re

uni_name = "University of Sussex"
base_url = "http://www.sussex.ac.uk"
text = []

urls = [
    "http://www.sussex.ac.uk/study/international-students/visiting-exchange-erasmus-students/modules/modules/213",
    "http://www.sussex.ac.uk/study/international-students/visiting-exchange-erasmus-students/modules/modules/3515"
]

for url in urls:
    response = requests.get(url)



    links = []
    #print response.text
    uni_soup = BeautifulSoup(response.content, "html.parser")

    # The html response is messed up, there's a random /ul that stuffs up the parser
    # have to rely on hardcoding

    uls = uni_soup.find_all("ul")

    # cool ul = the list of courses, not ul of links. I got these by manually counting...
    cool_uls = []
    cool_uls.append(uls[20])
    cool_uls.append(uls[21])
    cool_uls.append(uls[22])
    cool_uls.append(uls[23])

    for cool_ul in cool_uls:
        print cool_ul
        lis = cool_ul.find_all("li")

        for li in lis:
            #print li
            links.append(li.find("a").get("href"))
            print li.find("a").get("href")

    #links_element = div.find_all("a")

    #print div
    #print div.contents

    for link in links:
      print "Pulling " + base_url + link
      response = requests.get(base_url + link)

      uni_soup = BeautifulSoup(response.content, "html.parser")
      div = uni_soup.find("div", class_= "small-12 large-9 large-push-3 columns wysiwyg content-region")

      h2 = div.find("h2")
      course_title = h2.text

      module_p = div.find("p")
      m = re.search("Module code:\s(.*?)\s", module_p.text)
      course_code = m.group(1)

      link_obj = {
        "university": uni_name,
        "url": base_url + link,
        "course_code": course_code,
        "course_title": course_title,
        "text": str(div)
      }
      text.append(link_obj)

with open("sussex.json", "w") as outfile:
  json.dump(text, outfile)
