from validation.TestBase import TestBase
from validation.state_objs.FailureState import FailureState
from validation.state_objs.SuccessState import SuccessState


class Test18(TestBase):
    def __init__(self):
        TestBase.__init__(self, self.test_def)

    def do_testing(self, log_list):
        # call to super class
        return TestBase.check_testing(self, log_list)

    def test_def(self, log):
        # Success means they had the tcp flag
        if log.tcp == "T":
            self.state = SuccessState(log, self.get_test_result)
        # only fail if we have not already succeeded, just in case
        elif not isinstance(self.state, SuccessState):
            self.state = FailureState(log, self.get_test_result)

    def get_test_result(self, log, log_list):
        return "{} Tcp:{}".format(TestBase.get_test_result(self, log, log_list), log.tcp)
