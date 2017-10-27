from bs4 import BeautifulSoup
import requests

import json
import re

uni_name = "Babson College"
base_url = "https://fusionmx.babson.edu/CourseListing/"
text = []

urls = [
    "https://fusionmx.babson.edu/CourseListing/index.cfm?fuseaction=CourseListing.DisplayCourseListing&blnShowHeader=true&program=Undergraduate&semester=All&sort_by=course_description&btnSubmit=Display+Courses"
]

for url in urls:
    response = requests.get(url)



    links = []
    #print response.text
    uni_soup = BeautifulSoup(response.content, "html.parser")

    # The html response is messed up, there's a random /ul that stuffs up the parser
    # have to rely on hardcoding

    table = uni_soup.find("table", attrs={"border":"0", "cellspacing": "0", "width": "950"})
    #table_rows = table.find_all("tr", class_=lambda x: x != "tableheader")
    #table_rows = [] # one row is generally one course, and it has multiple classes
    existing_children = []

    for child in table.children:
        if "tableheader" in str(child):
            continue
        #print child
        #print len(str(child))
        if str(child) not in '\n' and str(child) not in existing_children:
            #print child
            existing_children.append(str(child))

            child_link = child.find("a").get("href")
            link_match = re.search("openWindow\('(.*?)'",child_link)
            link = link_match.group(1)

            row_obj = {
                "link": base_url + link,
                "text": child
            }
            text.append(row_obj)
            print row_obj["link"]
            print "================================================"

    # for row in table_rows:
    #     row_desc = row.find("td", attrs={"colspan": "7"})
    #     print row_desc
    #     link_obj = {
    #         "university": uni_name,
    #         "url": base_url + link,
    #         "text": str(div)
    #     }
    #     text.append(link_obj)

    # print table_rows

    #print len(table_rows)
    #links_element = div.find_all("a")

    #print div
    #print div.contents



with open("babson.json", "w") as outfile:
    json.dump(str(text), outfile)
