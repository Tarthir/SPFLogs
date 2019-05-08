import os
from validation.TestBase import TestBase
from validation.state_objs.StartState import StartState
from validation.state_objs.StateUtils import do_state_change
from validation.state_objs.StateUtils import get_class
from validation.state_objs.StateUtils import check_a


class Test16(TestBase):
    def __init__(self):
        TestBase.__init__(self, self.test_def)
        self.dyn_classes = {"to_ipv4": get_class("to_ipv4"),
                            "to_ipv6": get_class("to_ipv6"),
                            "queried_A": get_class("queried_A"),
                            "queried_AAAA": get_class("queried_AAAA"),
                            "queried_both": get_class("queried_both")}
        self.which_Test = "t16"
        self.gen_to_ip = {}
        cur_path = os.path.dirname(__file__)
        #print(cur_path + "/new_true_domains.txt")
        # take the relative path to new_true_domains
        cur_path = cur_path + "/new_true_domains.txt"
        with open(cur_path, "r") as f:
            for line in f:
                arr = line.split()
                self.gen_to_ip[arr[2]] = arr[1]

    def do_testing(self, log_list):
        # call to super class
        #print("\n")
        self.sent_to = self.gen_to_ip[log_list[0].generated_name]
        self.queried = "N/A"
        return TestBase.check_testing(self, log_list)

    def test_def(self, log):
        #print(str(log))
        # we will check for "." for ipv4 addresses and ":" for ipv6 addresses
        if isinstance(self.state, StartState) and "." in self.sent_to:
            self.state = do_state_change("to_ipv4", log, self.dyn_classes, self.get_test_result)
            #get the ip address associated with the generated name with an ip address in new_true_domains.txt
            self.sent_to = "to_ipv4"
        elif isinstance(self.state, StartState) and ":" in self.sent_to:
            self.state = do_state_change("to_ipv6", log, self.dyn_classes, self.get_test_result)
            self.sent_to = "to_ipv6"
        if check_a(log.rec_queried) and log.level != None and log.level == "b":
            if log.rec_queried == "A": #ipv4
                if self.state.name == "queried_AAAA":
                    self.state = do_state_change("queried_both", log, self.dyn_classes, self.get_test_result)
                    self.queried = "queried_both"
                else:
                    self.state = do_state_change("queried_A", log, self.dyn_classes, self.get_test_result)
                    self.queried = "queried_A"
            elif log.rec_queried == "AAAA": #ipv6
                if self.state.name == "queried_A":
                    self.state = do_state_change("queried_both", log, self.dyn_classes, self.get_test_result)
                    self.queried = "queried_both"
                else:
                    self.state = do_state_change("queried_AAAA", log, self.dyn_classes, self.get_test_result)
                    self.queried = "queried_AAAA"
        #print("queried: %s" % (self.queried))
                                

    def get_test_result(self, log, log_list):
        return "{} sent_to:{}  QueriedFor:{}".format(TestBase.get_test_result(self, log, log_list), self.sent_to, self.queried)
