import datetime
import sys


# This class acts as a data holder for each individual query we get. It stores all pertinent information
class LogHolder:
    def __init__(self, matches):
        # The ip address of the server that queried us
        self.ip = matches.group(6)
        # The port number that came with the address above
        self.port = matches.group(7)
        # lead/baritone/etc
        self.server_name = matches.group(4)
        # Holds which test is this query for
        self.test_name = None
        # The unique generated name of the query
        self.generated_name = None
        # The "level" the query got to
        self.level = None
        # Holds the ".ipv4." or ".ipv6." label if there
        self.ipv_protocol = None
        # parse through the query
        self.parse_query(matches.group(8))
        # Our IP address
        self.server_ip = matches.group(10)
        # convert timestamp to seconds
        self.sec_from_1970 = self.seconds_from(matches.group(1), matches.group(2), matches.group(3))
        record_arr = matches.group(9).strip().split(" ")  # if there is the "T" for tcp we want to grab it
        # grab the record queried for and whether this query was done over TCP
        self.rec_queried, self.tcp = self.check_record(record_arr)

    # Gets the generated name we made from the domain_name
    def parse_query(self, domain_name):
        if "org" in domain_name:
            # split everything but the .org
            tmp = domain_name.split(".", domain_name.count(".") - 1)
        else:
            tmp = domain_name.split(".")
        try:
            # get whether it was ipv4/6 in the domain name
            if "ipv4" in tmp:
                self.ipv_protocol = "ipv4"
            elif "ipv6" in tmp:
                self.ipv_protocol = "ipv6"

            tmp = [item.lower() for item in tmp] # make everything lowercase
            idx = tmp.index("spf-test") # spf-test is always at index 3
            gen_idx = idx - 2
            test_name_idx = idx - 3

            # check to see if our tmp is too short to contain all the info it should
            if idx < 3:  # if the idx of "spf-test" is not what it should be normally
                if idx == 2:  # if we are missing just the test name
                    self.test_name = None
                    self.generated_name = tmp[gen_idx]
                elif idx <= 1:  # if we are missing a randomized name
                    self.write_special_case(tmp)
                    self.generated_name = None
            self.test_name = tmp[test_name_idx]
            self.generated_name = tmp[gen_idx]
            # if there is a level as part of the query
            if (idx - 3) == 1:
                self.level = tmp[0]
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
        with open("data/special_cases.log", "a") as f:
            f.write("%s - %s" % (self.ip, ' '.join(tmp) + "\n"))

    # This method checks the array passed in to see if it contains a T in the 2nd position which signifies TCP
    def check_record(self, record_arr):
        if len(record_arr) == 1:
            return record_arr[0], None
        return record_arr[0], record_arr[1]

    def __str__( self ):
        #return 'log(gen:{},test:{},level:{},record:{},time_1970:{})'.format(self.generated_name,self.test_name,self.level,self.rec_queried,self.sec_from_1970)
        #return 'log(gen:{},test:{},level:{},record:{},ip:{})'.format(self.generated_name,self.test_name,self.level,self.rec_queried,self.ip)
        return 'log(gen:{},test:{},level:{},record:{},tcp:{},time:{},ip_proto:{})'.format(self.generated_name,self.test_name,self.level,self.rec_queried,self.tcp, self.sec_from_1970,self.ipv_protocol)
