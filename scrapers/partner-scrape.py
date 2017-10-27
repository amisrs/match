from bs4 import BeautifulSoup
import requests

import json
import re


url = "https://student.unsw.edu.au/views/ajax"
baseUrl = "https://student.unsw.edu.au"

payload = {
    "ajax_html_ids[]":"skip-link",
    "ajax_html_ids[]":"header-outer-wrapper",
    "ajax_html_ids[]":"header-wrapper",
    "ajax_html_ids[]":"header",
    "ajax_html_ids[]":"top-links",
    "ajax_html_ids[]":"block-block-1",
    "ajax_html_ids[]":"logo",
    "ajax_html_ids[]":"site-name",
    "ajax_html_ids[]":"top-search",
    "ajax_html_ids[]":"block-cs-topsearch-form",
    "ajax_html_ids[]":"cs-topsearch-block-form",
    "ajax_html_ids[]":"edit-cs-topsearch-block-form--2",
    "ajax_html_ids[]":"edit-cs-topsearch-submit",
    "ajax_html_ids[]":"outer-wrapper",
    "ajax_html_ids[]":"nav-top-border",
    "ajax_html_ids[]":"wrapper-banner",
    "ajax_html_ids[]":"nav-header",
    "ajax_html_ids[]":"nav-wrapper",
    "ajax_html_ids[]":"block-cs-page-nav-signon",
    "ajax_html_ids[]":"cs-page-nav-signon-form",
    "ajax_html_ids[]":"nav-signon-link",
    "ajax_html_ids[]":"nav-signon-popup",
    "ajax_html_ids[]":"nav-signon-popup-inner",
    "ajax_html_ids[]":"edit-username",
    "ajax_html_ids[]":"edit-password",
    "ajax_html_ids[]":"edit-goto",
    "ajax_html_ids[]":"edit-goto-myunsw",
    "ajax_html_ids[]":"edit-goto-moodle",
    "ajax_html_ids[]":"edit-goto-idm",
    "ajax_html_ids[]":"edit-submit",
    "ajax_html_ids[]":"block-handyblock-nav-menu",
    "ajax_html_ids[]":"content-top",
    "ajax_html_ids[]":"wrapper",
    "ajax_html_ids[]":"wrapper-top-border",
    "ajax_html_ids[]":"sidebar-topwhite",
    "ajax_html_ids[]":"main",
    "ajax_html_ids[]":"main-inner",
    "ajax_html_ids[]":"main-heading",
    "ajax_html_ids[]":"main-content",
    "ajax_html_ids[]":"block-system-main",
    "ajax_html_ids[]":"node-9463",
    "ajax_html_ids[]":"block-views-global-partners-block",
    "ajax_html_ids[]":"views-exposed-form-global-partners-block",
    "ajax_html_ids[]":"edit-field-global-partner-search-data-value-wrapper",
    "ajax_html_ids[]":"edit-field-global-partner-search-data-value",
    "ajax_html_ids[]":"edit-field-country-tid-wrapper",
    "ajax_html_ids[]":"edit-field-country-tid",
    "ajax_html_ids[]":"edit-field-language-of-instruction-tid-wrapper",
    "ajax_html_ids[]":"edit-field-language-of-instruction-tid",
    "ajax_html_ids[]":"edit-field-faculty-tid-wrapper",
    "ajax_html_ids[]":"edit-field-faculty-tid",
    "ajax_html_ids[]":"edit-field-student-type-tid-wrapper",
    "ajax_html_ids[]":"edit-field-student-type-tid",
    "ajax_html_ids[]":"edit-field-type-of-study-tid-wrapper",
    "ajax_html_ids[]":"edit-field-type-of-study-tid",
    "ajax_html_ids[]":"edit-submit-global-partners",
    "ajax_html_ids[]":"edit-reset",
    "ajax_html_ids[]":"edit-items-per-page",
    "ajax_html_ids[]":"sidebar-right",
    "ajax_html_ids[]":"block-print-print-links",
    "ajax_html_ids[]":"block-cs-rhsnav-rhs-nav2",
    "ajax_html_ids[]":"block-handyblock-sidebar-seealso",
    "ajax_html_ids[]":"block-handyblock-sidebar-related-notices",
    "ajax_html_ids[]":"block-handyblock-sidebar-related-events",
    "ajax_html_ids[]":"footer",
    "ajax_html_ids[]":"block-menu-menu-footer-menu",
    "ajax_html_ids[]":"block-block-2",
    "ajax_html_ids[]":"back-to-top",
    "ajax_html_ids[]":"wrapper-footer-below",
    "ajax_html_ids[]":"footer-below",
    "ajax_html_ids[]":"block-views-last-updated-block",
    "ajax_page_state[css][modules/field/theme/field.css]":"1",
    "ajax_page_state[css][modules/node/node.css]":"1",
    "ajax_page_state[css][modules/search/search.css]":"1",
    "ajax_page_state[css][modules/system/system.base.css]":"1",
    "ajax_page_state[css][modules/system/system.menus.css]":"1",
    "ajax_page_state[css][modules/system/system.messages.css]":"1",
    "ajax_page_state[css][modules/system/system.theme.css]":"1",
    "ajax_page_state[css][modules/user/user.css]":"1",
    "ajax_page_state[css][sites/all/modules/contrib/calendar/css/calendar_multiday.css]":"1",
    "ajax_page_state[css][sites/all/modules/contrib/ctools/css/ctools.css]":"1",
    "ajax_page_state[css][sites/all/modules/contrib/date/date_api/date.css]":"1",
    "ajax_page_state[css][sites/all/modules/contrib/date/date_popup/themes/datepicker.1.7.css]":"1",
    "ajax_page_state[css][sites/all/modules/contrib/ldap/ldap_servers/ldap_servers.admin.css]":"1",
    "ajax_page_state[css][sites/all/modules/contrib/ldap/ldap_user/ldap_user.css]":"1",
    "ajax_page_state[css][sites/all/modules/contrib/print/css/printlinks.css]":"1",
    "ajax_page_state[css][sites/all/modules/contrib/views/css/views.css]":"1",
    "ajax_page_state[css][sites/all/modules/custom/cc_quiz/misc/node.student-quiz.css]":"1",
    "ajax_page_state[css][sites/all/modules/custom/cc_quiz/misc/node.student-quiz.print.css]":"1",
    "ajax_page_state[css][sites/all/themes/currentstudents/css/ie7.css]":"1",
    "ajax_page_state[css][sites/all/themes/currentstudents/css/ie8.css]":"1",
    "ajax_page_state[css][sites/all/themes/currentstudents/css/ie9.css]":"1",
    "ajax_page_state[css][sites/all/themes/currentstudents/css/print.css]":"1",
    "ajax_page_state[css][sites/all/themes/currentstudents/css/screen.css]":"1",
    "ajax_page_state[css][sites/all/themes/currentstudents/debug.css]":"1",
    "ajax_page_state[css][sites/all/themes/ninesixty/styles/framework/960.css]":"1",
    "ajax_page_state[css][sites/all/themes/ninesixty/styles/framework/debug.css]":"1",
    "ajax_page_state[css][sites/all/themes/ninesixty/styles/framework/reset.css]":"1",
    "ajax_page_state[css][sites/all/themes/ninesixty/styles/framework/text.css]":"1",
    "ajax_page_state[css][sites/all/themes/ninesixty/styles/styles.css]":"1",
    "ajax_page_state[js][0]":"1",
    "ajax_page_state[js][misc/ajax.js]":"1",
    "ajax_page_state[js][misc/drupal.js]":"1",
    "ajax_page_state[js][misc/jquery.cookie.js]":"1",
    "ajax_page_state[js][misc/jquery.form.js]":"1",
    "ajax_page_state[js][misc/jquery.js]":"1",
    "ajax_page_state[js][misc/jquery.once.js]":"1",
    "ajax_page_state[js][misc/progress.js]":"1",
    "ajax_page_state[js][sites/all/modules/contrib/google_analytics/googleanalytics.js]":"1",
    "ajax_page_state[js][sites/all/modules/contrib/views/js/ajax_view.js]":"1",
    "ajax_page_state[js][sites/all/modules/contrib/views/js/base.js]":"1",
    "ajax_page_state[js][sites/all/themes/currentstudents/js/accordion.js]":"1",
    "ajax_page_state[js][sites/all/themes/currentstudents/js/carousel.js]":"1",
    "ajax_page_state[js][sites/all/themes/currentstudents/js/google_analytics.js]":"1",
    "ajax_page_state[js][sites/all/themes/currentstudents/js/jquery.cookie.js]":"1",
    "ajax_page_state[js][sites/all/themes/currentstudents/js/jquery.flexslider-min.js]":"1",
    "ajax_page_state[js][sites/all/themes/currentstudents/js/nav.js]":"1",
    "ajax_page_state[js][sites/all/themes/currentstudents/js/search.js]":"1",
    "ajax_page_state[js][sites/all/themes/currentstudents/js/signon.js]":"1",
    "ajax_page_state[js][sites/all/themes/currentstudents/js/site.js]":"1",
    "ajax_page_state[theme]":"currentstudents",
    "ajax_page_state[theme_token]":"J8uN0McHQdpUbEDtsR35sVgl-0f_a4pvXMo1VDSACuc",
    "field_country_tid":"All",
    "field_faculty_tid":"All",
    "field_global_partner_search_data_value":"",
    "field_language_of_instruction_tid":"92",
    "field_student_type_tid":"18",
    "field_type_of_study_tid":"85",
    "items_per_page":"All",
    "pager_element":"0",
    "view_args":"",
    "view_base_path":"null",
    "view_display_id":"block",
    "view_dom_id":"cdea5d0d9b67eba9cd2f15f32562c999",
    "view_name":"global_partners",
    "view_path":"node/9463"
}

headers = {
    'accept': "application/json, text/javascript, */*; q=0.01",
    'origin': "https://student.unsw.edu.au",
    'x-requested-with': "XMLHttpRequest",
    'user-agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
    'content-type': "application/x-www-form-urlencoded",
    'dnt': "1",
    'referer': "https://student.unsw.edu.au/partners",
    'accept-encoding': "gzip, deflate, br",
    'accept-language': "en-AU,en;q=0.8,en-GB;q=0.6,en-US;q=0.4,ru;q=0.2",
    'cookie': "_ga=GA1.4.712609431.1479894901; SSESS1161c79545847a1f5d8b4c8f3c4265bf=LZznA8w5oKGWc1KMajWi4KSZbAh0vA4WcUlbBk4Unw8; has_js=1; _ga=GA1.3.712609431.1479894901; _ga=GA1.4.712609431.1479894901; SSESS1161c79545847a1f5d8b4c8f3c4265bf=LZznA8w5oKGWc1KMajWi4KSZbAh0vA4WcUlbBk4Unw8; has_js=1",
    'cache-control': "no-cache",
    'postman-token': "b1d35539-06c5-66fb-5b10-40557233b34f"
    }

response = requests.request("POST", url, data=payload, headers=headers)

htmlInsert = ""
responseJson = response.json()

for command in responseJson:
    if command['command'] == "insert":
        htmlInsert = command['data']
        #print command

soup = BeautifulSoup(htmlInsert, 'html.parser')
#print soup.prettify()

tbody = soup.find('tbody')
rowList = tbody.find_all('tr')

uniDict = {}


for row in rowList:
    td = row.find_all('td')
    for col in td:
        link = col.find('h4').find('a')

        uniname = link.string
        href = link['href']
        print uniname + ": " + href

        uniDict[uniname] = href
    #print row
    #print '\n'

# those that offer for business school or engineering
validUniDict = {}

for uni in uniDict:
    print uniDict[uni]
    uniRequest = requests.get(baseUrl+uniDict[uni])
    uniSoup = BeautifulSoup(uniRequest.text, 'html.parser')
    #print uniSoup.prettify()

    data = uniSoup.find("div","global-partner-data")

    faculty = data.find("h4", string="Relevant to UNSW Faculty:")
    countryResult = data.find("h4", string="Country:")
    #print data
    faculties = faculty.next_sibling.string
    country = countryResult.next_sibling.string

    partnersbody = uniSoup.find("div", "partners-body")

    moreinformation = partnersbody.find(string=re.compile("For more information about this institution visit:"))
    print "More information =="
    #print moreinformation
    print moreinformation.next_element

    href = moreinformation.next_element
    #print "the second href is: " + str(href)


    while href.find("a") == None:
        href = href.next_element
        print "moving on... " + str(href)

    print "HREF: " + str(href)

    if "<span" in str(href):
        print "This is for texas."
        href = href.find("a").string
        print href

    unilink = href
    # if str(moreinformation.next_element) == "<br/>":
    #     print "IT WAS A BR"
    #     print moreinformation.next_element.next_element
    #
    #     unilink = moreinformation.next_element.next_element['href']
    # else:
    #     unilink = moreinformation.next_element['href']

    #print faculties

    if "Business" not in faculties and "Engineering" not in faculties:
        print uni + " doesn't have business school or engineering."
    else:
        validUniDict[uni] = {
            "unsw-link": uniDict[uni],
            "link": unilink,
            "country": country
        }
    print "\n"

print json.dumps(validUniDict, indent=4)

validUniFile = open('unis.json', 'w')
validUniFile.write(json.dumps(validUniDict, indent=4))
