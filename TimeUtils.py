#! python3
# coding=utf-8

import time
import datetime
import RandomUtils


class TimeUtils:

    @staticmethod
    def str_2_datetime(str_time, pattern='%Y-%m-%d %H:%M:%S'):
        return datetime.datetime.strptime(str_time, pattern)

    @staticmethod
    def get_today_datetime():
        return datetime.date.today()

    @staticmethod
    def replace_year(date_time, year_new):
        return date_time.replace(year=year_new)

    @staticmethod
    def replace_month(date_time, month_new):
        return date_time.replace(month=month_new)

    @staticmethod
    def replace_day(date_time, day_new):
        return date_time.replace(day=day_new)

    @staticmethod
    def replace_hour(date_time, hour_new):
        return date_time.replace(hour=hour_new)

    @staticmethod
    def replace_minute(date_time, minute_new):
        return date_time.replace(minute=minute_new)

    @staticmethod
    def replace_second(date_time, second_new):
        return date_time.replace(second=second_new)

    @staticmethod
    def datetime_replace(date_time, year=None, month=None, day=None, hour=None, minute=None, second=None):
        if year is None:
            year = date_time.year
        if month is None:
            month = date_time.month
        if day is None:
            day = date_time.day
        if hour is None:
            hour = date_time.hour
        if minute is None:
            minute = date_time.minute
        if second is None:
            second = date_time.second
        return date_time.replace(year=year, month=month, day=day, hour=hour, minute=minute, second=second)

    @staticmethod
    def sleep(ms):
        time.sleep(ms * 0.001)

    @staticmethod
    def sleep_random():
        time.sleep(RandomUtils.RandomUtils.get_random_int())

    #
    # e.g. 2019-05-26 --> [2019-05-26 00:00:00, 2019-05-26 23:59:59]
    #      05-26      --> [2019-05-26 00:00:00, 2019-05-26 23:59:59]
    #
    @staticmethod
    def get_datetime_range(datetime_list, date_pattern='%Y-%m-%d'):
        datetimes_range_list = list()
        for date_time in datetime_list:
            datetime_range_list = list()
            date_time = TimeUtils.str_2_datetime(date_time, date_pattern)
            if 'Y' not in date_pattern:  # 没有提供年份
                date_time = TimeUtils.replace_year(date_time, TimeUtils.get_today_datetime().year)
            datetime_range_list.append(date_time)
            datetime_range_list.append(TimeUtils.datetime_replace(date_time, hour=23, minute=59, second=59))
            datetimes_range_list.append(datetime_range_list)
        return datetimes_range_list
