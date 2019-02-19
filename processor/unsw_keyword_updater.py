# This script just reruns the keyword cleaner on current entries in the database
# I didn't want to have to rerun the whole process again when I was tweaking the keywords

import MySQLdb
from keyword_cleaner import keyword_cleaner

with open('mysqlp.txt', 'r') as mysqlp_file:
    mysqlp = mysqlp_file.read().split('\n')[0]
db = MySQLdb.connect(host="", user="", passwd=, db="") # don't laugh at me i left credentials in the commit

cursor = db.cursor()

query = "SELECT keywords, id FROM course_scrape WHERE university = 'University of New South Wales' and keywords != ''"
cursor.execute(query)

results = cursor.fetchall()

for keywords, course_id in results:

    print "Keywords:"
    keywords = keywords.replace("\"", "")
    keywords = keywords.split(", ")
    print keywords


    kc = keyword_cleaner()
    cleaned_keywords = kc.clean_keywords(keywords)

    ck_string = ""
    for k in cleaned_keywords:
        ck_string += "\""+k+"\", "

    update_query = "UPDATE course_scrape SET keywords = \'%s\' WHERE id = %d" % (ck_string, course_id)
    print update_query
    update_cursor = db.cursor()
    update_cursor.execute(update_query)
    update_cursor.close()
    db.commit()
