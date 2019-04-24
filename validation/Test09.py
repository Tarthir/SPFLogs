from validation.TestBase import TestBase
from validation.state_objs.SuccessState import SuccessState
from validation.state_objs.StartState import StartState
from validation.state_objs.BaseState import BaseState
from validation.state_objs.FailureState import FailureState


# meaning lets have a dict for each test, we can add states as needed?
class Test09(TestBase):

    def __init__(self):
        TestBase.__init__(self, self.test_def)

    def get_test_result(self, log, log_list):
        return TestBase.get_test_result(self, log, log_list)

    def do_testing(self, log_list):
        return TestBase.check_testing(self, log_list)

    def test_def(self, log):
        if isinstance(self.state, StartState) and log.rec_queried == "TXT":
            self.state = BaseState(log, self.get_test_result)
        elif (isinstance(self.state, BaseState) or isinstance(self.state, SuccessState)) and log.level != "l10" \
                and log.rec_queried == "TXT":
            self.state = FailureState(log, self.get_test_result)  # logic flow lets us know when it stopped
        elif isinstance(self.state, FailureState) and log.level == "l10" and log.rec_queried == "TXT":
            self.state = SuccessState(log, self.get_test_result)
