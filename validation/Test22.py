from validation.TestBase import TestBase


class Test22(TestBase):
    def __init__(self):
        TestBase.__init__(self, self.test_def)

    def do_testing(self, log_list):
        # call to super class
        return TestBase.check_testing(self, log_list)

    def test_def(self, log):
        pass

    def get_test_result(self, log, log_list):
        pass