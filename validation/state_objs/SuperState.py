import sys
from abc import ABC, abstractmethod


# Creating dynamic states: https://www.python-course.eu/python3_classes_and_type.php
class SuperState(ABC):

    def __init__(self, state_name, log, get_result):
        self.name = state_name
        self.ending_log = log
        self.get_result_method = get_result

    def get_final_result(self, log_list):
        if self.get_result_method is not None:
            file_name = "validation_results/{}_results.txt".format(self.ending_log.test_name)
            with open(file_name, "a+") as f:
                try:
                    res = self.get_result_method(self.ending_log, log_list) #TODO getting error here when running on server??
                    if res is not None:
                        f.write(res)
                        f.flush()
                except TypeError as err: # TODO get rid of this
                    sys.stderr.write("{} - {} - {}".format(str(err), self.get_result_method, self.ending_log.test_name))
        else:
            sys.stderr.write("SuperState: No get Result method given, please give state objects get_result method(s)\n")

