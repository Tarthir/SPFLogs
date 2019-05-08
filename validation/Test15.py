from validation.TestBase import TestBase
from validation.state_objs.FailureState import FailureState
from validation.state_objs.StartState import StartState
from validation.state_objs.StateUtils import check_a
from validation.state_objs.SuccessState import SuccessState


class Test15(TestBase):
    def __init__(self):
        TestBase.__init__(self, self.test_def)

    def do_testing(self, log_list):
        # call to super class
        #print("\n")
        return TestBase.check_testing(self, log_list)

    def test_def(self, log):
        #print(str(log))
        if isinstance(self.state, StartState) and log.rec_queried == "TXT" and log.level is None:
            self.state = SuccessState(log, self.get_test_result)
        elif check_a(log.rec_queried) and log.level == "b":
            self.state = FailureState(log, self.get_test_result)

    def get_test_result(self, log, log_list):
        return TestBase.get_test_result(self, log, log_list)
