import validation.TestBase as BaseClass
from validation.States import States as s

# Types
# TXT A AAAA MX SPF NS DS SRV CNAME


class Test03(BaseClass.TestBase):

    def do_testing(self, log_list):
        self.check_testing(log_list)

    def test_def(self, log):
        pass

    def get_test_result(self, log, log_list):
        pass

    def check_testing(self, log_list):
        if len(log_list) == 0:                  # the list is empty for some reason
            return

        print("\n")
        #print(log_list[0].generated_name)
        for log in log_list:
            print(str(log))

        first_txt_time = None
        bg_value = "NO_BG"             # were there any bg's period
        before_value = "None"         # bg's came before first txt query
        after_value = "None"          # bg's came after first txt query
        space = " "
        endline = "\n"
        # get frequency of each record type
        records = {}
        for entry in log_list:
            keys = records.keys()
            rec = entry.rec_queried.upper()
            if rec not in keys: # in case this is the first time we've seen this rec type
                records[rec] = 0
            records[rec] += 1 # this increases the frequency count of each rec type


        for entry in log_list:                  # find if we have a txt query
            if entry.rec_queried.upper() == s.TXT.value:
                first_txt_time = entry.sec_from_1970
                break


        # contains a TXT query
        if first_txt_time is not None:
            for entry in log_list:
                rec = entry.rec_queried.upper()
                if entry.sec_from_1970 < first_txt_time: #entries that came before first txt
                    if rec == s.TXT.value and rec == s.SPF.value:
                        continue
                    else:
                        bg_value = "BG"
                        before_value = "BEFORE"
                        continue
                print("txt: %s\tafter: %s" % (str(first_txt_time), str(entry.sec_from_1970)))
                print("rec: %s\tSPF.value: %s" % (rec, s.SPF.value))
                if entry.sec_from_1970 > first_txt_time: #entries that came after first txt
                    if rec == s.TXT.value and rec == s.SPF.value:
                        continue
                    else:
                        print("why")
                        bg_value = "BG"
                        after_value = "AFTER"
                        continue
        else:                                   # does not contain TXT query
            for entry in log_list:
                if entry.rec_queried.upper() is not s.TXT.value or entry.rec_queried.upper() is not s.SPF.value:
                    bg_value = "BG"
                    break
    # Append the test results file
        frequency_string = ""
        for keys in records:
            frequency_string = frequency_string + keys + "=" + str(records[keys]) + " "
        result = log_list[0].generated_name + space + bg_value + space + before_value + space + after_value + space + frequency_string + endline
        f = open("./t03_results.txt", "a+")     # this will append to the t03 results file
        f.write(result)
        f.flush()
        f.close()
