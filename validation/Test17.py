from validation.TestBase import TestBase
from validation.state_objs.BaseState import BaseState
from validation.state_objs.StartState import StartState
from validation.state_objs.StateUtils import check_a
from validation.state_objs.StateUtils import do_state_change
from validation.state_objs.StateUtils import get_class


class Test17(TestBase):
    def __init__(self):
        TestBase.__init__(self, self.test_def)
        self.dyn_classes = {"l1": get_class("l1"),
                            "l2": get_class("l2"),
                            "l3": get_class("l3"),
                            "l4": get_class("l4"),
                            "l5": get_class("l5")
                            }

    def do_testing(self, log_list):
        # call to super class
        print("\n")
        self.counter = 0
        return TestBase.check_testing(self, log_list)

    def test_def(self, log):
        print(str(log))
        if isinstance(self.state, StartState) and log.level is None and log.rec_queried == "TXT":
            self.state = BaseState(log, self.get_test_result)
        elif log.level == "b" and check_a(log.rec_queried):
            self.counter += 1
        else:
            self.state = do_state_change(log.level, log, self.dyn_classes, self.get_test_result)

    def get_test_result(self, log, log_list):
        cache = ""
        if self.counter == 1:
            cache = "Yes_" + str(self.counter)
        else:
            cache = "No_" + str(self.counter)
        return "{} Caching:{}".format(TestBase.get_test_result(self, log, log_list), cache)
