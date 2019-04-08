import datetime
import sys


# This class acts as a data holder for each individual query we get. It stores all pertinent information
class LogHolder:
    def __init__(self, matches):
        self.ip = matches.group(6)
        self.port = matches.group(7)
        self.server_name = matches.group(4)
        self.test_name = None
        self.generated_name = self.get_generated_name(matches.group(8))
        self.sec_from_1970 = self.seconds_from(matches.group(1), matches.group(2), matches.group(3))
        self.rec_queried = matches.group(9)

    # Gets the generated name we made from the domain_name
    def get_generated_name(self, domain_name):
        if "org" in domain_name:
            # split everything but the .org
            tmp = domain_name.split(".", domain_name.count(".") - 1)
        else:
            tmp = domain_name.split(".")
        try:
            tmp = [item.lower() for item in tmp] # make everything lowercase
            # TODO make this case insensitive
            idx = tmp.index("spf-test") # spf-test is always at index 3
            # check to see if our tmp is too short to contain all the info it should
            if idx < 3:  # if the idx of "spf-test" is not what it should be normally
                if idx == 2:  # if we are missing just the test name
                    self.test_name = None
                    return tmp[idx - 2]
                elif idx <= 1:  # if we are missing a randomized name
                    self.write_special_case(tmp)
                    return None
            self.test_name = tmp[idx - 3]
            return tmp[idx - 2]
        except ValueError as error:
            sys.stderr.write("Error: %s\n" % str(error))

    # Take the date that we got and convert it into seconds for sorting purposes
    def seconds_from(self, date, hour, micro_seconds):
        d = date.split("-")
        h = hour.split(":")
        m = micro_seconds.split("-")
        my_date = datetime.datetime(int(d[0]),int(d[1]),int(d[2]),int(h[0]),int(h[1]),int(h[2]),int(m[0]))
        return (my_date-datetime.datetime(1970,1,1)).total_seconds()

    def write_special_case(self, tmp):
        with open("special_cases.log", "a") as f:
            f.write("%s - %s" % (self.ip, ' '.join(tmp) + "\n"))
