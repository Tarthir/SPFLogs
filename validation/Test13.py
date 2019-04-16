from validation.TestBase import TestBase
from validation.States.SuccessState import SuccessState
from validation.States.StartState import StartState
from validation.States.BaseState import BaseState
from validation.States.FailureState import FailureState


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
            pass
            # TODO other states dynamically

    def get_test_result(self, log, log_list):
        pass