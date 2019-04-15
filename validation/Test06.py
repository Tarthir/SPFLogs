from validation.TestBase import TestBase
from validation.States.BaseState import BaseState
from validation.States.SuccessState import SuccessState
from validation.States.StartState import StartState
from validation.States.FailureState import FailureState


class Test06(TestBase):

    def __init__(self):
        TestBase.__init__(self, self.test_def)

    def get_test_result(self):
        pass

    def do_testing(self, log_list):
        return TestBase.check_testing(self, log_list)

    def test_def(self, log):
        if isinstance(self.state, StartState) and log.rec_queried == "TXT":
            self.state = BaseState(log, None)
        elif log.rec_queried == "b" and isinstance(self.state,BaseState):
            self.state = SuccessState(log, None)
        elif isinstance(self.state, SuccessState) and log.rec_queried == "c":
            self.state = FailureState(log, None)
