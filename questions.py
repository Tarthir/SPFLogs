#!/usr/bin/python
import sys
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
import numpy as np
import time
# Script that looks at results of t01 - t03

# Questions:
# How many did no BG for t01 - t03?
# How many had differing behavior for all 3 tests?
# How many did the same queries for each test no matter what?
# How many did the same queries for t01 and t03?
# How many did BG queries before the best TXT query for t01 and t03?
# How many did BG queries after the final one for all 3 tests?

#-----------------------------------CLASSES--------------------------------------
class Test01:
    def __init__( self, bg, before, after, rec_list ):
        self.test = 1
        self.bg = bg
        self.before = before
        self.after = after
        self.rec_list = rec_list
    def __str__( self ):
        return 'Test01(bg:{}, before:{}, after:{}, rec_list:{}'.format(self.bg,self.before,self.after,str(self.rec_list))
class Test02:
    def __init__( self, bg, before_l1, after_l1, after_ba, rec_list ):
        self.test = 2
        self.bg = bg
        self.before_l1 = before_l1
        self.after_l1 = after_l1
        self.after_ba = after_ba
        self.rec_list = rec_list
    def __str__( self ):
        return 'Test02(bg:{}, before_l1:{}, after_l1:{}, after_ba:{}, rec_list:{}'.format(self.bg,self.before_l1,self.after_l1,self.after_ba,str(self.rec_list))
class Test03:
    def __init__( self, bg, before, after, rec_list ):
        self.test = 3
        self.bg = bg
        self.before = before
        self.after = after
        self.rec_list = rec_list
    def __str__( self ):
        return 'Test03(bg:{}, before:{}, after:{}, rec_list:{}'.format(self.bg,self.before,self.after,str(self.rec_list))
#-------------------------------------END CLASSES--------------------------------
#-------------------------------------Make initial map with every single gen name----------
gen_map = {}
def make_gen_map( gen_file_name ): # creates map that has key of gen name and contains an empty list
    try:
        with open( gen_file_name ) as gen_names:
            for line in gen_names:
                # example of one line in list:
                # jss.gov.in    164.100.65.73       duodecimally2       True
                # domain        ip_address          gen_names           non_duplicated_server
                # [0]           [1]                 [2]                 [3]
                line = line.strip()
                line = line.split()
                gen_map[line[2].lower()] = [line[1]]
        print(str(gen_map))
    except Exception as e:
        print("*ERROR*: %s" % str(e))
#------------------------------------Combine result files for tests 1 - 3 ----------
def add_file( file_name, test_num ):
    try:
        with open ( file_name ) as test:
            for line in test:
                try:
                    line = line.strip()
                    my_list = line.split() # [0] = gen_name [1] = BG ... test specific
                    # ----------------TEST 1-------------------------------------
                    if test_num == "TEST1":
                        curr_list = gen_map[my_list[0]]
                        mini_list = []
                        for i in range(4, len(my_list)):
                            mini_list.append(my_list[i])
                        test1_obj = Test01( my_list[1], my_list[2], my_list[3], mini_list )
                        curr_list.append(test1_obj)
                        gen_map[my_list[0]] = curr_list
                    # ----------------TEST 2-------------------------------------
                    if test_num == "TEST2":
                        curr_list = gen_map[my_list[0]]
                        mini_list = []
                        for i in range(5, len(my_list)):
                            mini_list.append(my_list[i])
                        test2_obj = Test02( my_list[1], my_list[2], my_list[3], my_list[4], mini_list )
                        curr_list.append(test2_obj)
                        gen_map[my_list[0]] = curr_list
                    # ----------------TEST 3-------------------------------------
                    if test_num == "TEST3":
                        curr_list = gen_map[my_list[0]]
                        mini_list = []
                        for i in range(4, len(my_list)):
                            mini_list.append(my_list[i])
                        test3_obj = Test03( my_list[1], my_list[2], my_list[3], mini_list )
                        curr_list.append(test3_obj)
                        gen_map[my_list[0]] = curr_list

                except Exception as msg:
                    sys.stderr.write("*ERROR msg for %s*: %s\n" % (test_num, str(msg)))
    except Exception as e:
        print("*ERROR*: %s" % str(e))
# -------------------------- Compare queries of tests ------------------------------
def compare3( t01, t02, t03 ):
    if t01.rec_list == t02.rec_list == t03.rec_list:
        return True
    else:
        return False
def compare2( first_test, second_test ):
    if first_test.rec_list == second_test.rec_list:
        return True
    else:
        return False
# --------------------------- END comparison methods --------------------------------

#---------------------------------ANALYZE---------------------------------------
# Questions:
# How many did no BG for t01 - t03?
# How many had differing behavior for all 3 tests?
# How many did the same queries for each test no matter what?
# How many did the same queries for t01 and t03?
# How many did BG queries before the best TXT query for t01 and t03?
# How many did BG queries after the final one for all 3 tests?
def analyze( ):
    no_bg = 0
    no_validation = 0
    yes_validation = 0
    yes_bg = 0
    ipv4_num = 0
    ipv6_num = 0
    validated_all_3 = 0
    validated_2_tests = 0
    validated_1_test = 0
    all_3_same = 0
    all_different = 0
    tests_1_and_3_same = 0
    tests_2_and_3_same = 0
    tests_1_and_2_same = 0
    before_txt_for_1_and_3 = 0
    after_txt_for_1_and_3 = 0
    both_before_and_after_txt_1_and_3 = 0
    total = len(gen_map)
    for key in gen_map:
        try:
            result = ""
            result += key + " "
            log_list = gen_map[key]
            ip_sent = log_list.pop(0)
            if ":" in ip_sent:
                result += "sent_on_ipv6 "
                ipv6_num += 1
            else:
                result += "sent_on_ipv4 "
                ipv4_num += 1

            if len(log_list) == 0:
                result += "No_validation_at_all "
                no_validation += 1
                sys.stderr.write(result)
                sys.stderr.write("\n")
                continue
            else:
                yes_validation += 1

            # Look at overall BGness
            # How many did no BG for t01 - t03?
            bg_counter = 0
            for log in log_list:
                if log.bg != "NO_BG":
                    bg_counter += 1
            if bg_counter == 0:
                result += "NO_BG_for_any_test "
                no_bg += 1
                sys.stderr.write(result)
                sys.stderr.write("\n")
                continue
            else:
                result += "BG_for_" + str(bg_counter) + "_test(s) "
                yes_bg += 1

            # Query analysis between all three tests...did they send the same queries?
            # How many had differing behavior for all 3 tests?
            # How many did the same queries for each test no matter what?
            # How many did the same queries for t01 and t03?
            if len(log_list) == 3:
                result += "Validated_all_tests "
                validated_all_3 += 1
                if compare3(log_list[0], log_list[1], log_list[2]):
                    result += "Exact_same_t01_t02_t03 "
                    all_3_same += 1
                elif compare2(log_list[0], log_list[2]):
                    result += "Test_1_and_3_same "
                    tests_1_and_3_same += 1
                elif compare2(log_list[1], log_list[2]):
                    result += "Test_2_and_3_same "
                    tests_2_and_3_same += 1
                elif compare2(log_list[0], log_list[1]):
                    result += "Test_1_and_2_same "
                    tests_1_and_2_same += 1
                else:
                    result += "All_tests_DIFFERENT "
                    all_different += 1
            elif len(log_list) == 2:
                result += "Only_validated_2_tests "
                validated_2_tests += 1
                if compare2(log_list[0], log_list[1]):
                    result += "Test_" + str(log_list[0].test) + "_and_" + str(log_list[1].test) + "_same "
                    if log_list[0].test == 1 and log_list[1].test == 2:
                        tests_1_and_2_same += 1
                    elif log_list[0].test == 1 and log_list[1].test == 3:
                        tests_1_and_3_same += 1
                    elif log_list[0].test == 2 and log_list[1].test == 3:
                        tests_2_and_3_same += 1
                else:
                    result += "Test_" + str(log_list[0].test) + "_and_Test_" + str(log_list[1].test) + "_are_DIFFERENT "

            else:
                result += "Only_validated_1_test "
                validated_1_test += 1

            # How many did BG queries before the best TXT query for t01 and t03?
            # How many did BG queries after the final one for all 3 tests?
            before_1 = False
            after_1 = False
            before_3 = False
            after_3 = False
            for log in log_list:
                if log.bg == "BG":
                    if log.test == 1:
                        if log.before == "BEFORE":
                            before_1 = True
                        if log.after == "AFTER":
                            after_1 = True
                    elif log.test == 3:
                        if log.before == "BEFORE":
                            before_3 = True
                        if log.after == "AFTER":
                            after_3 = True
            if before_1 and before_3:
                result += "BG_before_txt_1_and_3 "
                before_txt_for_1_and_3 += 1
            if after_1 and after_3:
                result += "BG_after_txt_1_and_3 "
                after_txt_for_1_and_3 += 1
            if before_1 and before_3 and after_1 and after_3:
                both_before_and_after_txt_1_and_3 += 1

            sys.stderr.write(result)
            sys.stderr.write("\n")
        except Exception as e:
            sys.stderr.write("********* ERROR : %s*********" % str(e))




    sys.stderr.flush()
    sys.stdout.flush()

    # plot the results bruh
    # before_txt_for_1_and_3 = 0
    # after_txt_for_1_and_3 = 0
    num_list = [total, ipv4_num, ipv6_num, no_validation, yes_validation, yes_bg, no_bg,
                validated_all_3, validated_2_tests, validated_1_test,
                all_3_same, all_different, tests_1_and_2_same,
                tests_1_and_3_same, tests_2_and_3_same,
                before_txt_for_1_and_3, after_txt_for_1_and_3,
                both_before_and_after_txt_1_and_3]
    labels = ["Total_Tried", "sent_on_ipv4", "sent_on_ipv6",
                "No_validation_at_all", "Yes_validation", "Yes_BG", "NO_BG_for_any_test",
                "validated_all_3_tests", "validated_2_tests", "validated_1_test",
                "all_3_tests_the_same", "all_3_tests_different",
                "tests_1_and_2_same", "tests_1_and_3_same", "tests_2_and_3_same",
                "BG_before_txt_1_and_3", "BG_after_txt_1_and_3",
                "both_before_and_after_txt_1_and_3"]
    index = np.arange(len(num_list))
    fig = plt.figure(figsize=(15, 10))
    plt.bar(index, num_list, width=.6, color='#7EE9FF', edgecolor='black')
    plt.xlabel('Categories', fontsize=14)
    plt.ylabel('Out of all gen_names', fontsize=14)
    plt.xticks(index, labels, fontsize=8, rotation=70)
    plt.title('Analysis for Tests 1, 2, 3',fontsize=16)
    for a,b in zip(index, num_list):
            plt.text(a, b, str(b), fontdict=None, fontsize=8, horizontalalignment='center', verticalalignment='bottom')
    plt.gca().yaxis.set_major_formatter(PercentFormatter(total)) # turns y axis into percentage
    plt.tight_layout()
    plt.savefig('./matplot/results_1_2_3.eps', format='eps', dpi=1000)
    plt.show()
#-----------------------------------------END ANALYZE-------------------------


def main():
    # Command Line args: gen_name_file.txt t01_results.txt t02_results.txt t03_results.txt
    arg_list = sys.argv
    gen_file_name = arg_list[1]
    t01_file = arg_list[2]
    t02_file = arg_list[3]
    t03_file = arg_list[4]
    # make generated name map with gen names as the key
    make_gen_map(gen_file_name)
    add_file(t01_file, "TEST1")
    add_file(t02_file, "TEST2")
    add_file(t03_file, "TEST3")

    # --- print map objects ---
    for obj in gen_map:
        da_list = gen_map[obj]
        print(obj)
        for min in da_list:
            print("gen: %s - %s" % (obj, str(min)))

    analyze()



if __name__ == '__main__':
    main()
