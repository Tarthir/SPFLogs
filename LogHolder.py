import datetime


# This class acts as a data holder for each individual query we get. It stores all pertinent information
class LogHolder:
    def __init__(self, matches):
        self.ip = matches.group(6)
        self.port = matches.group(7)
        self.servername = matches.group(4)
        self.test_name = None
        self.generated_name = self.get_generated_name(matches.group(8))
        # run this later?
        self.sec_from_1970 = self.seconds_from(matches.group(1), matches.group(2), matches.group(3))

    # Gets the generated name we made from the domain_name
    def get_generated_name(self, domain_name):
        tmp = domain_name.split(".")
        try:
            idx = tmp.index("spf-test") # spf-test is always at index 3
            # check to see if our tmp is too short to contain all the info it should
            if idx - 2 < 0 or idx - 3 < 0:
                self.write_special_case(tmp)
            self.test_name = tmp[idx - 3]
            return tmp[idx - 2]
        except ValueError as error:
            sys.stderr.write("Error: %s\n" % str(error))

    def seconds_from(self, date, hour, micro_seconds):
        d = date.split("-")
        h = hour.split(":")
        m = micro_seconds.split("-")
        my_date = datetime.datetime(int(d[0]),int(d[1]),int(d[2]),int(h[0]),int(h[1]),int(h[2]),int(m[0]))
        return (my_date-datetime.datetime(1970,1,1)).total_seconds()

    def write_special_case(self, tmp):
        with open("special_cases.log", "a") as f:
            f.write("%s - %s" % (self.ip, str(tmp) + "\n"))
