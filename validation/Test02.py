import validation.TestBase as BaseClass
import validation.States as s
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

        first_txt_time = math.inf
        first_l1_txt_time = math.inf
        first_bA_time = math.inf
        bg_value = "NO_BG"
        before_l1_txt = "None"
        after_l1_txt = "None"
        after_bA = "None"
        space = " "
        endline = "\n"

        for entry in log_list:
            rec = entry.rec_queried.upper()
            time = entry.sec_from_1970
            # make sure this works, should be base txt record query
            if entry.level == None and rec == s.States.TXT and first_txt_time == None:
                first_txt_time = time
                continue
            if entry.level is not None and entry.level.lower() == s.States.lv1 and rec == s.States.TXT and first_l1_txt_time == None:
                first_l1_txt_time = time
                continue
            if (rec == s.States.A or rec == s.States.AAAA) and entry.level.lower() == "b" and first_bA_time == None:
                first_bA_time = time

        for entry in log_list:  # now we check for BG queries
            time = entry.sec_from_1970
            rec = entry.rec_queried.upper()
            if rec == s.States.TXT or rec == s.States.SPF:  # we want to skip all text records and spf records
                continue
            if first_l1_txt_time is not math.inf and first_l1_txt_time is not math.inf and time > first_txt_time and time < first_l1_txt_time:  # between base txt and l1 txt
                bg_value = "BG"
                before_l1_txt = "BEFORE_L1"
                continue
            if time > first_l1_txt_time and time < first_bA_time:  # between l1 txt &  bA queries
                bg_value = "BG"
                after_l1_txt = "AFTER_L1"
                continue
            if time > first_bA_time and (rec is not AAAA or rec is not A):
                bg_value = "BG"
                after_bA = "AFTER_b"

        # Append test results to file
        result = log_list[
                     0].generated_name + space + bg_value + space + before_l1_txt + space + after_l1_txt + space + after_bA + endline
        f = open("./t02_results.txt", "a+")  # this will append to the t02 results file
        f.write(result)
        f.flush()
        f.close()
