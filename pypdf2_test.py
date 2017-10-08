import glob
import os

import textract

save_directory = "/auckland"

pdfs = glob.glob(os.getcwd()+save_directory+"/"+"*.pdf")

for pdf in pdfs:
    pdf_text = textract.process(pdf)
    print pdf_text
