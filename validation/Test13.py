from validation.TestBase import TestBase
from validation.state_objs.SuccessState import SuccessState
from validation.state_objs.StartState import StartState
from validation.state_objs.BaseState import BaseState
from validation.state_objs.FailureState import FailureState
from validation.state_objs.StateUtils import check_a
from validation.state_objs.StateUtils import do_state_change
from validation.state_objs.StateUtils import get_class
import math


class Test13(TestBase):
    def __init__(self):
        TestBase.__init__(self, self.test_def)
        self.counter = 0
        self.dyn_classes = {"mail01": get_class("mail01"), "mail02": get_class("mail02"), "mail03": get_class("mail03"),
                            "mail04": get_class("mail04"), "mail05": get_class("mail05"), "mail06": get_class("mail06"),
                            "mail07": get_class("mail07"), "mail08": get_class("mail08"), "mail09": get_class("mail09"),
                            "mail10": get_class("mail10"), "mail11": get_class("mail11"), "mail12": get_class("mail12"),
                            "mail13": get_class("mail13"), "mail14": get_class("mail14"), "mail15": get_class("mail15"),
                            "mail16": get_class("mail16"), "mail17": get_class("mail17"), "mail18": get_class("mail18"),
                            "mail19": get_class("mail19"), "mail20": get_class("mail20"), "mail21": get_class("mail21"),
                            "mail22": get_class("mail22"), "under_10": get_class("under_10"),
                            "at_10": get_class("at_10"), "over_10": get_class("over_10"),
                            "b_mx": get_class("b_mx")}

    def do_testing(self, log_list):
        # call to super class
        #print("\n")
        self.counter = 0
        self.holder = set()
        return TestBase.check_testing(self, log_list)

    def test_def(self, log):
        #print(str(log))
        if log.level is not None:
            #print(log.level[:-2])
            if log.level[:-2] == "mail":
                if log.level in self.holder:
                    pass
                else:
                    self.holder.add(log.level)
                    self.counter += 1
                    if self.counter < 10:
                        self.state = do_state_change("under_10", log, self.dyn_classes, self.get_test_result)
                    elif self.counter == 10:
                        self.state = do_state_change("at_10", log, self.dyn_classes, self.get_test_result)
                    elif self.counter > 10:
                        self.state = do_state_change("over_10", log, self.dyn_classes, self.get_test_result)
                    else:
                        self.state = do_state_change(log.level, log, self.dyn_classes, self.get_test_result)
            elif log.level == "b" and log.rec_queried == "MX":
                self.state = do_state_change("b_mx", log, self.dyn_classes, self.get_test_result)

        elif isinstance(self.state, StartState) and log.rec_queried == "TXT" and log.level == None:
            self.state = BaseState(log, self.get_test_result)

        #print("class levels: %s" % class_level)



        #
        # if isinstance(self.state, StartState) and log.rec_queried == "TXT":
        #     self.state = BaseState(log, self.get_test_result)
        # elif isinstance(self.state, BaseState) and log.rec_queried == "MX" and log.level == "b":
        #     self.state = FailureState(log, self.get_test_result)
        # elif isinstance(self.state, FailureState) and check_a(log.rec_queried):
        #     if log.level == "mail10":
        #         self.state = SuccessState(log, self.get_test_result)
        #     else:
        #         self.state = FailureState(log, self.get_test_result)
        # elif isinstance(self.state, SuccessState):  # if they keep querying after mail10
        #     self.state = FailureState(log, self.get_test_result)

    def get_test_result(self, log, log_list):
        return TestBase.get_test_result(self, log, log_list)
