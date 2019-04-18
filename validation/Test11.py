from validation.TestBase import TestBase
from validation.state_objs.StartState import StartState
from validation.state_objs.BaseState import BaseState
from validation.state_objs.FailureState import FailureState
from validation.state_objs.StateUtils import get_class
from validation.state_objs.StateUtils import do_state_change
from validation.state_objs.StateUtils import check_a
import validation.States as s


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
        if isinstance(self.state, StartState) and log.rec_queried == s.States.TXT:
            self.state = BaseState(log, self.get_test_result)

        elif isinstance(self.state, BaseState) and log.level in self.queries_types and check_a(log.rec_queried):
            self.queries_types.remove(log.level)
            self.state = do_state_change("lookup_1", log, self.dyn_classes)

        elif self.state.name == "lookup_1" and log.level in self.queries_types and check_a(log.rec_queried):
            self.queries_types.remove(log.level)
            self.state = do_state_change("lookup_2", log, self.dyn_classes)

        elif self.state.name == "lookup_2" and log.level in self.queries_types and check_a(log.rec_queried):
            self.state = FailureState(log, self.get_test_result)

    def get_test_result(self, log, log_list):
        pass
