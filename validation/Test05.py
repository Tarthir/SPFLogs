from validation.state_objs.BaseState import BaseState
from validation.state_objs.SuccessState import SuccessState
from validation.state_objs.StartState import StartState
from validation.TestBase import TestBase
from validation.state_objs.StateUtils import check_a
from validation.state_objs.StateUtils import get_class
from validation.state_objs.StateUtils import do_state_change


class Test05(TestBase):

    def __init__(self):
        TestBase.__init__(self, self.test_def)
        self.dyn_classes = {"l1": get_class("l1")}

    def get_test_result(self, log, log_list):
        return TestBase.get_test_result(self, log, log_list)

    def do_testing(self, log_list):
        # call to super class
        print("\n")
        return TestBase.check_testing(self, log_list)

    def test_def(self, log):
        print(str(log))
        # b means we have succeeded, all other queries are fine, no need to check
        if isinstance(self.state, StartState) and log.rec_queried == "TXT" and log.level == None:
            self.state = BaseState(log, self.get_test_result)
        elif isinstance(self.state, BaseState) and log.level == "l1" and log.rec_queried == "TXT":
            self.state = do_state_change("l1", log, self.dyn_classes, self.get_test_result)
        elif self.state.name == "l1" and log.level == "b" and check_a(log.rec_queried):
            self.state = SuccessState(log, self.get_test_result)
