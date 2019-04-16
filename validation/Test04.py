import validation.TestBase as BaseClass
from validation.TestBase import TestBase
from validation.States.SuccessState import SuccessState
from validation.States.StartState import StartState
from validation.States.BaseState import BaseState
from validation.States.FailureState import FailureState
from validation.States.SuperState import ClassFactory


class Test04(TestBase):
    def __init__(self):
        TestBase.__init__(self, self.test_def)
        self.dyn_classes = {"l1": self.get_class("l1"), "l2": self.get_class("l2"),
                            "l3": self.get_class("l3"), "b_to4_a": self.get_class("b_to4_a"),
                            "p_l1": self.get_class("p_l1"), "p_l2": self.get_class("p_l2"),
                            "parallel": self.get_class("parallel"), "maybe_serial": self.get_class("maybe_serial"),
                            "delayed_parallel": self.get_class("delayed_parallel"), "serial": self.get_class("serial")}

    def do_testing(self, log_list):
        # call to super class
        return TestBase.check_testing(self, log_list)

    # https://github.com/byu-imaal/Tanner/blob/master/quartet_backup_sept07_2018/validation/post_swaks_parsing/scratch/definitions/t04.dot.png
    def test_def(self, log):

        if isinstance(self.state, StartState) and log.rec_queried == "TXT":
            self.state = BaseState(log, self.get_test_result)

        elif isinstance(self.state, BaseState) and log.level == "l1" and log.rec_queried == "TXT":
            self.do_state_change("l1", log)
        elif isinstance(self.state, BaseState) and log.level == "b" and log.rec_queried == "A":
            self.do_state_change("b_to4_a", log)
        elif isinstance(self.state, BaseState) and log.level == "l2" and log.rec_queried == "TXT":
            self.do_state_change("l2", log)
        elif isinstance(self.state, BaseState) and log.level == "l3" and log.rec_queried == "TXT":
            self.do_state_change("l3", log)

        elif self.state.name == "l1":
            if log.level == "l2" and log.rec_queried == "TXT":
                self.do_state_change("l2", log)
            elif log.level == "l3" and log.rec_queried == "TXT":
                self.do_state_change("l3", log)
            elif log.level == "b_to4_a" and log.rec_queried == "TXT":
                self.do_state_change("b_to4_a", log)

        elif self.state.name == "l3" and log.level == "b" and log.rec_queried == "A":
            self.do_state_change("serial", log)  # Success
        elif self.state.name == "l2" and log.level == "b" and log.rec_queried == "TXT":
            self.do_state_change("maybe_serial", log)  # Success
        elif self.state.name == "maybe_serial" and log.level == "l3" and log.rec_queried == "TXT":
            self.do_state_change("delayed_parallel", log)  # Success

        elif self.state.name == "b_to4_a":
            if log.level == "l1" and log.rec_queried == "TXT":
                self.do_state_change("p_l1", log)
            elif log.level == "l2" and log.rec_queried == "TXT":
                self.do_state_change("p_l2")
            elif log.level == "l3" and log.rec_queried == "TXT":
                self.do_state_change("parallel", log)  # Success

        elif self.state.name == "p_l1":
            if log.rec_queried == "l2" and log.rec_queried == "TXT":
                self.do_state_change("p_l2")
            elif log.level == "l3" and log.rec_queried == "TXT":
                self.do_state_change("parallel", log)  # Success
        elif self.state.name == "p_l2" and log.level == "l3" and log.rec_queried == "TXT":
            self.do_state_change("parallel", log)  # Success

    def get_test_result(self, log, log_list):
        pass

    # returns a dynamic class based on SuperState
    def get_class(self, name):
        args = "name ending_log get_result_method".split()
        my_c = ClassFactory(name, args)
        return my_c(name=name, ending_log=None, get_result_method=self.get_test_result)

    def do_state_change(self, name, log):
        self.state = self.dyn_classes[name]
        self.state.ending_log = log