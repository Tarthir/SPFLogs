import validation.TestBase as BaseClass

# results = "generated_name" "BG or NO_BG" "BEFORE or None" "AFTER or None"

class Test01(BaseClass.TestBase):

    def check_testing(self, log_list):
        if len(log_list) == 0:                  # the list is empty for some reason
            return
        first_txt_time = None
        bg_value = "NO_BG"             # were there any bg's period
        before_value = "None"         # bg's came before first txt query
        after_value = "None"          # bg's came after first txt query
        space = " "
        endline = "\n"
        
        for entry in log_list:                  # find if we have a txt query
            if entry.rec_type.upper() == TXT:
                first_txt_time = entry.sec_from_1970
                break


        # contains a TXT query
        if first_txt_time is not None:
            for entry in log_list:
                if entry.sec_from_1970 < first_txt_time: #entries that came before first txt
                    if entry.rec_type.upper() is not TXT:
                        bg_value = "BG"
                        before_value = "BEFORE"
                        continue
                if entry.sec_from_1970 > first_txt_time: #entries that came after first txt
                    if entry.rec_type.upper() is not TXT:
                        bg_value = "BG"
                        after_value = "AFTER"
                        continue


        else:                                   # does not contain TXT query
            for entry in log_list:
                if entry.rec_type.upper() is not TXT or entry.rec_type.upper() is not SPF:
                    bg_value = "BG"
                    break

        # _______________in the future we can count the frequency of record types here________

        # Append the test results file
        result = log_list[0].generated_name + space + bg_value + space + before_value + space + after_value + endline
        f = open("./t01_results.txt", "a+")     # this will append to the t01 results file
        f.write(result)
        f.flush()
        f.close()

