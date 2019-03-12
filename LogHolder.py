import sys
import datetime

import pytz as pytz


class LogHolder:
    def __init__(self, date, hour, micro_seconds, ip, domain_name):
        self.ip = ip
        self.domain_name = domain_name
        self.test_name = None
        self.generated_name = self.get_generated_name()
        self.sec_from_1970 = self.seconds_from(date, hour, micro_seconds)
    def get_generated_name(self):
        tmp = self.domain_name.split(".")
        for i in range(len(tmp)):
            if "test" in tmp[i] and i != 0:  # testXX is always after the generated name and is not the first in array
                self.test_name = tmp[i - 2]
                return tmp[i - 1]
        if self.test_name is None:
            raise AttributeError("No test name found, passed regex but is not in correct format")

    def seconds_from(self, date, hour, micro_seconds):
        d = date.split("-")
        h = hour.split(":")
        m = micro_seconds.split("-")
        my_date = datetime.datetime(int(d[0]),int(d[1]),int(d[2]),int(h[0]),int(h[1]),int(h[2]),int(m[0]))
        return (my_date-datetime.datetime(1970,1,1)).total_seconds()