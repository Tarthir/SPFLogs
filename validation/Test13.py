from validation.TestBase import TestBase
from validation.States.SuccessState import SuccessState
from validation.States.StartState import StartState
from validation.States.BaseState import BaseState
from validation.States.FailureState import FailureState
from validation.States.StateUtils import get_class

class Test13(TestBase):
    def __init__(self):
        TestBase.__init__(self, self.test_def)

    def do_testing(self, log_list):
        # call to super class
        return TestBase.check_testing(self, log_list)

    def test_def(self, log):
        if isinstance(self.state, StartState) and log.rec_queried == "TXT":
            self.state = BaseState(log, self.get_test_result)
        elif isinstance(self.state, BaseState) and log.rec_queried == "MX" and log.level == "b":
            self.state = FailureState(log, self.get_test_result)
        elif isinstance(self.state, FailureState) and log.rec_queried == "A":
            if log.level == "mail10":
                self.state = SuccessState(log, self.get_test_result)
            else:
                self.state = FailureState(log, self.get_test_result)

    def get_test_result(self, log, log_list):
        pass