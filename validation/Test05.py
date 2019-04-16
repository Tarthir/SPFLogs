from validation.States.BaseState import BaseState
from validation.States.SuccessState import SuccessState
from validation.States.StartState import StartState
from validation.TestBase import TestBase


class Test05(TestBase):

    def __init__(self):
        TestBase.__init__(self, self.test_def)
        
    def get_test_result(self, log, log_list):
        pass

    def do_testing(self, log_list):
        # call to super class
        return TestBase.check_testing(self, log_list)

    def test_def(self, log):
        # b means we have succeeded, all other queries are fine, no need to check
        if isinstance(self.state, StartState) and log.rec_queried == "TXT":
            self.state = BaseState(log, self.get_test_result)
        elif isinstance(self.state, BaseState) and log.level == "b" and (log.rec_queried == "A" or log.rec_queried == "AAAA"):
            self.state = SuccessState(log, self.get_test_result)
            # TODO queries can come out of order

