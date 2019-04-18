from validation.state_objs.BaseState import BaseState
from validation.state_objs.SuccessState import SuccessState
from validation.state_objs.StartState import StartState
from validation.TestBase import TestBase
from validation.state_objs.StateUtils import check_a
import validation.States as s


class Test05(TestBase):

    def __init__(self):
        TestBase.__init__(self, self.test_def)
        
    def get_test_result(self, log, log_list):
        return TestBase.get_test_result(self, log, log_list)

    def do_testing(self, log_list):
        # call to super class
        return TestBase.check_testing(self, log_list)

    def test_def(self, log):
        # b means we have succeeded, all other queries are fine, no need to check
        if isinstance(self.state, StartState) and log.rec_queried == "TXT":
            self.state = BaseState(log, self.get_test_result)
        elif isinstance(self.state, BaseState) and log.level == "b" and (check_a(log.rec_queried) or check_a(log.rec_queried)):
            self.state = SuccessState(log, self.get_test_result)
            # TODO queries can come out of order

