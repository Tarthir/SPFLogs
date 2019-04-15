from abc import ABC, abstractmethod


# Creating dynamic states: https://www.python-course.eu/python3_classes_and_type.php
class SuperState(ABC):

    def __init__(self, state_name, log, get_result):
        self.name = state_name
        self.ending_log = log
        self.get_result_method = get_result

    def get_result(self, log_list):
        if self.get_result_method is not None:
            self.get_result_method(log_list, self.ending_log)  # TODO what parameters does this take? Does it matter?
        else:
            print("SuperState: No get Result method given, please give state objects get_result method(s)")
