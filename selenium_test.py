from selenium import webdriver, common
from bs4 import BeautifulSoup

driver = webdriver.Firefox()
driver.get("http://www.courses.business.auckland.ac.nz/SubjectListing/ACCTG/")
result = driver.execute_script("document.title")

pdf_list = []
page_sources = []

page_sources.append(driver.page_source)

next_button_has_href = True;
#whiule next button is enabled AKA has a href
#while next_button_has_href:
next_button = driver.find_element_by_id("ctl00_ContentMain_lbtnNext")

while next_button_has_href:

    next_button.click()
    try:
        next_button = driver.find_element_by_id("ctl00_ContentMain_lbtnNext")
    except common.exceptions.NoSuchElementException as e:
        print "end"
        next_button_has_href = False
    page_sources.append(driver.page_source)

print len(page_sources)


for page_source in page_sources:

    page_soup = BeautifulSoup(page_source, "html.parser")

    aspnetForm = page_soup.find("form", attrs={"name": "aspnetForm"})

    link_list = aspnetForm.find_all("a")

    for link in link_list:
        href = link.get("href")
        if("pdf" in str(href)):
            pdf_list.append(str(href))
            print str(href)
    #print aspnetForm
