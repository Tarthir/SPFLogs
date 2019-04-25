from validation.TestBase import TestBase
from validation.state_objs.StartState import StartState
from validation.state_objs.SuccessState import SuccessState
from validation.state_objs.FailureState import FailureState
from validation.state_objs.StateUtils import get_class
from validation.state_objs.StateUtils import do_state_change


class Test19(TestBase):
    def __init__(self):
        TestBase.__init__(self, self.test_def)
        self.dyn_classes = {"to_ipv4": get_class("to_ipv4"),
                            "to_ipv6": get_class("to_ipv6")}
        self.sent_to = "N/A"

    def do_testing(self, log_list):
        # call to super class
        return TestBase.check_testing(self, log_list)

    def test_def(self, log):
        if isinstance(self.state, StartState) and "." in log.ip:
            self.state = do_state_change("to_ipv4", log, self.dyn_classes, self.get_test_result)
            self.sent_to = self.state.name
        elif isinstance(self.state, StartState) and ":" in log.ip:
            self.state = do_state_change("to_ipv6", log, self.dyn_classes, self.get_test_result)
            self.sent_to = self.state.name
        elif self.state.name == "to_ipv6" or self.state.name == "to_ipv4" or isinstance(self.state, FailureState):
            if log.rec_queried == "TXT":
                self.state = SuccessState(log, self.get_test_result)
            else:
                self.state = FailureState(log, self.get_test_result)

    def get_test_result(self, log, log_list):
        return "{} Sent_to:{}".format(TestBase.get_test_result(self, log, log_list), self.sent_to)
