# FxCalendar

[![Actions Status](https://github.com/pakonda/FxCalendar/workflows/Scraping/badge.svg)](https://github.com/pakonda/FxCalendar/actions)

Forex Calendar @ Forex Factory

- For EA
- Update every day
- UTC +0

```text
curl https://pakonda.github.io/FxCalendar/last_update.json

{
    "timestamp": "2019-11-23T06:09:00+00:00",
    "events": [
        {
            "event_id": "105621",
            "currency": "GBP",
            "impact": "Low Impact Expected",
            "event": "Rightmove HPI m/m",
            "actual": "-1.3%",
            "forecast": "",
            "previous": "0.6%",
            "event_dt": "2019-11-18T00:01:00+00:00"
        },
        ...
    ]
}


curl https://pakonda.github.io/FxCalendar/date/2019/11/2019-11-20.json

{
    "timestamp": "2019-11-23T06:09:00+00:00",
    "events": [
        {
            "event_id": "106475",
            "currency": "EUR",
            "impact": "Low Impact Expected",
            "event": "German PPI m/m",
            "actual": "-0.2%",
            "forecast": "0.0%",
            "previous": "0.1%",
            "event_dt": "2019-11-20T07:00:00+00:00"
        },
        ...
    ]
}
```
