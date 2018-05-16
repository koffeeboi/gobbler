import requests

url = "https://pisa.ucsc.edu/class_search/"
data = {
        "action": "results",
        "binds[:term]": 2178,
        "rec_dur": 10000, # Max number of result
}

r = requests.post(
        url,
        data=data
)

from bs4 import BeautifulSoup

# with open("out.html", 'w') as out:
#     out.write(r.text)
