from validation.TestBase import TestBase
from validation.state_objs.BaseState import BaseState
from validation.state_objs.SuccessState import SuccessState
from validation.state_objs.StartState import StartState
from validation.state_objs.FailureState import FailureState
from validation.state_objs.StateUtils import check_a


class Test06(TestBase):

    def __init__(self):
        TestBase.__init__(self, self.test_def)

    def get_test_result(self, log, log_list):
        return TestBase.get_test_result(self, log, log_list)

    def do_testing(self, log_list):
        #print("\n")
        return TestBase.check_testing(self, log_list)

    def test_def(self, log):
        #print(str(log))
        if isinstance(self.state, StartState) and log.rec_queried == "TXT":
            self.state = BaseState(log, self.get_test_result)
        elif log.level == "b" and isinstance(self.state, BaseState) and check_a(log.rec_queried):
            self.state = SuccessState(log, self.get_test_result)
        elif isinstance(self.state, SuccessState) and log.level == "c" and check_a(log.rec_queried):
            self.state = FailureState(log, self.get_test_result)
