from abc import ABC, abstractmethod


# Creating dynamic states: https://www.python-course.eu/python3_classes_and_type.php
class SuperState(ABC):

    def __init__(self, state_name, log, get_result):
        self.name = state_name
        self.ending_log = log
        self.get_result_method = get_result

    def get_final_result(self, log_list):
        if self.get_result_method is not None:
            self.get_result_method(log_list, self.ending_log)
        else:
            print("SuperState: No get Result method given, please give state objects get_result method(s)")


# https://stackoverflow.com/questions/15247075/how-can-i-dynamically-create-derived-classes-from-a-base-class
def ClassFactory(name, argnames, BaseClass=SuperState):
    def __init__(self, **kwargs):
        vals = []
        for key, value in kwargs.items():
            # here, the argnames variable is the one passed to the
            # ClassFactory call
            if key not in argnames:
                raise TypeError("Argument %s not valid for %s"
                    % (key, self.__class__.__name__))
            setattr(self, key, value)
            vals.append(value)
        BaseClass.__init__(self, vals[0], vals[1], vals[2] )
    newclass = type(name, (BaseClass,),{"__init__": __init__})
    return newclass