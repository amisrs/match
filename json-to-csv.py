import json
import csv
import sys
import MySQLdb


with open('processor/mysqlp.txt', 'r') as mysqlp_file:
    mysqlp = mysqlp_file.read().split('\n')[0]

db = MySQLdb.connect(host="104.236.9.215", user="scraper", passwd=mysqlp, db="scrape")

f = open(sys.argv[1])
data = json.load(f)

cursor = db.cursor()

for item in data:
  sql = """INSERT INTO course_scrape (url, text, university) VALUES("%s", "%s", "%s")""" % \
    (item["url"].encode("utf-8", "ignore"), item["text"].encode("utf-8", "ignore").replace("'", "''").replace("\"", "\\\""), item["university"].encode("utf-8", "ignore"))
  print sql
  cursor.execute(sql)
  db.commit()


cursor.close()
f.close()
