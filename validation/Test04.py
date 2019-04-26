from validation.TestBase import TestBase
from validation.state_objs.BaseState import BaseState
from validation.state_objs.StartState import StartState
from validation.state_objs.StateUtils import check_a
from validation.state_objs.StateUtils import do_state_change
from validation.state_objs.StateUtils import get_class


class Test04(TestBase):
    def __init__(self):
        TestBase.__init__(self, self.test_def)
        self.dyn_classes = {"l1": get_class("l1"), "l2": get_class("l2"),
                            "l3": get_class("l3"),
                            "b_t04_a": get_class("b_t04_a"),
                            "p_l1": get_class("p_l1"),
                            "p_l2": get_class("p_l2"),
                            "parallel": get_class("parallel"),
                            "maybe_serial": get_class("maybe_serial"),
                            "delayed_parallel": get_class("delayed_parallel"),
                            "serial": get_class("serial")}

    def do_testing(self, log_list):
        # call to super class
        return TestBase.check_testing(self, log_list)

    # https://github.com/byu-imaal/Tanner/blob/master/quartet_backup_sept07_2018/validation/post_swaks_parsing/scratch/definitions/t04.dot.png
    def test_def(self, log):
        if isinstance(self.state, StartState) and log.rec_queried == "TXT" and log.level is None:
            self.state = BaseState(log, self.get_test_result)

        # check branches from base state
        if isinstance(self.state, BaseState) or isinstance(self.state, StartState):
            if log.level == "l1" and log.rec_queried == "TXT":
                self.state = do_state_change("l1", log, self.dyn_classes, self.get_test_result)
            elif log.level == "b" and check_a(log.rec_queried):
                self.state = do_state_change("b_t04_a", log, self.dyn_classes, self.get_test_result)
            elif log.level == "l2" and log.rec_queried == "TXT":
                self.state = do_state_change("l2", log, self.dyn_classes, self.get_test_result)
            elif  log.level == "l3" and log.rec_queried == "TXT":
                self.state = do_state_change("l3", log, self.dyn_classes, self.get_test_result)

        # check branches from l1
        elif self.state.name == "l1":
            if log.rec_queried == "TXT":
                if log.level == "l2":
                    self.state = do_state_change("l2", log, self.dyn_classes, self.get_test_result)
                elif log.level == "l3":
                    self.state = do_state_change("l3", log, self.dyn_classes, self.get_test_result)
            elif check_a(log.rec_queried) and log.level == "b":
                self.state = do_state_change("b_t04_a", log, self.dyn_classes, self.get_test_result)

        # check branch from l3
        elif self.state.name == "l3" and log.level == "b" and check_a(log.rec_queried):
            self.state = do_state_change("serial", log, self.dyn_classes, self.get_test_result)  # Success

        # check branches from l2
        elif self.state.name == "l2":
            if log.level == "l3" and log.rec_queried == "TXT":
                self.state = do_state_change("l3", log, self.dyn_classes, self.get_test_result)
            elif log.level == "b" and check_a(log.rec_queried):
                self.state = do_state_change("maybe_serial", log, self.dyn_classes, self.get_test_result)  # Success

        # check branch from maybe_Serial
        elif self.state.name == "maybe_serial" and log.level == "l3" and log.rec_queried == "TXT":
            self.state = do_state_change("delayed_parallel", log, self.dyn_classes, self.get_test_result)  # Success

        # check branch from b_t04_a
        elif self.state.name == "b_t04_a" and log.rec_queried == "TXT":
            if log.level == "l1":
                self.state = do_state_change("p_l1", log, self.dyn_classes, self.get_test_result)
            elif log.level == "l2":
                self.state = do_state_change("p_l2", log, self.dyn_classes, self.get_test_result)
            elif log.level == "l3":
                self.state = do_state_change("parallel", log, self.dyn_classes, self.get_test_result)  # Success

        # check branch from p_l1
        elif self.state.name == "p_l1" and log.rec_queried == "TXT":
            if log.rec_queried == "l2":
                self.state = do_state_change("p_l2", log, self.dyn_classes, self.get_test_result)
            elif log.level == "l3":
                self.state = do_state_change("parallel", log, self.dyn_classes, self.get_test_result)  # Success
        elif self.state.name == "p_l2" and log.level == "l3" and log.rec_queried == "TXT":
            self.state = do_state_change("parallel", log, self.dyn_classes, self.get_test_result)  # Success

    def get_test_result(self, log, log_list):
        return TestBase.get_test_result(self, log, log_list)





