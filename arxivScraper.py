import urllib, urllib.request
import xml.etree.ElementTree as ET
import traceback
import re

from tqdm import trange

from DatabaseBuilder import add_paper, create_database

import tqdm

"""
# url = 'http://export.arxiv.org/api/query?search_query="reinforcement learning"&sortBy=lastUpdatedDate&sortOrder=descending&start=1&max_results=1'
url = 'http://export.arxiv.org/api/query?search_query=cat:cs.CV&sortBy=lastUpdatedDate&sortOrder=descending&max_results=1'
data = urllib.request.urlopen(url)
print(data.read().decode('utf-8'))
"""
short_catagories = []
catagories = urllib.request.urlopen("https://arxiv.org/category_taxonomy")
cata_html = catagories.read().decode("utf-8")

create_database()

top_level_catagores = ["cs", "econ", "eess", "math", "q-bio", "q-fin", "stat"]
for tpc in top_level_catagores:
    cs = re.findall(">" + tpc + "\...", cata_html)
    cs = [cata.replace(">", "") for cata in cs]
    short_catagories = short_catagories + cs

print(short_catagories)


def return_api_url(cata, n=1000):
    return (
        "http://export.arxiv.org/api/query?search_query=%s&sortBy=lastUpdatedDate&sortOrder=descending&max_results=%d"
        % (cata, n)
    )

for x in trange(len(short_catagories)):
    cata = short_catagories[x]
# for cata in short_catagories:
#     # print(cata, return_api_url(cata))

    try:
        papers = urllib.request.urlopen(return_api_url(cata)).read().decode("utf-8")
        tree = ET.fromstring(papers)
    except:
        print("Failed to parse, continuing")
        # print("Failed to parse xml from response (%s)" % traceback.format_exc())
        # exit()
        continue
    list_of_papers = tree.findall("{http://www.w3.org/2005/Atom}entry")
    for paper in list_of_papers:
        authors = list(set([
            c[0].text
            for c in paper.findall(
                "{http://www.w3.org/2005/Atom}author"
            )
        ]))
        categories = [c.attrib['term'] for c in paper.findall("{http://www.w3.org/2005/Atom}category")]
        categories = [c for c in categories if c in short_catagories]
        id = paper.findall("{http://www.w3.org/2005/Atom}id")[0].text
        updated = paper.findall("{http://www.w3.org/2005/Atom}updated")[0].text
        published = paper.findall("{http://www.w3.org/2005/Atom}published")[0].text
        title = paper.findall("{http://www.w3.org/2005/Atom}title")[0].text
        if paper.findall("{http://www.w3.org/2005/Atom}comment"):
            # print(paper.findall("{http://www.w3.org/2005/Atom}comment"))
            comment = paper.findall("{http://www.w3.org/2005/Atom}comment").text
        else:
            comment = ""
        abstract = paper.findall("{http://www.w3.org/2005/Atom}summary")[0].text
        add_paper(id, updated, published, title, abstract, authors, comment, id, categories)
    # breakpoint()
