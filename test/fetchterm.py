import requests
from bs4 import BeautifulSoup


terms = []

# Retrieves all the terms options
def fetch_all_terms():
    url = "https://pisa.ucsc.edu/class_search/"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    for option in soup.find_all(id="term_dropdown"):
        for term in option.find_all("option"):
           terms.append(term["value"])


# Retrieves all the classes for a term
def fetch_all_classes_from_term(term=2178, max_results=10000):
    url = "https://pisa.ucsc.edu/class_search/"
    data = {
        "action": "results",
        "binds[:term]": term,
        "rec_dur": max_results,  # Max number of classes retrieved
    }

    r = requests.post(url, data=data)
    return r.text


with open("out.html") as fp:
    soup = BeautifulSoup(fp, "html.parser")
# soup = BeautifulSoup(, 'html.parser')

data = []
for form in soup.find_all("form"):
    form_data = {}
    for form_input in form.find_all("input"):
        name = form_input["name"]
        value = form_input["value"]
        if name == "class_data[:STRM]":
            form_data["strm"] = value
        elif name == "class_data[:CLASS_NBR]":
            form_data["class_nbr"] = value
        elif name == "binds[:term]":
            form_data["term"] = value
        elif name == "binds[:session_code]":
            form_data["session_code"] = value
        elif name == "rec_start":
            form_data["rec_start"] = value
        elif name == "rec_dur":
            form_data["rec_dur"] = value
    data.append(form_data)

import datetime
# Import to keep track when we updated for the users and the developer to know when to force an update or change the update rate
# FIXME Make last_updated timezone aware, or respect unix timestamp
data = {
    "last_updated": str(datetime.datetime.now()),
    "data": data
}

import json

with open("term.json", "w") as outfile:
    json.dump(data, outfile, sort_keys=True, indent=4)

# with open("out.html", 'w') as out:
#    out.write(soup.prettify())
