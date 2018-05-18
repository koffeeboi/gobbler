
def format_to_fixture(all_course_info):
    formatted = [] 

    courses = all_course_info["data"]
    for i in range(len(courses)):
        course = courses[i]
        if all(key in course for key in ("desc", "detail", "meeting_info", "section_and_labs")):
            course_fields = {}
            course_fields["title"] = course["title"]
            course_fields["description"] = course["desc"][0]
            course_fields["class_notes"] = course["desc"][1]

            formatted_course = {}
            formatted_course["model"] = "api.course"
            formatted_course["pk"] = i + 1 # Start index at 1 for django pk
            formatted_course["course_fields"] = course_fields

            formatted.append(formatted_course)
    return formatted

import json

with open("course_info.json", "r") as infile:
    all_course_info = json.load(infile)

fixture = format_to_fixture(all_course_info)

with open("course_info_fixture.json", "w") as outfile:
    json.dump(fixture, outfile, sort_keys=True, indent=4)
