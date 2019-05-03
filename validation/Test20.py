from validation.Test19 import Test19
from validation.TestBase import TestBase
from validation.state_objs.StartState import StartState


class Test20(TestBase):
    def __init__(self):
        TestBase.__init__(self, self.test_def)
        self.test19 = Test19()
        self.test19.state = StartState(None, self.get_test_result)
        self.test19.which_test_running = "t20"

    def do_testing(self, log_list):
        # call to super class
        return TestBase.check_testing(self, log_list)

    def test_def(self, log):
        # Reuse test 19 since it is pretty much the same thing
        self.test19.state = self.state
        self.test19.test_def(log)
        self.state = self.test19.state

    def get_test_result(self, log, log_list):
        self.state = StartState(None, self.get_test_result)
        return self.test19.get_test_result(log, log_list)
