from validation.TestBase import TestBase
from validation.state_objs.SuccessState import SuccessState
from validation.state_objs.FailureState import FailureState
from validation.state_objs.BaseState import BaseState
import math

class Test21(TestBase):
    def __init__(self):
        TestBase.__init__(self, self.test_def)


    def do_testing(self, log_list):
        self.timed_out = False
        self.total_time = 0.0
        self.last_node = None
        self.biggest_depth = -math.inf
        self.largest_branch = "a"
        print("\n")
        first = log_list[0]
        last = log_list[len(log_list)-1]
        self.timed_out = (last.sec_from_1970 - first.sec_from_1970 > 20)
        self.total_time = last.sec_from_1970 - first.sec_from_1970
        if not self.timed_out:
            self.state = SuccessState(last, self.get_test_result)
        else:
            self.state = FailureState(last, self.get_test_result)
        for log in log_list:
            print(str(log))
            node = log.level
            #print("***log.level: %s\trec_type: %s**" % (node, log.rec_queried))
            stripped_node = None
            depth = self.biggest_depth
            branch = self.largest_branch
            if node == None or log.rec_queried != "TXT":
                continue
            stripped_node = node[:1]
            if stripped_node == "l":
                depth = int(node[1])
                branch = node[2]
                if depth >= self.biggest_depth:
                    self.biggest_depth = depth
                else: continue
                if branch > self.largest_branch:
                    self.largest_branch = branch
                self.last_node = "l" + str(self.biggest_depth) + self.largest_branch
        print("***Last Node: %s" % self.last_node)

        self.state.get_final_result(log_list)


    def test_def(self, log):
        pass

    def get_test_result(self, log, log_list):
        if self.timed_out:
            time_check = "greater"
        else:
            time_check = "less_than"
        return "{} 20_timeout:{} Deepest_Node:{} TotalTime:{}".format(TestBase.get_test_result(self, log, log_list), time_check, self.last_node, self.total_time)
