# This just explodes the csv format we had the training data into directory structure

import csv
import glob
import os
import shutil

directories = [os.getcwd()+'/outline_sentences/textbooks',
               os.getcwd()+'/outline_sentences/contact_hours',
               os.getcwd()+'/outline_sentences/assessments',
               os.getcwd()+'/outline_sentences/course_outcomes',
               os.getcwd()+'/outline_sentences/course_content']

for directory in directories:
    try:
        shutil.rmtree(directory)
    except Exception as e:
        print 'ok'
    os.makedirs(directory)

with open('/media/sf_share/training_sentences.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile)
    sentence_list = list(reader)

    print sentence_list

categories = []
for sentence in sentence_list:
    if sentence[4] == '' and sentence[3] == '':
        continue


    if sentence[3] not in categories:
        categories.append(sentence[3])
        print "added category " + sentence[3]

    category_directory = ""
    if sentence[3] == 'Textbook':
        category_directory = os.getcwd()+"/outline_sentences/textbooks/"
    elif sentence[3] == 'Contact Hours':
        category_directory = os.getcwd()+"/outline_sentences/contact_hours/"
    elif sentence[3] == 'Assessments':
        category_directory = os.getcwd()+"/outline_sentences/assessments/"
    elif sentence[3] == 'Course Outcomes':
        category_directory = os.getcwd()+"/outline_sentences/course_outcomes/"
    elif sentence[3] == 'Course Content':
        category_directory = os.getcwd()+"/outline_sentences/course_content/"

    existing_files = glob.glob(category_directory+"*")
    print "There are " + str(len(existing_files)) + "files in " + category_directory

    new_file = open(category_directory+str(len(existing_files)+1)+"test", 'wb+')
    new_file.write(sentence[4])
    new_file.flush()
    new_file.close()
