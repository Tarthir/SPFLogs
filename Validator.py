import os
import sys

from RemoveFiles import removeValidationFiles
from log_reading import TestsHolder as tests
from validation import Test06, Test08, Test19, Test18, Test11, Test05, Test07

#  This script is in charge of checking to see how far in the validation process each email server got for
# each particular test
method_name = "check_testing"
validation_testing_dict = {#"t01": Test01.Test01(None),
                            #"t02": Test02.Test02(None),
                            #"t03": Test03.Test03(None),
                            #"t04": Test04.Test04(),
                            #"t05": Test05.Test05(),
                            #"t06": Test06.Test06(), # error with b...TXT and b...A
                            #"t07": Test07.Test07(),
                            #"t08": Test08.Test08(),
                            #"t09": Test09.Test09(),
                            #"t10": Test10.Test10(),
                            #"t11": Test11.Test11(),
                            #"t12": Test12.Test12(),
                            #"t13": Test13.Test13(),
                            #"t14": Test14.Test14(),
                            #"t15": Test15.Test15(),
                            #"t16": Test16.Test16(),
                            #"t17": Test17.Test17(),
                            #"t18": Test18.Test18(),
                            "t19": Test19.Test19(),
                            #"t20": Test20.Test20(),
                            #"t21": Test21.Test21(),
                            #"t22": Test22.Test22()
                           }
dependent_val_tests = {"t05": Test05.Test05(), "t06": Test06.Test06(),
                       "t07": Test07.Test07(), "t08": Test08.Test08(),
                       "t11": Test11.Test11(), "t18": Test18.Test18()}
removeValidationFiles()  # removes all old result files in the validation_results directory
holder = tests.TestsHolder()
print("Time To Validate...\n\nLoading the data...")
dir_path = os.path.dirname(os.path.realpath(__file__))

# go through every all_logs file
for f in holder.get_log_files(dir_path + "\\data\\"):
    holder.load(f)  # load up all the data

    if not holder.all_tests:
        print("No file was loaded, Or it was empty! Exiting...")
        exit(-1)
    print("Entering Validation loop...\n")
    # sorting ensures that tests run from 1-22
    for key in sorted(holder.all_tests.keys()):
        logs = holder.all_tests[key]
        test_num = key.split("_")[0]
        gen_name = key.split("_")[1]
        try:
            # 5/6/7/8 dependent on 4
            if test_num == "t05" or test_num == "t06" or test_num == "t07" or test_num == "t08":
                if gen_name in validation_testing_dict["t04"].is_serial:
                    dependent_val_tests[test_num].do_testing(logs)
            # 11/18 dependent on 10
            elif test_num == "t11" or test_num == "t18":
                if gen_name in validation_testing_dict["t10"].succeeded:
                    dependent_val_tests[test_num].do_testing(logs)
            else:
                validation_testing_dict[test_num].do_testing(logs)

        except KeyError as err:
            sys.stderr.write("Validating KeyError with: %s\n" % str(err))

print("Done Validating\n")
