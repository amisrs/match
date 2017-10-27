from bs4 import BeautifulSoup
import textract
import requests

import json
import re
import os
import glob

uni_name = "University of New South Wales"
base_url = "https://www.business.unsw.edu.au"
base_file_url = "https://www.business.unsw.edu.au/Programs-Courses-Site/Courseoutlines/"
save_directory = "/unsw"

text = []

urls = [
    "https://www.business.unsw.edu.au/degrees-courses/course-outlines/undergraduate"
]

for url in urls:
    response = requests.get(url)

    pdf_list = []
    #print response.text
    uni_soup = BeautifulSoup(response.content, "html5lib")

    # The html response is messed up, there's a random /ul that stuffs up the parser
    # have to rely on hardcoding

    div = uni_soup.find("div", attrs={"class":"col-lg-15 col-lg-offset-1 p-t-lg"})

    downloads = div.find_all("ul", class_="a-l__downloads")

    for download in downloads:
        a_elements = download.find_all("a")
        for a in a_elements:
            pdf_url = base_url+a.get("href")

            a_regex = re.search("([A-Z]{4}\d{4}) (.*)",a.string)
            course_code = a_regex.group(1)
            course_title = a_regex.group(2)

            pdf = requests.get(pdf_url).content
            filename = pdf_url.rsplit("/", 1)[-1]

            link_obj = {
                "university": uni_name,
                "url": base_file_url + filename,
                "course_code": course_code,
                "course_title": course_title,
                "text": ""
            }
            text.append(link_obj)

            print "Downloading " + pdf_url

            with open(os.getcwd()+"/"+save_directory+"/"+filename, "wb+") as f:
                f.write(pdf)


    pdfs = glob.glob(os.getcwd()+save_directory+"/"+"*.pdf")

    for pdf in pdfs:
        try:
            pdf_text = textract.process(pdf)
        except Exception as e:
            continue

        filename = pdf.rsplit("/", 1)[-1]
        for link_obj in text:
            if link_obj["url"] == base_file_url + filename:
                link_obj["text"] = pdf_text

with open("unsw.json", "w") as outfile:
  json.dump(text, outfile)
