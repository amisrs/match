import re
import MySQLdb
with open('mysqlp.txt', 'r') as mysqlp_file:
    mysqlp = mysqlp_file.read().split('\n')[0]
db = MySQLdb.connect(host="104.236.9.215", user="scraper", passwd=mysqlp, db="scrape")
cursor = db.cursor()
cursor.execute("""SELECT text, id FROM course_scrape WHERE emails IS NULL""")
update_tuples = []
for result in cursor:
    #process
    print len(result)
    print result
    email_string = ""
    emails = re.findall(".*?([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+).*?",list(result)[0])
    for email in emails:
        email_string += str(email) + ", "
    print """UPDATE course_scrape SET emails = \"{0}\" WHERE id = {1}""".format(email_string, list(result)[1])
    # cursor.execute("""UPDATE course_scrape SET emails = \"{0}\" WHERE id = {1}""".format(email_string, list(result)[1]))
    update_tuples.append((email_string, list(result)[1]))
for email_list in update_tuples:
    cursor.execute("UPDATE course_scrape SET emails = \"{0}\" WHERE id = {1}".format( email_list[0], email_list[1]))
db.commit()
cursor.close()
                                            
