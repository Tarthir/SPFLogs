from validation.TestBase import TestBase
from validation.States.StartState import StartState
from validation.States.BaseState import BaseState
from validation.States.SuccessState import SuccessState


class Test10(TestBase):
    def __init__(self):
        TestBase.__init__(self, self.test_def)
        self.all_five = {"b", "c", "d", "e", "f"}

    def do_testing(self, log_list):
        # call to super class
        return TestBase.check_testing(self, log_list)

    def test_def(self, log):
        if isinstance(self.state, StartState) and log.rec_queried == "TXT":
            self.state = BaseState(log, self.get_test_result)
        elif isinstance(self.state, BaseState):
            # TODO is this right? do we have to see each one or just 5 of any kind
            if log.rec_queried in self.all_five:
                self.all_five.remove(log.rec_queried)
            # if we have seen all five queries
            if len(self.all_five) == 0:
                self.state = SuccessState(log, self.get_test_result)

    def get_test_result(self, log, log_list):
        pass
