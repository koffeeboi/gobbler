import requests
from bs4 import BeautifulSoup


url = "https://pisa.ucsc.edu/class_search/"


def fetch_class(strm, class_nbr, term):
    form_data = {
        "action": "detail",
        "class_data[:STRM]": strm,
        "class_data[:CLASS_NBR]": class_nbr,
        "binds[:term]": term,
    }

    r = requests.post(url, data=form_data)

    soup = BeautifulSoup(r.text, "html.parser")
    return parse_course_info(soup)


def parse_course_info(soup):
    course_title = find_course_title(soup)
    course_detail = find_course_detail(soup)
    course_desc = find_course_desc_and_class_notes(soup)
    meeting_info = find_meeting_info(soup)
    section_and_labs = find_section_and_lab(soup)

    course_info = {}
    course_info["title"] = course_title
    course_info["detail"] = course_detail
    course_info["desc"] = course_desc
    course_info["meeting_info"] = meeting_info
    course_info["section_and_labs"] = section_and_labs
    return course_info

# Try and find the course title
# Returns a string


def find_course_title(soup):
    rows = soup.find_all("div", "row")
    for row in rows:
        cols = row.find_all("div", "col-xs-12")
        for col in cols:
            h2s = col.find_all("h2")
            for h2 in h2s:
                if h2.text:
                    return h2.text.strip()
    return ""


# Try and find the course detail
# Returns an dict
def find_course_detail(soup):
    course_detail = {}
    dls = soup.find_all("dl", "dl-horizontal")
    for dl in dls:
        dts = soup.find_all("dt")
        dd = soup.find_all("dd")

        if len(dts) != len(dd):
            return None

        for i in range(len(dts)):
            course_detail[dts[i].text] = dd[i].text
    return course_detail


# Try and find the course description and class notes
# Returns an array, where the first element is the course description and the second eleemtn is the class notes
def find_course_desc_and_class_notes(soup):
    desc = []
    panel_bodies = soup.find_all("div", "panel-body")
    for i in range(len(panel_bodies)):
        text = panel_bodies[i].find(text=True, recursive=False).strip()
        if len(text) > 0:
            desc.append(text)
        
    # Hack
    if len(desc) == 0:
        desc.append("")
        desc.append("")
    elif len(desc) == 1:
        desc.append("")

    return desc


# Try and find the meeting information
# Returns an dict
def find_meeting_info(soup):
    meeting_info = {}
    table = soup.find("table")
    rows = table.find_all("tr")
    th = rows[0].find_all("th")
    td = rows[1].find_all("td")
    for i in range(len(th)):
        key = th[i].text.strip()
        info = td[i].text.strip()
        meeting_info[key] = info
    return meeting_info

# Try and find all the lab and sections information
# Returns an array of arrays of lab or section information


def find_section_and_lab(soup):
    section_and_labs = []
    panel_body = soup.find_all("div", "panel-body")

    # Get last panel body
    panel_body = panel_body[len(panel_body) - 1]

    for row in panel_body.find_all("div", "row"):
        section_or_lab = []
        for item in row.find_all("div"):
            section_or_lab.append(item.text.strip())
        section_and_labs.append(section_or_lab)

    return section_and_labs


import json
import datetime

with open("term.json", "r") as infile:
    data = json.load(infile)

courses = data["data"]

curr_item = 0
num_item = len(courses)

course_info = []
for course in courses:
    if all(key in course for key in ("strm", "class_nbr", "term")):
        try:
            course_info.append(fetch_class(
                course["strm"], course["class_nbr"], course["term"]))
            curr_item += 1
            print("Progress {0}/{1}\r".format(curr_item, num_item), end="")
        except:
            print("Failed: ")
            print(course)

all_course_info = {
    "data": course_info,
    "last_updated": str(datetime.datetime.now())
}

with open("course_info.json", "w") as outfile:
    json.dump(all_course_info, outfile, sort_keys=True, indent=4)

