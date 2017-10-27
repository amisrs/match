from bs4 import BeautifulSoup
from selenium import webdriver, common

import textract

import glob
import os
import requests

import json
import re

driver = webdriver.Firefox()

uni_name = "University of Auckland"
base_url = "http://www.courses.business.auckland.ac.nz/"
pdf_base_url = "http://www.courses.business.auckland.ac.nz/CoursePdfs/"

save_directory = "/auckland"
text = []
pdf_list = []

subject_list_url = "http://www.courses.business.auckland.ac.nz/BrowseBySubject.aspx"

subject_list_response = requests.get(subject_list_url)
subject_list_soup = BeautifulSoup(subject_list_response.content, "html.parser")


table = subject_list_soup.find("table")

filename_map = {}

print table

links = []

for a in table.find_all("a"):
    links.append(a.get("href"))
    print a.get("href")

for link in links:


  print "Pulling " + base_url + link
  response = requests.get(base_url + link)

  driver.get(base_url + link)
  result = driver.execute_script("document.title")

  page_sources = []

  page_sources.append(driver.page_source)

  next_button_has_href = True;
  #whiule next button is enabled AKA has a href
  #while next_button_has_href:
  try:
      next_button = driver.find_element_by_id("ctl00_ContentMain_lbtnNext")
  except common.exceptions.NoSuchElementException as e:
      print "end"
      next_button_has_href = False

  while next_button_has_href:

      next_button.click()
      try:
          next_button = driver.find_element_by_id("ctl00_ContentMain_lbtnNext")
      except common.exceptions.NoSuchElementException as e:
          print "end"
          next_button_has_href = False
      page_sources.append(driver.page_source)

  print len(page_sources)
  # driver.quit()

  for page_source in page_sources:

      page_soup = BeautifulSoup(page_source, "html.parser")


      aspnetForm = page_soup.find("form", attrs={"name": "aspnetForm"})
      if aspnetForm is not None:
        print "Found aspnetForm!"
      else:
        print "Weird, didn't find aspnetForm..."
        continue
      link_list = aspnetForm.find_all("a")

      for link in link_list:
          href = link.get("href")
          if("pdf" in str(href)):
              title_text = link.get("title")
              m = re.search("PDF download for:(.*)", title_text)
              course_title = m.group(1)

              m = re.search("(([^\/]*).pdf)",str(href))
              course_code = m.group(2)
              filename = m.group(1)

              filename_map[filename] = (course_code, course_title)

              pdf_list.append(str(href))
              print str(href)
      #print aspnetForm


print pdf_list

for pdf_url in pdf_list:
    pdf = requests.get(pdf_url).content
    filename = pdf_url.rsplit("/", 1)[-1]

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
        "url": pdf_base_url + filename,
        "course_code": filename_map[filename][0],
        "course_title": filename_map[filename][1],
        "text": pdf_text
    }

    text.append(link_obj)

with open("auckland.json", "w") as outfile:
  json.dump(text, outfile)
