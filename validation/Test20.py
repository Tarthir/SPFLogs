import os

from validation import States as s
from validation.TestBase import TestBase
from validation.state_objs.FailureState import FailureState
from validation.state_objs.StartState import StartState
from validation.state_objs.StateUtils import do_state_change
from validation.state_objs.StateUtils import get_class
from validation.state_objs.SuccessState import SuccessState


class Test20(TestBase):
    def __init__(self):
        TestBase.__init__(self, self.test_def)
        self.dyn_classes = {"to_ipv4": get_class("to_ipv4"),
                            "to_ipv6": get_class("to_ipv6")}
        self.ipv_method = "."
        self.which_Test = "t20"
        self.gen_to_ip = {}
        cur_path = os.path.dirname(__file__)
        # take the relative path to new_true_domains
        cur_path = cur_path + "/new_true_domains.txt"
        with open(cur_path, "r") as f:
            for line in f:
                arr = line.split()
                self.gen_to_ip[arr[2]] = arr[1]

    def do_testing(self, log_list):
        # call to super class
        self.sent_to = self.gen_to_ip[log_list[0].generated_name]
        #print("\n")
        return TestBase.check_testing(self, log_list)

    def test_def(self, log):
        #print(str(log))
        if isinstance(self.state, StartState) and "." in self.sent_to:
            self.state = do_state_change("to_ipv4", log, self.dyn_classes, self.get_test_result)
            self.sent_to = "to_ipv4"
            # get the ip address associated with the generated name with an ip address in new_true_domains.txt
        elif isinstance(self.state, StartState) and ":" in self.sent_to:
            self.state = do_state_change("to_ipv6", log, self.dyn_classes, self.get_test_result)
            self.sent_to = "to_ipv6"
        elif self.state.name == "to_ipv6" or self.state.name == "to_ipv4" or isinstance(self.state, FailureState):
            # ipv_protocol is the label "ipv4" or "ipv6" that was in the query
            if log.rec_queried == s.States.TXT.value and log.ipv_protocol is not None:
                self.state = SuccessState(log, self.get_test_result)
            else:
                self.state = FailureState(log, self.get_test_result)

    def get_test_result(self, log, log_list):
        return "{} sent_to:{}  Protocol:{}".format(TestBase.get_test_result(self, log, log_list), self.sent_to, log.ipv_protocol)

