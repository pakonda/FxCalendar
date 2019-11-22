# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import arrow
from pprint import pprint

now = arrow.utcnow()
URL = "https://www.forexfactory.com/calendar.php"
PARAMS = {"day": now.format("MMMDD.YYYY")}
COOKIES = {
    "fftimezoneoffset": 0,
    "ffdstonoff": 0,
    "fftimeformat": 1,  # 24H format
    "ffverifytimes": 1,
}


jar = requests.cookies.RequestsCookieJar()
for k, v in COOKIES.items():
    jar.set(k, str(v), domain="forexfactory.com", path="/")

r = requests.get(URL, params=PARAMS, cookies=jar)
soup = BeautifulSoup(r.content, "html.parser")
table = soup.find("table", {"class": "calendar__table"})
trs = table.select("tr.calendar__row.calendar_row")
fields = [
    "date",
    "time",
    "currency",
    "impact",
    "event",
    "actual",
    "forecast",
    "previous",
]

events = []
for tr in trs:
    event = {}
    for field in fields:
        data = tr.select(f"td.calendar__cell.calendar__{field}.{field}")[0]
        if field == "date" and data.text.strip() != "":
            curr_date = data.text.strip()
        elif field == "time" and data.text.strip() != "":
            curr_time = data.text.strip() if ":" in data.text.strip() else "00:00"
        elif field == "currency":
            event[field] = data.text.strip()
        elif field == "impact":
            event[field] = data.find("span")["title"]
        elif field == "event":
            event[field] = data.text.strip()
        elif field == "actual":
            event[field] = data.text.strip()
        elif field == "forecast":
            event[field] = data.text.strip()
        elif field == "previous":
            event[field] = data.text.strip()

    dt = arrow.get(f"{now.format('YYYY-MM-DD')} {curr_time}", "YYYY-MM-DD H:mm")
    event["datetime"] = str(dt)
    events.append(event)


pprint(events)
