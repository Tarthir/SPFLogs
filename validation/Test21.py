from validation.TestBase import TestBase
from validation.state_objs.SuccessState import SuccessState
from validation.state_objs.FailureState import FailureState


class Test21(TestBase):
    def __init__(self):
        TestBase.__init__(self, self.test_def)
        self.timed_out = False

    def do_testing(self, log_list):
        first = log_list[0]
        last = log_list[len(log_list)-1]
        self.timed_out = (last.sec_from_1970 - first.sec_from_1970 > 20)
        if not self.timed_out:
            self.state = SuccessState(last, self.get_test_result)
        else:
            self.state = FailureState(last, self.get_test_result)
        self.state.get_final_result(log_list)


    def test_def(self, log):
        pass

    def get_test_result(self, log, log_list):
        return "{} >20:{}".format(TestBase.get_test_result(self, log, log_list), self.timed_out)
