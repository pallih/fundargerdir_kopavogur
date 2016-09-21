# -*- coding: utf-8 -*-

import scraperwiki
import lxml.html
import requests
import urlparse
from dateutil import parser

BASE_URL = "http://www.kopavogur.is/stjornsyslan/fundargerdir/"
DATA_URL = "http://www.kopavogur.is/stjornsyslan/fundargerdir/searchmeetings.aspx"

r = requests.get(DATA_URL)
root = lxml.html.fromstring(r.text)
items = root.xpath("//span[@id='l_Content']/table/tr")

data = []

for item in items[1:]:
    meeting = {}
    meeting["titill"] = item[1].text
    meeting["url"] = urlparse.urljoin(BASE_URL, item[0][0].attrib["href"])
    meeting["dagsetning"] = item[2].text
    meeting["date"] = parser.parse(item[2].text)
    meeting["nefnd"] = item[0][0].text
    data.append(meeting)
scraperwiki.sqlite.save(unique_keys=['url'],
                        data=data)
