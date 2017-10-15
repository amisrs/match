import compare
import MySQLdb

from itertools import combinations


with open('mysqlp.txt', 'r') as mysqlp_file:
    mysqlp = mysqlp_file.read().split('\n')[0]

db = MySQLdb.connect(host="104.236.9.215", user="scraper", passwd=mysqlp, db="scrape")


unsw_cursor = db.cursor()
unsw_query = "SELECT keywords, id FROM course_scrape WHERE university = 'University of New South Wales'"
unsw_cursor.execute(unsw_query)
unsw_keywords = unsw_cursor.fetchall()
print "unsw_keywords: " + str(len(unsw_keywords))
unsw_cursor.close()

other_cursor = db.cursor()
other_query = "SELECT keywords, id FROM course_scrape WHERE university = 'University of Auckland' and keywords != '';"#university != 'University of New South Wales' and university != 'Swansea University' and keywords != ''"
other_cursor.execute(other_query)
other_keywords = other_cursor.fetchall()
print "other_keywords: " + str(len(other_keywords))
other_cursor.close()

sim_cursor = db.cursor()
sim_query = "SELECT * from similarity;"
sim_cursor.execute(sim_query)
sims = sim_cursor.fetchall()
sim_cursor.close()

lefts = {}
for unsw_keywords, unsw_id in unsw_keywords:
    # print unsw_id
    lefts[unsw_id] = unsw_keywords

rights = {}
for other_keywords, other_id in other_keywords:
    # print other_id
    rights[other_id] = other_keywords
    # print "Sim: " + str(unsw_id) + " vs " + str(other_id)

# print lefts
# print rights
#
for left in lefts:
    for right in rights:
        print
        print "Sim: " + str(left) + " vs " + str(right)
        print rights[right]
        sim = compare.compare_keywords(lefts[left], rights[right])

        insert_query = "INSERT INTO similarity (course1, course2, similarity) VALUES ({0}, {1}, {2}) ON DUPLICATE KEY UPDATE similarity = {2};".format(left,right,compare.simdict_avg(sim))
        insert_cursor = db.cursor()
        insert_cursor.execute(insert_query);
        insert_cursor.close()
        db.commit()

        #compare unsw_course vs target_course
        # similarity = get_similarity(unsw_course, target_course["id"])

        # if similarity == None:
        #     # print "No existing sim found for %d vs %d. Processing..." % (int(unsw_course), int(target_course["id"]))
        #     # do sim
        #     # print get_course_keywords_by_id(unsw_course)
        #     sim = compare.compare_keywords(get_course_keywords_by_id(unsw_course)[0],[target_course["keywords"]])
        #     # print sim
