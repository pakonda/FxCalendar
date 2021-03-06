# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import arrow
from pprint import pprint
import os
import json
import itertools

if not os.path.exists("data"):
    os.makedirs("data")


RUN_DT = arrow.utcnow()
URL = "https://www.forexfactory.com/calendar.php"
COOKIES = {
    "fftimezoneoffset": 0,
    "ffdstonoff": 0,
    "fftimeformat": 1,  # 24H format
    "ffverifytimes": 1,
}


def get_calendar(days_shift: int = 0):
    shifted_dt = RUN_DT.shift(days=days_shift)
    print("start scraping on", shifted_dt.format("YYYY-MM-DD"), end="...")
    params = {"day": shifted_dt.format("MMMDD.YYYY")}
    jar = requests.cookies.RequestsCookieJar()
    for k, v in COOKIES.items():
        jar.set(k, str(v), domain="forexfactory.com", path="/")

    r = requests.get(URL, params=params, cookies=jar)
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

    if len(trs) == 1 and trs[0]["data-eventid"] == "":
        print("no event")
        return []

    events = []
    for tr in trs:
        event = {"event_id": tr["data-eventid"]}
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

        dt = arrow.get(
            f"{shifted_dt.format('YYYY-MM-DD')} {curr_time}", "YYYY-MM-DD H:mm"
        )
        event["event_dt"] = dt.format("YYYY-MM-DDTHH:mm:ssZZ")
        events.append(event)
    print(f"done ({len(events)} events)")
    # pprint(events)

    dir = f"data/date/{shifted_dt.year}/{shifted_dt.month}"
    if not os.path.exists(dir):
        os.makedirs(dir)

    json_file = f"{dir}/{shifted_dt.format('YYYY-MM-DD')}.json"
    json_data = {"timestamp": RUN_DT.format("YYYY-MM-DDTHH:mm:ssZZ"), "events": events}
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(json_data, f)
    return events


if __name__ == "__main__":
    events_day = []
    for i in range(-3, 8):
        events = get_calendar(i)
        events_day.append(events)

    merged = list(itertools.chain.from_iterable(events_day))

    json_data = {"timestamp": RUN_DT.format("YYYY-MM-DDTHH:mm:ssZZ"), "events": merged}
    with open("data/last_update.json", "w", encoding="utf-8") as f:
        json.dump(json_data, f)
