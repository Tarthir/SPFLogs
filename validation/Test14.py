from validation.TestBase import TestBase
from validation.state_objs.SuccessState import SuccessState
from validation.state_objs.StartState import StartState
from validation.state_objs.BaseState import BaseState
from validation.state_objs.FailureState import FailureState
from validation.state_objs.StateUtils import check_a
from validation.state_objs.StateUtils import do_state_change
from validation.state_objs.StateUtils import get_class


class Test14(TestBase):
    def __init__(self):
        TestBase.__init__(self, self.test_def)
        self.dyn_classes = {"b_A": get_class("b_A"), "c_A": get_class("c_A"), "both": get_class("both")}

    def do_testing(self, log_list):
        # call to super class
        print("\n")
        self.holder = {"b", "c"}
        return TestBase.check_testing(self, log_list)

    def test_def(self, log):
        print(str(log))
        if isinstance(self.state, StartState) and log.rec_queried == "TXT" and log.level == None:
            self.state = BaseState(log, self.get_test_result)
        elif check_a(log.rec_queried):
            if log.level == "b":
                if log.level in self.holder:
                    self.holder.remove(log.level)
                self.state = do_state_change("b_A", log, self.dyn_classes, self.get_test_result)
            elif log.level == "c":
                if log.level in self.holder:
                    self.holder.remove(log.level)
                self.state = do_state_change("c_A", log, self.dyn_classes, self.get_test_result)
        if len(self.holder) == 0:
            self.state = do_state_change("both", log, self.dyn_classes, self.get_test_result)
    def get_test_result(self, log, log_list):
        return TestBase.get_test_result(self, log, log_list)
