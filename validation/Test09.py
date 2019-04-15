from validation.TestBase import TestBase
from validation.States.SuccessState import SuccessState
from validation.States.StartState import StartState
from validation.States.BaseState import BaseState
from validation.States.FailureState import FailureState


# meaning lets have a dict for each test, we can add states as needed?
class Test09(TestBase):

    def get_test_result(self):
        pass

    def do_testing(self, log_list):
        pass

    def test_def(self, log):
        if isinstance(self.state, StartState) and log.level == "TXT":
            self.state = BaseState(log, None)
        elif (isinstance(self.state, BaseState) or isinstance(self.state,SuccessState)) and log.level != "l10":
            self.state = FailureState(log, None)
        elif isinstance(self.state, FailureState) and log.level == "l10":
            self.state = SuccessState(log, None)

