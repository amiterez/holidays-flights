import requests
import datetime
from datetime import datetime
from datetime import timedelta

HOLIDAYS_REST_API_URL="https://www.hebcal.com/hebcal/?v=1&cfg=json&maj=on&min=off&mod=off&nx=off&year={year}&month=x&ss=off&s=off&mf=off&c=off&geo=none&m=50&s=on"
TOTAL_MONTHS_IN_YEAR = 12
SEARCH_FLIGHTS_MONTHS = 11
AVG_DAYS_IN_MONTH = 30
DAY_OFF_NUMBER = 5 # Shabat day off
DATE_FORMAT = '%Y-%m-%d'
SUMMER_VACATION_START = '{}-07-01'
SUMMER_VACATION_END = '{}-08-31'



# Major holidays names
PASSOVER = 'Pesach'
PURIM = 'Purim'
SUKKOT = 'Sukkot'
CHANUKAH = 'Chanukah'
ROSH_HASHANA = 'Rosh Hashana'
SHAVUOT = 'Shavuot'

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

def is_holiday(holiday_name):
    return holiday_name.find(PASSOVER) >= 0 or \
           holiday_name.find(PURIM) >= 0 or  \
           holiday_name.find(SUKKOT) >= 0 or \
           holiday_name.find(CHANUKAH) >= 0 or \
           holiday_name.find(ROSH_HASHANA) >= 0 or \
           holiday_name.find(SHAVUOT) >= 0


def convert_to_dates_list(holidays_json, dates_list):

    for holiday in holidays_json["items"]:
        if (is_holiday(holiday["title"])):
            datetime_object = datetime.strptime(holiday["date"], DATE_FORMAT).date()

            # add the date to the list in case its not too fat in the future
            end_date = (datetime.now() + timedelta(days=(SEARCH_FLIGHTS_MONTHS * AVG_DAYS_IN_MONTH))).date()
            if datetime_object < end_date:
                dates_list.append(datetime_object)


def merge_dates(dates_list):

    holidays = []

    index_start = 0

    # merge dates to dates intervals
    for curr_index, curr_date in enumerate(dates_list):

        # if the current day is not the day after last day in the list - create a new dates interval
        if (curr_index != 0) and (dates_list[curr_index - 1] + timedelta(days=1) != curr_date):

            start_date = dates_list[index_start]
            end_date = dates_list[curr_index - 1]

            # add shabat (also day off) if its close to start/end dates
            if (start_date - timedelta(days=1)).weekday() == DAY_OFF_NUMBER:
                start_date = start_date - timedelta(days=1)
            elif (end_date + timedelta(days=1)).weekday() == DAY_OFF_NUMBER:
                end_date = start_date + timedelta(days=1)

            # add current date interval
            holidays.append((start_date, end_date))
            index_start = curr_index

            #  add close saturday

    holidays.append((dates_list[index_start], dates_list[len(dates_list) - 1]))

    return holidays

def add_summer_vacation(holidays):

    # set summer vacation dates
    summer_vacation_start = datetime.strptime(SUMMER_VACATION_START.format(datetime.now().year), DATE_FORMAT).date()
    summer_vacation_end   = datetime.strptime(SUMMER_VACATION_END.format(datetime.now().year), DATE_FORMAT).date()

    # in case the summer vacation of that year has alreay passed, set the date to the next year vacation
    if summer_vacation_end < datetime.now().date():
        summer_vacation_start = datetime.strptime(SUMMER_VACATION_START.format(datetime.now().year + 1), DATE_FORMAT).date()
        summer_vacation_end = datetime.strptime(SUMMER_VACATION_END.format(datetime.now().year + 1), DATE_FORMAT).date()

    holidays.append((summer_vacation_start, summer_vacation_end))

    return holidays

def get_holidays_dates():

    current_year = datetime.now().year
    current_month = datetime.now().month

    # fetch current year holidays
    current_year_holidays = fetch_holidays_api(current_year)

    if not current_year_holidays:
        return

    # in case this year has not enough months left, search for next year dates as well
    next_year_holidays = False
    if (TOTAL_MONTHS_IN_YEAR - current_month) < SEARCH_FLIGHTS_MONTHS:
        next_year_holidays = fetch_holidays_api(current_year + 1)

    # convert holidays json into dates list
    dates_list = []
    convert_to_dates_list(current_year_holidays, dates_list)

    # convert holidays of next year
    if next_year_holidays:
        convert_to_dates_list(next_year_holidays, dates_list)

    # Merging all dates to holidays periods over the year
    holidays = merge_dates(dates_list)

    # adding the summer vacation to the dates list (those dates are not provided by holidays api)
    holidays = add_summer_vacation(holidays)

    return holidays