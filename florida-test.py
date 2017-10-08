import glob
import json
import os
import textract

uni_name = "University of Florida"
base_url = "http://warrington.ufl.edu"
save_directory = "/florida"

text = []

pdfs = glob.glob(os.getcwd()+save_directory+"/"+"*.pdf")

for pdf in pdfs:
    print "Processing: " + pdf
    try:
        pdf_text = textract.process(pdf)
    except Exception as e:
        print "Exception textracting " + pdf
        continue

    filename = pdf.rsplit("/", 1)[-1]

    link_obj = {
        "university": uni_name,
        "url": base_url + filename,
        "text": pdf_text
    }

    text.append(link_obj)

with open("florida.json", "w") as outfile:
  json.dump(text, outfile)
