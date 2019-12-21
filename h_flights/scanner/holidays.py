import requests
import datetime

HOLIDAYS_REST_API_URL="https://www.hebcal.com/hebcal/?v=1&cfg=json&maj=on&min=off&mod=off&nx=off&year={year}&month=x&ss=off&s=off&mf=off&c=off&geo=none&m=50&s=on"
TOTAL_MONTHS_IN_YEAR = 12
SEARCH_FLIGHTS_MONTHS = 10

def fetch_holidays_api(year):

    holidays_json = None
    try:
        # fetch holidays from the API
        response = requests.get(HOLIDAYS_REST_API_URL.format(year=year))

        # make sure the response is valid
        response.raise_for_status()

        holidays_json = response.json()

    except:
        print("error - failed to nagotiate holidays api")

    return holidays_json


def convert_to_dates_list(holidays_json, dates_list):

    pass


def get_holidays_dates():

    current_year = datetime.datetime.now().year
    current_month = datetime.datetime.now().month

    # fetch current year holidays
    current_year_holidays = fetch_holidays_api(current_year)

    if not current_year_holidays:
        return

    # in case this year has not enough months left, search for next year dates as well
    if (TOTAL_MONTHS_IN_YEAR - current_month) < SEARCH_FLIGHTS_MONTHS:
        next_year_holidays = fetch_holidays_api(current_year + 1)

    dates_list = []
    convert_to_dates_list(current_year_holidays, dates_list)

    if next_year_holidays:
        convert_to_dates_list(next_year_holidays, dates_list)

    
    # adding the summer vacation to the dates list (those dates are not provided by holidays api)
    #dates_list.append(())