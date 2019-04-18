from validation.TestBase import TestBase
from validation.state_objs.SuccessState import SuccessState
from validation.state_objs.StartState import StartState
from validation.state_objs.FailureState import FailureState
from validation.state_objs.StateUtils import check_a
import validation.States as s


class Test08(TestBase):

    def __init__(self):
        TestBase.__init__(self, self.test_def)

    def get_test_result(self, log, log_list):
        pass

    def do_testing(self, log_list):
        return TestBase.check_testing(self, log_list)

    def test_def(self, log):
        if isinstance(self.state, StartState) and log.rec_queried == s.States.TXT:
            self.state = SuccessState(log, self.get_test_result)
        elif isinstance(self.state, SuccessState) and log.level == "b" and log.rec_queried == s.States.TXT:
            self.state = FailureState(log, self.get_test_result)
