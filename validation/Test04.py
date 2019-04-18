from validation.TestBase import TestBase
from validation.state_objs.StartState import StartState
from validation.state_objs.BaseState import BaseState
from validation.state_objs.StateUtils import get_class
from validation.state_objs.StateUtils import do_state_change
from validation.state_objs.StateUtils import check_a
import validation.States as s


class Test04(TestBase):
    def __init__(self):
        TestBase.__init__(self, self.test_def)
        self.dyn_classes = {"l1": get_class("l1", self.get_test_result), "l2": get_class("l2", self.get_test_result),
                            "l3": get_class("l3", self.get_test_result),
                            "b_to4_a": get_class("b_to4_a", self.get_test_result),
                            "p_l1": get_class("p_l1", self.get_test_result),
                            "p_l2": get_class("p_l2", self.get_test_result),
                            "parallel": get_class("parallel", self.get_test_result),
                            "maybe_serial": get_class("maybe_serial", self.get_test_result),
                            "delayed_parallel": get_class("delayed_parallel", self.get_test_result),
                            "serial": get_class("serial", self.get_test_result)}

    def do_testing(self, log_list):
        # call to super class
        return TestBase.check_testing(self, log_list)

    # https://github.com/byu-imaal/Tanner/blob/master/quartet_backup_sept07_2018/validation/post_swaks_parsing/scratch/definitions/t04.dot.png
    def test_def(self, log):
        if isinstance(self.state, StartState) and log.rec_queried == "TXT":
            self.state = BaseState(log, self.get_test_result)

        # check branches from base state
        if isinstance(self.state, BaseState):
            if log.level == "l1" and log.rec_queried == "TXT":
                self.state = do_state_change("l1", log, self.dyn_classes)
            elif log.level == "b" and check_a(log.rec_queried):
                self.state = do_state_change("b_to4_a", log, self.dyn_classes)
            elif log.level == "l2" and log.rec_queried == "TXT":
                self.state = do_state_change("l2", log, self.dyn_classes)
            elif  log.level == "l3" and log.rec_queried == "TXT":
                self.state = do_state_change("l3", log, self.dyn_classes)

        # check branches from l1
        elif self.state.name == "l1":
            if log.rec_queried == "TXT":
                if log.level == "l2":
                    self.state = do_state_change("l2", log, self.dyn_classes)
                elif log.level == "l3":
                    self.state = do_state_change("l3", log, self.dyn_classes)
            elif check_a(log.rec_queried) and log.level == "b_to4_a":
                self.state = do_state_change("b_to4_a", log, self.dyn_classes)

        # check branch from l3
        elif self.state.name == "l3" and log.level == "b" and check_a(log.rec_queried):
            self.state = do_state_change("serial", log, self.dyn_classes)  # Success

        # check branches from l2
        elif self.state.name == "l2" and log.rec_queried == "TXT":
            if log.level == "l3":
                self.state = do_state_change("l3", log, self.dyn_classes)
            elif log.level == "b":
                self.state = do_state_change("maybe_serial", log, self.dyn_classes)  # Success

        # check branch from maybe_Serial
        elif self.state.name == "maybe_serial" and log.level == "l3" and log.rec_queried == "TXT":
            self.state = do_state_change("delayed_parallel", log, self.dyn_classes)  # Success

        # check branch from b_to4_a
        elif self.state.name == "b_to4_a" and log.rec_queried == "TXT":
            if log.level == "l1":
                self.state = do_state_change("p_l1", log, self.dyn_classes)
            elif log.level == "l2":
                self.state = do_state_change("p_l2", log, self.dyn_classes)
            elif log.level == "l3":
                self.state = do_state_change("parallel", log, self.dyn_classes)  # Success

        # check branch from p_l1
        elif self.state.name == "p_l1" and log.rec_queried == "TXT":
            if log.rec_queried == "l2":
                self.state = do_state_change("p_l2", log, self.dyn_classes)
            elif log.level == "l3":
                self.state = do_state_change("parallel", log, self.dyn_classes)  # Success
        elif self.state.name == "p_l2" and log.level == "l3" and log.rec_queried == "TXT":
            self.state = do_state_change("parallel", log, self.dyn_classes)  # Success

    def get_test_result(self, log, log_list):
        return TestBase.get_test_result(self, log, log_list)





