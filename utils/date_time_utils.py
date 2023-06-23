from datetime import date, datetime, timedelta, time
from dateutil.relativedelta import relativedelta
from dateutil import parser


def find_time_diff_from_midnight(route_time):
    route_time = str(route_time).split(":")
    today_date = str(date.today()).split("-")
    tomm_date = str(date.today() + timedelta(days=1)).split("-")

    time1 = datetime(int(today_date[0]), int(today_date[1]), int(today_date[2]), int(route_time[0]), int(route_time[1]),
                     0)
    time2 = datetime(int(tomm_date[0]), int(
        tomm_date[1]), int(tomm_date[2]), 0, 0, 0)

    time_delta = time2 - time1
    time_delta_in_seconds = time_delta.total_seconds()
    diff_in_minutes = int(time_delta_in_seconds / 60)

    return diff_in_minutes


def get_time_from_duration(old_time, duration):
    old_time_hour = old_time.hour
    old_time_mins = old_time.minute
    dt = datetime.combine(date.today(), time(
        old_time_hour, old_time_mins)) + timedelta(minutes=duration)

    return dt.time()


def difference_in_days(start_date, end_date):
    start_date = str(start_date).split("-")
    end_date = str(end_date).split("-")

    start_date_obj = date(int(start_date[0]), int(
        start_date[1]), int(start_date[2]))
    end_date_obj = date(int(end_date[0]), int(end_date[1]), int(end_date[2]))

    delta = end_date_obj - start_date_obj
    total_days = delta.days

    return total_days, start_date_obj, end_date_obj


def find_new_time(old_time, duration):
    old_time_hour = old_time.hour
    old_time_mins = old_time.minute
    dt = datetime.combine(old_time.date(), time(
        old_time_hour, old_time_mins)) + timedelta(minutes=duration)

    return dt


def difference_bt_timestamps(timestamp_1, timestamp_2):
    diff = relativedelta(timestamp_1, timestamp_2)
    return diff.days, diff.hours, diff.minutes


def difference_bt_timestamps_2(timestamp_1, timestamp_2):
    diff = relativedelta(timestamp_1, timestamp_2)
    return diff.months, diff.days, diff.hours, diff.minutes


def is_nearby_time(time_1, time_2, allowed_diff_minutes):
    greater = time_1
    smaller = time_2

    if smaller > greater:
        greater, smaller = smaller, greater

    diff_minutes = (greater - smaller).seconds // 60

    if abs(diff_minutes) < allowed_diff_minutes:
        return True
    return False
