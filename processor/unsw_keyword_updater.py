import MySQLdb
from keyword_cleaner import keyword_cleaner

with open('mysqlp.txt', 'r') as mysqlp_file:
    mysqlp = mysqlp_file.read().split('\n')[0]
db = MySQLdb.connect(host="104.236.9.215", user="scraper", passwd=mysqlp, db="scrape")
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
