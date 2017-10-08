from bs4 import BeautifulSoup
import requests

import glob
import os
import json
import re

uni_name = "University of Florida"
base_url = "http://warrington.ufl.edu"
base_file_url = "http://warrington.ufl.edu/academics/syllabi"
save_directory = "/florida"


text = []
pdf_list = []

urls = [
    "http://warrington.ufl.edu/academics/syllabi.asp",
]

for url in urls:
    response = requests.get(url)



    links = []
    #print response.text
    uni_soup = BeautifulSoup(response.content, "html.parser")

    # The html response is messed up, there's a random /ul that stuffs up the parser
    # have to rely on hardcoding

    uls = uni_soup.find_all("ul", class_="indented")

    for ul in uls:
      links_element = ul.find_all("a")
      for a in links_element:
        pdf_list.append(base_url+a.get("href"))

    print pdf_list
    #print div
    #print div.contents
    # for link in links:
    #   print "Pulling " + base_url + link
    #   response = requests.get(base_url + link)
    #
    #   uni_soup = BeautifulSoup(response.content, "html.parser")
    #   div = uni_soup.find("div", class_= "small-12 large-9 large-push-3 columns wysiwyg content-region")
    #
    #   link_obj = {
    #     "university": uni_name,
    #     "url": base_url + link,
    #     "text": str(div)
    #   }
    #   text.append(link_obj)

# with open("florida.json", "w") as outfile:
#   json.dump(text, outfile)
    for pdf_url in pdf_list:
        pdf = requests.get(pdf_url).content
        filename = pdf_url.rsplit("/", 1)[-1]

        print "Downloading " + filename + "..."
        with open(os.getcwd()+"/"+save_directory+"/"+filename, "wb+") as f:
            f.write(pdf)

        #print pdf_reader.getNumPages()
    # with open("auckland.json", "w") as outfile:
    #   json.dump(text, outfile)

    pdfs = glob.glob(os.getcwd()+save_directory+"/"+"*.pdf")

    for pdf in pdfs:
        try:
            pdf_text = textract.process(pdf)
        except Exception as e:
            continue

        filename = pdf.rsplit("/", 1)[-1]

        link_obj = {
            "university": uni_name,
            "url": base_file_url + filename,
            "text": pdf_text
        }

        text.append(link_obj)

    with open("florida.json", "w") as outfile:
      json.dump(text, outfile)
