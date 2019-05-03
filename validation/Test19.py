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
        self.ipv_method = "."
        self.which_Test = "t19"

    def do_testing(self, log_list):
        # call to super class
        print("\n")
        return TestBase.check_testing(self, log_list)

    def test_def(self, log):
        print(str(log))
        if isinstance(self.state, StartState) and "." in log.ip:
            self.state = do_state_change("to_ipv4", log, self.dyn_classes, self.get_test_result)
            self.sent_to = self.state.name
        elif isinstance(self.state, StartState) and ":" in log.ip:
            self.state = do_state_change("to_ipv6", log, self.dyn_classes, self.get_test_result)
            self.sent_to = self.state.name
        elif self.state.name == "to_ipv6" or self.state.name == "to_ipv4" or isinstance(self.state, FailureState):
            if log.rec_queried == "TXT" and self.ipv_method == ".":
                self.state = SuccessState(log, self.get_test_result)
            else:
                self.state = FailureState(log, self.get_test_result)
                # TODO include whether they looked up over ipv4/6 here. On top of "TXT". May need to change test 20 to be alone

    def get_test_result(self, log, log_list):
        return "{} Sent_to:{}".format(TestBase.get_test_result(self, log, log_list), self.sent_to)
