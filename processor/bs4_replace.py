from bs4 import BeautifulSoup

html = """<div class="content" id="module-programmes"><!-- modid 319658 --><h1>2017/18
Undergraduate Module Catalogue</h1>
<h2>
ARAB1001

Beginning Arabic 1</h2>
<h3>20 credits<span style=" margin: 0px; padding: 0px; float: right;">Class Size: 60</span></h3>
<p><strong>Module manager:</strong> Rasha Soliman<br><strong>Email:</strong> <a href="mailto:R.K.Soliman@leeds.ac.uk">R.K.Soliman@leeds.ac.uk</a>
</br></p><p><strong>Taught:</strong> Semester 1 <a href="http://timetable.leeds.ac.uk/teaching/201718/reporting/Individual?objectclass=module&amp;idtype=name&amp;identifier=ARAB100101&amp;&amp;template=SWSCUST+module+Individual&amp;days=1-7&amp;weeks=1-52&amp;periods=1-21">View Timetable</a></p>
<p><strong>Year running</strong> 2017/18</p>
<h3>Co-requisites</h3> <p><table border="1" width="100%"><tr><td width="20%"><a href="dynmodules.asp?Y=201718&amp;M=ARAB-1002">ARAB1002</a></td><td width="80%">Beginning Arabic 2</td></tr></table></p><h3>This module is mutually exclusive with</h3> <p><table border="1" width="100%"><tr><td width="20%"><a href="dynmodules.asp?Y=201718&amp;M=ARAB-1015">ARAB1015</a></td><td width="80%">Arabic for Beginners</td></tr><tr><td width="20%"><a href="dynmodules.asp?Y=201718&amp;M=ARAB-1016">ARAB1016</a></td><td width="80%">Arabic for Beginners</td></tr></table></p><p><strong>This module is not approved as a discovery module</strong></p>
<h3>Module summary</h3>This module offers students an opportunity to progress from the level of a total beginner to (A1 according to the CEFR scale or half a GCSE) in the four skills (reading, writing, speaking and listening) in Modern Standard Arabic. On completion of this module you will be able to understand simple instructions, respond appropriately in everyday situations, express yourself using limited vocabulary and formulaic expressions and use the target language in a limited number of contexts so that it can be understood by a sympathetic native speaker. You will also develop an understanding of the structure of the language and the culture of the countries where the target language is spoken. You will be taught by enthusiastic and competent teachers who have well-established reputation in teaching Arabic as a foreign language.<h3>Objectives</h3>
The aim of this module is to progress students from the level of a total beginner to A1 according to CEFR or half a GCSE in the four skills (reading, writing, speaking and listening) in Modern Standard Arabic. On completion of the module, students will be able to: understand simple instructions, respond appropriately in everyday situations, express themselves using limited vocabulary and formulaic expressions and use the target language in a limited number of contexts so that it can be understood by a sympathetic native speaker. Students will also develop an understanding of the structure of the language and the culture of the countries where the target language is spoken.
<br><h3>Syllabus</h3><p>A beginner''s course which encourages communication in the target language.  The study of grammatical structures and the acquisition of cultural awareness are incorporated into the language learning programme.  This course encourages interactive communication in class through the use of a variety of materials.  A wide range of subjects will be studied in class using audio-visual as well as audio and written materials to utilise and consolidate the use of the four communicative skills (reading, writing, speaking and hearing).  Topics/skills covered at this level include communication in everyday situations (through role-play) and the comprehension of short, simple texts.</p>
<h3>Teaching methods</h3><p><table border="1" width="100%"><tr><td align="left" width="40%">Delivery type</td><td align="right" width="20%">Number</td><td align="right" width="20%">Length hours</td><td align="right" width="20%">Student hours</td></tr><tr><td>Language Class</td><td align="right">10</td><td align="right">2.00</td><td align="right">20.00</td></tr><tr><td>Lecture</td><td align="right">30</td><td align="right">2.00</td><td align="right">60.00</td></tr><tr><td colspan="3">Private study hours</td><td align="right">120.00</td></tr><tr><td colspan="3">Total Contact hours</td><td align="right">80.00</td></tr><tr><td colspan="3">Total hours (100hr per 10 credits)</td><td align="right">200.00</td></tr></table><h3>Private study</h3>preparatory reading for lectures/languages classes, completion of coursework and exam preparation<br/></p>
<h3>Opportunities for Formative Feedback</h3>Students'' progress will be monitored through weekly language coursework, oral presentations and written examination.</br></div>"""
# html = "<p><strong>This module is not approved as a discovery module</strong></p>"


soup = BeautifulSoup(html, 'lxml')
print soup

print "\n\nREPLACING"
for p_element in soup.find_all('p'):
    print p_element
    p_element.replace_with(p_element.text + ".")
    print p_element
print "DONE\n\n"
print soup
