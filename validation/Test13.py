from validation.TestBase import TestBase
from validation.state_objs.SuccessState import SuccessState
from validation.state_objs.StartState import StartState
from validation.state_objs.BaseState import BaseState
from validation.state_objs.FailureState import FailureState
from validation.state_objs.StateUtils import check_a
import validation.States as s


class Test13(TestBase):
    def __init__(self):
        TestBase.__init__(self, self.test_def)

    def do_testing(self, log_list):
        # call to super class
        return TestBase.check_testing(self, log_list)

    def test_def(self, log):
        if isinstance(self.state, StartState) and log.rec_queried == s.States.TXT:
            self.state = BaseState(log, self.get_test_result)
        elif isinstance(self.state, BaseState) and log.rec_queried == s.States.MX and log.level == "b":
            self.state = FailureState(log, self.get_test_result)
        elif isinstance(self.state, FailureState) and check_a(log.rec_queried):
            if log.level == "mail10":
                self.state = SuccessState(log, self.get_test_result)
            else:
                self.state = FailureState(log, self.get_test_result)

    def get_test_result(self, log, log_list):
        pass