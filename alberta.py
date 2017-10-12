from bs4 import BeautifulSoup
import requests
import glob

import json
import re
import os


uni_name = "University of Alberta"
base_url = "https://catalogue.ualberta.ca"
text = []
save_directory = "/alberta"

urls = [
    "https://catalogue.ualberta.ca/Course/Faculty?facultyCode=BC"
]

filename_url_map = {}
filename_info_map = {}

for url in urls:
    response = requests.get(url)

    subject_links = []
    #print response.text
    uni_soup = BeautifulSoup(response.content, "html5lib")

    # The html response is messed up, there's a random /ul that stuffs up the parser
    # have to rely on hardcoding

    div = uni_soup.find("table", class_="pure-table pure-table-striped")
    print div

    a_elements = div.find_all("a")
    for a in a_elements:
        subject_links.append(a.get("href"))

    # for content in accordion_contents:

    print subject_links
    for link in subject_links:
        print "Pulling " + base_url + link
        response = requests.get(base_url + link)

        page_soup = BeautifulSoup(response.content, "html.parser")


        more_buttons = page_soup.find_all("a", class_="pure-button pure-button-primary claptrap-more-button")

        for more_button in more_buttons:
            parent = more_button.parent
            print type(parent)
            spans = parent.find_all("span")
            course_title = ""
            course_number = ""
            for span in spans:
                print '\n'
                print span
                print span.get('class')
                if span.get('class')[0] == "claptrap-course-title":
                    course_title = span.text
                    print "Found course title: " + course_title
                elif span.get('class')[0] == "claptrap-course-number":
                    course_number = span.text
                    print "Found course number: " + course_number

            more_link = more_button.get("href").replace("Details", "PastSyllabi")
            print "    Then pulling " + more_link

            syllabus_list = []
            syllabus_response = requests.get(base_url + more_link)

            syllabus_soup = BeautifulSoup(syllabus_response.content, "html.parser")
            div_container = syllabus_soup.find("div", class_="content-container container")


            try:
                p = div_container.find("p")

                syllabus_list.append(p.find("a").get("href"))
                pdf = requests.get(base_url+p.find("a").get("href")).content
                filename = p.find("a").get("href").rsplit("filename=", 1)[-1]
                filename_url_map[filename] = base_url+p.find("a").get("href")
                filename_info_map[filename] = { "course_title": course_title, "course_number": course_number }

                with open(os.getcwd()+"/"+save_directory+"/"+filename, "wb+") as f:
                    f.write(pdf)
            except Exception as e:
                continue


pdfs = glob.glob(os.getcwd()+save_directory+"/*.pdf")
for pdf in pdfs:
    try:
        pdf_text = textract.procses(pdf)
    except Exception as e:
        continue
    filename = pdf.rsplit("/", 1)[-1]

    link_obj = {
        "university": uni_name,
        "url": filename_url_map[filename],
        "course_code": course_number,
        "course_title": course_title,
        "text": pdf_text
    }
    text.append(link_obj)

with open("alberta.json", "w") as outfile:
  json.dump(text, outfile)
