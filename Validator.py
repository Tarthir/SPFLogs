from log_reading import TestsHolder as tests
from validation import Test02, Test06, Test13, Test17, Test08, Test12, Test14, Test19, Test21, Test04, Test03, Test10, \
    Test18, Test16, Test22, Test11, Test05, Test07, Test09, Test01, Test20, Test15
import sys
import os
#  This script is in charge of checking to see how far in the validation process each email server got for
# each particular test
method_name = "check_testing"
validation_testing_dict = {#"t01": Test01.Test01(None), "t02": Test02.Test02(None), "t03": Test03.Test03(None),
                           "t04": Test04.Test04(), "t05": Test05.Test05(), "t06": Test06.Test06(),
                           "t07": Test07.Test07(), "t08": Test08.Test08(), "t09": Test09.Test09(),
                           "t10": Test10.Test10(), "t11": Test11.Test11(), "t12": Test12.Test12(),
                           "t13": Test13.Test13(), "t14": Test14.Test14(), "t15": Test15.Test15(),
                           "t16": Test16.Test16(), "t17": Test17.Test17(), "t18": Test18.Test18(),
                           "t19": Test19.Test19(), "t20": Test20.Test20(), "t21": Test21.Test21(),
                           "t22": Test22.Test22()}

holder = tests.TestsHolder()
print("Time To Validate...\n\nLoading the data...")
dir_path = os.path.dirname(os.path.realpath(__file__))
holder.load(dir_path)  # load up all the data

if not holder.all_tests:
    print("No file was loaded! Exiting...")
    exit(-1)

print("Entering Validation loop...\n")

for key in holder.all_tests.keys():
    logs = holder.all_tests[key]
    test_num = key.split("_")[0]
    try:
        validation_testing_dict[test_num].do_testing(logs)
    except KeyError as err:
        sys.stderr.write("Validating KeyError with: %s\n" % str(err))

# TODO tests t01-t03 have runtime errors, also checking agaisnt the enum will cause isssues