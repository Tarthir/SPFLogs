import validation.TestBase as BaseClass
from validation.States import States as s
import math


# Assuming that the log_list will be sorted chronological order

class Test02(BaseClass.TestBase):

    def do_testing(self, log_list):
        self.check_testing(log_list)

    def test_def(self, log):
        pass

    def get_test_result(self, log, log_list):
        pass

    def check_testing(self, log_list):
        if len(log_list) == 0:  # the list is empty for some reason
            return

        print("\n")
        #print(log_list[0].generated_name)
        for log in log_list:
            print(str(log))
        first_txt_time = math.inf
        first_l1_txt_time = math.inf
        first_bA_time = math.inf
        bg_value = "NO_BG"
        before_l1_txt = "None"
        after_l1_txt = "None"
        after_bA = "None"
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

        for entry in log_list:
            rec = entry.rec_queried.upper()
            time = entry.sec_from_1970
            # make sure this works, should be base txt record query
            if entry.level == None and rec == s.TXT.value and first_txt_time == math.inf:
                first_txt_time = time
                continue
            if entry.level is not None and entry.level.lower() == s.lv1.value and rec == s.TXT.value and first_l1_txt_time == math.inf:
                first_l1_txt_time = time
                continue
            if entry.level is not None and (rec == s.A.value or rec == s.AAAA.value) and entry.level.lower() == "b" and first_bA_time == math.inf:
                first_bA_time = time
        print("txt: %s\t l1: %s\t bA: %s" % (str(first_txt_time), str(first_l1_txt_time), str(first_bA_time)))
        for entry in log_list:  # now we check for BG queries
            if entry.level is not None and entry.level.lower() == "_dmarc":
                continue
            time = entry.sec_from_1970
            rec = entry.rec_queried.upper()
            if rec == s.TXT.value or rec == s.SPF.value:  # we want to skip all text records and spf records
                continue
            if first_l1_txt_time is not math.inf and first_l1_txt_time is not math.inf and time > first_txt_time and time < first_l1_txt_time:  # between base txt and l1 txt
                bg_value = "BG"
                before_l1_txt = "BEFORE_L1"
                continue
            if time > first_l1_txt_time and time < first_bA_time:  # between l1 txt &  bA queries
                bg_value = "BG"
                after_l1_txt = "AFTER_L1"
                continue
            if time > first_bA_time and entry.level is not "b" and (rec is not s.AAAA.value or rec is not s.A.value):
                #print(rec)
                bg_value = "BG"
                after_bA = "AFTER_b"
        bool = True
        if bg_value == "NO_BG":
            for log in log_list:
                rec = log.rec_queried.upper()
                if rec == s.TXT.value or rec == s.SPF.value:
                    bool = False
            if bool:
                bg_value = "NO_TXT"


        # Append test results to file
        frequency_string = ""
        for keys in records:
            frequency_string = frequency_string + keys + "=" + str(records[keys]) + " "
        result = log_list[
                     0].generated_name + space + bg_value + space + before_l1_txt + space + after_l1_txt + space + after_bA + space + frequency_string + endline
        f = open("./validation_results/t02_results.txt", "a+")  # this will append to the t02 results file
        f.write(result)
        f.flush()
        f.close()
        # does an extra b...A query at the end count as a BG? ************************
