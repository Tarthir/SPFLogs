from validation.state_objs.FailureState import FailureState
from validation.state_objs.SuccessState import SuccessState
from validation.state_objs.StartState import StartState
from validation.TestBase import TestBase
from validation.state_objs.StateUtils import check_a


class Test17(TestBase):
    def __init__(self):
        TestBase.__init__(self, self.test_def)

    def do_testing(self, log_list):
        # call to super class
        return TestBase.check_testing(self, log_list)

    def test_def(self, log):
        if isinstance(self.state, StartState) and log.level == "b" and check_a(log.rec_queried):
            self.state = SuccessState(log, self.get_test_result)
        elif isinstance(self.state, SuccessState) and log.level == "b" and check_a(log.rec_queried):
            self.state = FailureState(log, self.get_test_result)
        elif isinstance(self.state, FailureState):
            self.state = FailureState(log, self.get_test_result)

    def get_test_result(self, log, log_list):
        cache = ""
        if isinstance(self.state, SuccessState):
            cache = "Yes"
        else:
            cache = "No"
        return "{} Caching:{}".format(TestBase.get_test_result(self, log, log_list), cache)
