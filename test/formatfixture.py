def get_value(dict, key):
    # Integer field
    if key in ["Available Seats", "Class Number", "Enrolled", "Enrollment Capacity",
               "Wait List Capacity", "Wait List Total", ]:
        if key in dict:
            return int(dict[key])
        else:
            return 0

    # Char field
    if key in dict:
        return dict[key]
    else:
        return ""


def format_to_fixture(all_course_info):
    formatted = []

    lab_index_key = 1

    courses = all_course_info["data"]
    for i in range(len(courses)):
        course = courses[i]
        index_key = i + 1  # Start index at 1 for django pk
        if all(key in course for key in ("desc", "detail", "meeting_info", "section_and_labs")):
            section_or_lab_exists = False

            for section_or_lab in course["section_and_labs"]:
                section_or_lab_exists = True

                sec_lab_fields = {}
                sec_lab_fields["course_num"] = get_value(
                    course["detail"], "Class Number")
                sec_lab_fields["class_id"] = section_or_lab[0]
                sec_lab_fields["time"] = section_or_lab[1]
                sec_lab_fields["instructor"] = section_or_lab[2]
                sec_lab_fields["location"] = section_or_lab[3]
                sec_lab_fields["enrollment"] = section_or_lab[4]
                sec_lab_fields["wait"] = section_or_lab[5]
                sec_lab_fields["status"] = section_or_lab[6]

                sec_lab = {}
                sec_lab["model"] = "api.sectionlab"
                sec_lab["pk"] = lab_index_key
                sec_lab["fields"] = sec_lab_fields

                formatted.append(sec_lab)
                lab_index_key += 1 


            course_fields = {}
            course_fields["title"] = get_value(course, "title")
            course_fields["description"] = course["desc"][0]
            course_fields["class_notes"] = course["desc"][1]
            course_fields["available_seats"] = get_value(
                course["detail"], "Available Seats")
            course_fields["career"] = get_value(course["detail"], "Career")
            course_fields["class_num"] = get_value(
                course["detail"], "Class Number")
            course_fields["credits"] = get_value(course["detail"], "Credits")
            course_fields["enrolled"] = get_value(course["detail"], "Enrolled")
            course_fields["enrollment_capacity"] = get_value(
                course["detail"], "Enrollment Capacity")
            course_fields["general_education"] = get_value(
                course["detail"], "General Education")
            course_fields["grading"] = get_value(course["detail"], "Grading")
            course_fields["status"] = get_value(course["detail"], "Status")
            course_fields["type"] = get_value(course["detail"], "Type")
            course_fields["waitlist_capacity"] = get_value(
                course["detail"], "Wait List Capacity")
            course_fields["waitlist_total"] = get_value(
                course["detail"], "Wait List Total")
            course_fields["days_and_times"] = get_value(
                course["meeting_info"], "Days & Times")
            course_fields["instructor"] = get_value(
                course["meeting_info"], "Instructor")
            course_fields["meeting_dates"] = get_value(
                course["meeting_info"], "Meeting Dates")
            course_fields["room"] = get_value(course["meeting_info"], "Room")

            # Foreign key to SectionLab
            if section_or_lab_exists:
                course_fields["section_and_labs"] = index_key

            formatted_course = {}
            formatted_course["model"] = "api.course"
            formatted_course["pk"] = index_key
            formatted_course["fields"] = course_fields

            formatted.append(formatted_course)
    return formatted


import json

with open("course_info.json", "r") as infile:
    all_course_info = json.load(infile)

fixture = format_to_fixture(all_course_info)

with open("course_info_fixture.json", "w") as outfile:
    json.dump(fixture, outfile, sort_keys=True, indent=4)
