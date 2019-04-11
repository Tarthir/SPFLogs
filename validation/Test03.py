import validation.TestBase as BaseClass


# Types
# TXT A AAAA MX SPF NS DS SRV CNAME


class Test03(BaseClass.TestBase):

    def check_testing(self, log_list):
	if len(log_list) == 0:                  # the list is empty for some reason
            return
	first_txt_time = None
        bg_value = "NO_BG"             # were there any bg's period
        before_value = "None"         # bg's came before first txt query
        after_value = "None"          # bg's came after first txt query
        space = " "
        endline = "\n"
        # get frequency of each record type
        records = {}
        for entry in log_list:
            rec = entry.rec_type.upper()
            if records[rec] == None: # in case this is the first time we've seen this rec type
                records[rec] = 0
            records[rec] += 1 # this increases the frequency count of each rec type
       


	for entry in log_list:                  # find if we have a txt query
            if entry.rec_type.upper() == TXT:
                first_txt_time = entry.sec_from_1970
                break


        # contains a TXT query
        if first_txt_time is not None:
            for entry in log_list:
                if entry.sec_from_1970 < first_txt_time: #entries that came before first txt
                    if entry.rec_type is not TXT:
                        bg_value = "BG"
                        before_value = "BEFORE"
                        continue
                if entry.sec_from_1970 > first_txt_time: #entries that came after first txt
                    if entry.rec_type is not TXT:
                        bg_value = "BG"
                        after_value = "AFTER"
                        continue
	else:                                   # does not contain TXT query
            for entry in log_list:
                if entry.rec_type.upper() is not TXT or entry.rec_type.upper() is not SPF:
                    bg_value = "BG"
                    break
 	# Append the test results file
	frequency_string = ""
        for keys in records:
            frequency_string = frequency_string + keys + "=" + records[keys] + " "
        result = log_list[0].generated_name + space + bg_value + space + before_value + space + after_value + space + frequency_string + endline
        f = open("./t03_results.txt", "a+")     # this will append to the t03 results file
        f.write(result)
        f.flush()
        f.close()


















