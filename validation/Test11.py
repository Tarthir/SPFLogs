from validation.TestBase import TestBase
from validation.States.StartState import StartState
from validation.States.BaseState import BaseState
from validation.States.SuccessState import SuccessState
from validation.States.FailureState import FailureState

class Test11(TestBase):
    def __init__(self):
        TestBase.__init__(self, self.test_def)
        self.queries = {"b", "c", "d", "e", "f"}

    def do_testing(self, log_list):
        # call to super class
        return TestBase.check_testing(self, log_list)

    def test_def(self, log):
        if isinstance(self.state, StartState) and log.rec_queried == "TXT":
            self.state = BaseState(log, self.get_test_result)
        elif isinstance(self.state, BaseState) and log.level in self.queries:
            pass
        # TODO lookup1 state
        # TODO elif we get to lookup2 state, then success, remove that query letter from self.queries

        elif isinstance(self.state, SuccessState) and log.level in self.queries:
            self.state = FailureState(log, self.get_test_result)

    def get_test_result(self, log, log_list):
        pass