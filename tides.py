import json
import requests
import logging
from collections import namedtuple, OrderedDict
from bs4 import BeautifulSoup

# A simple record to hold tide information
TideInfo = namedtuple(
    'TideInfo',
    ['date', 'time', 'time_zone', 'level_metric', 'level_std', 'event'])


def extract_tide_info(page):
    """Pull all tide information from a hypertext page"""

    soup = BeautifulSoup(page, "html.parser")
    tide_table = soup.find("table", class_="tide-table")

    for row in tide_table.find_all("tr"):
        logging.debug(u"Parsing row: {0}".format(row))

        date = row.find("th", class_="date")
        if date is not None:
            cur_date = date.getText().strip()

        cells = [x.getText().strip() for x in row.find_all("td")]
        if len(cells) != 5:
            logging.error(u"Malformed row: {0}".format(row))
            continue

        # Can probably do more parsing here e.g. to convert things
        # into nicer python representations (dates as datetimes, etc)
        yield TideInfo(
            date=cur_date,
            time=cells[0],
            time_zone=cells[1],
            level_metric=cells[2],
            level_std=cells[3].strip("()"),
            event=cells[4])


def daylight_low_tides(tide_data):
    """Extract low tide information from a set of tide data"""

    grouped_by_date = OrderedDict()
    for tide_info in tide_data:
        key = tide_info.date
        if key not in grouped_by_date:
            grouped_by_date[key] = list()
        grouped_by_date[key].append(tide_info)

    for date in grouped_by_date:
        state = "Predawn"
        for item in grouped_by_date[date]:
            if state == "Predawn":
                if item.event == "Sunrise":
                    state = "Daylight"
            elif state == "Daylight":
                if item.event == "Low Tide":
                    yield item
                elif item.event == "Sunset":
                    # Don't let the sun go down on me
                    break

if __name__ == "__main__":
    import sys

    # In future work, I would find a better way to automatically compute these
    # location identifiers. I played around with the site for a few minutes,
    # trying to figure out a nice way to do this, but gave up and moved on to
    # parsing the tide tables. Also, even without that, I should take these as
    # arguments instead of as a static list
    locations = [
        "Half-Moon-Bay-California",
        "Huntington-Beach",
        "Providence-Rhode-Island",
        "Wrightsville-Beach-North-Carolina"
    ]

    url_template = "https://www.tide-forecast.com/locations/{0}/tides/latest" 
    json_result = OrderedDict()
    for loc in locations:
        url = url_template.format(loc)
        response = requests.get(url)
        json_result[loc] = [
            x._asdict()
            for x in daylight_low_tides(extract_tide_info(response.text))
        ]

    sys.stdout.write(json.dumps(json_result, indent=4))
