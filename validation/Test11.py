from validation.TestBase import TestBase
from validation.States.StartState import StartState
from validation.States.BaseState import BaseState
from validation.States.SuccessState import SuccessState
from validation.States.FailureState import FailureState
from validation.States.StateUtils import get_class
from validation.States.StateUtils import do_state_change


class Test11(TestBase):
    def __init__(self):
        TestBase.__init__(self, self.test_def)
        self.queries_types = {"b", "c", "d", "e", "f"}
        self.dyn_classes = {"lookup_1": get_class("lookup_1", self.get_test_result),
                            "lookup_2": get_class("lookup_2", self.get_test_result)}

    def do_testing(self, log_list):
        # call to super class
        return TestBase.check_testing(self, log_list)

    def test_def(self, log):
        if isinstance(self.state, StartState) and log.rec_queried == "TXT":
            self.state = BaseState(log, self.get_test_result)

        elif isinstance(self.state, BaseState) and log.level in self.queries_types and log.rec_queried == "A":
            self.queries_types.remove(log.level)
            self.state = do_state_change("lookup_1", log, self.dyn_classes)

        elif self.state.name == "lookup_1" and log.level in self.queries_types and log.rec_queried == "A":
            self.queries_types.remove(log.level)
            self.state = do_state_change("lookup_2", log, self.dyn_classes)

        elif self.state.name == "lookup_2" and log.level in self.queries_types and log.rec_queried == "A":
            self.state = FailureState(log, self.get_test_result)

    def get_test_result(self, log, log_list):
        pass
