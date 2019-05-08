from validation.TestBase import TestBase
from validation.state_objs.BaseState import BaseState
from validation.state_objs.StartState import StartState
from validation.state_objs.StateUtils import check_a
from validation.state_objs.SuccessState import SuccessState


class Test10(TestBase):
    def __init__(self):
        TestBase.__init__(self, self.test_def)
        self.succeeded = {}

    def do_testing(self, log_list):
        # call to super class
        #print("\n")
        return TestBase.check_testing(self, log_list)

    def test_def(self, log):
        #print(str(log))
        if isinstance(self.state, StartState) and log.rec_queried == "TXT":
            self.state = BaseState(log, self.get_test_result)
        elif isinstance(self.state, BaseState) and check_a(log.rec_queried):
            if log.level == "e" or log.level == "f":
                self.state = SuccessState(log, self.get_test_result)
                self.succeeded[log.generated_name] = True

    def get_test_result(self, log, log_list):
        return TestBase.get_test_result(self, log, log_list)
