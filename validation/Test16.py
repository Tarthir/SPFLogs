from validation.TestBase import TestBase
from validation.state_objs.StartState import StartState
from validation.state_objs.StateUtils import get_class
from validation.state_objs.StateUtils import do_state_change

# TODO do we need to account for those queries that queriy ipv4, than 6, than 4 again?

# --------------------------------- NOT SURE HOW TO EVALUATE THE RESULTS -------------------

# STATES:
# A: All servers who queried for ipv4 first
# B: All servers who queried for ipv6 first
# C: All servers who queried ipv6 after ipv4
# D: All servers who queried ipv4 after ipv6
# E: A - C, no query after initial ipv4
# F: B - D, no query after initial ipv6
class Test16(TestBase):
    def __init__(self):
        TestBase.__init__(self, self.test_def)
        self.dyn_classes = {"ip4_first": get_class("ip4_first"),
                            "ip4_followed_by_ip6": get_class("ip4_followed_by_ip6"),
                            "ip6_first": get_class("ip6_first"),
                            "ip6_followed_by_ip4": get_class("ip6_followed_by_ip4"),
                            "ip4_nothing": get_class("ip4_nothing"),
                            "ip6_nothing": get_class("ip6_nothing"),
                            }

                            # {"A": get_class("A"),
                            # "A-C": get_class("A-C"),
                            # "B": get_class("B"),
                            # "B-D": get_class("B-D"),
                            # "A-E": get_class("A-E"),
                            # "B-F": get_class("B-F")}

    def do_testing(self, log_list):
        # call to super class
        print("\n")
        return TestBase.check_testing(self, log_list)

    def test_def(self, log):
        print(str(log))
        # we will check for "." for ipv4 addresses and ":" for ipv6 addresses
        # A:queried ipv4 first
        if isinstance(self.state, StartState) and "." in log.ip:
            self.state = do_state_change("ip4_nothing", log, self.dyn_classes, self.get_test_result)
        # B:queried ipv6 first
        elif isinstance(self.state, StartState) and ":" in log.ip:
            self.state = do_state_change("ip6_nothing", log, self.dyn_classes, self.get_test_result)
        # C:those that queried for ipv6 after ipv4
        elif not isinstance(self.state, StartState):
            if self.state.name == "ip4_nothing":
                # C:those that queried for ipv6 after ipv4
                if ":" in log.ip:
                    self.state = do_state_change("ip4_followed_by_ip6", log, self.dyn_classes, self.get_test_result)
                else:
                    # No longer apart of set E
                    self.state = do_state_change("ip4_first", log, self.dyn_classes, self.get_test_result)

            elif self.state.name == "ip6_nothing":
                # D:those that queried ipv4 after ipv6
                if "." in log.ip:
                    self.state = do_state_change("ip6_followed_by_ip4", log, self.dyn_classes, self.get_test_result)
                else:
                    # Not longer apart of set F
                    self.state = do_state_change("ip6_first", log, self.dyn_classes, self.get_test_result)

    def get_test_result(self, log, log_list):
        return TestBase.get_test_result(self, log, log_list)




# log(generated_name:harpsichordist2,test_name:t16,level:None,rec_queried:A,ip:2620:0:cc6::166)
# log(generated_name:harpsichordist2,test_name:t16,level:None,rec_queried:A,ip:2607:f8b0:4003:c11::10d)
# log(generated_name:harpsichordist2,test_name:t16,level:None,rec_queried:A,ip:173.194.101.6)
# log(generated_name:harpsichordist2,test_name:t16,level:None,rec_queried:MX,ip:2607:f8b0:4003:c11::103)
# log(generated_name:harpsichordist2,test_name:t16,level:None,rec_queried:MX,ip:2620:0:cc6::21)
# log(generated_name:harpsichordist2,test_name:t16,level:None,rec_queried:MX,ip:2607:f8b0:4003:c15::10a)
