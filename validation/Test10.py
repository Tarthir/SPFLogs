from validation.TestBase import TestBase
from validation.state_objs.BaseState import BaseState
from validation.state_objs.StartState import StartState
from validation.state_objs.SuccessState import SuccessState


class Test10(TestBase):
    def __init__(self):
        TestBase.__init__(self, self.test_def)
        self.all_five = {"b", "c", "d", "e", "f"}
        self.succeeded = {}

    def do_testing(self, log_list):
        # call to super class
        return TestBase.check_testing(self, log_list)

    def test_def(self, log):
        if isinstance(self.state, StartState) and log.rec_queried == "TXT":
            self.state = BaseState(log, self.get_test_result)
        elif isinstance(self.state, BaseState):
            # TODO do we need to check for what rec they queried?
            if log.level in self.all_five: #and check_a(log.rec_queried):
                self.all_five.remove(log.level)
            # if we have seen all five queries
            if len(self.all_five) == 0:
                self.state = SuccessState(log, self.get_test_result)
                self.succeeded[log.generated_name] = True

    def get_test_result(self, log, log_list):
        return TestBase.get_test_result(self, log, log_list)
