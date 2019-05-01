from validation.TestBase import TestBase
from validation.state_objs.FailureState import FailureState
from validation.state_objs.StartState import StartState
from validation.state_objs.StateUtils import check_a
from validation.state_objs.SuccessState import SuccessState


class Test17(TestBase):
    def __init__(self):
        TestBase.__init__(self, self.test_def)
        self.num_of_b_queries = 0

    def do_testing(self, log_list):
        # call to super class
        self.num_of_b_queries = 0
        return TestBase.check_testing(self, log_list)

    def test_def(self, log):
        if isinstance(self.state, StartState) and log.level == "b" and check_a(log.rec_queried):
            self.state = SuccessState(log, self.get_test_result)
            self.num_of_b_queries = 1
        elif isinstance(self.state, SuccessState) and log.level == "b" and check_a(log.rec_queried):
            self.state = FailureState(log, self.get_test_result)
            self.num_of_b_queries += 1
        elif isinstance(self.state, FailureState):
            # if there are more b queries
            # TODO may need to change to only get b queries before l1-l5 queries?
            if log.level == "b" and check_a(log.rec_queried):
                self.num_of_b_queries += 1
            self.state = FailureState(log, self.get_test_result)

    def get_test_result(self, log, log_list):
        cache = ""
        if isinstance(self.state, SuccessState):
            cache = "Yes"
        else:
            cache = "No"
        return "{} Caching:{} #of b{}".format(TestBase.get_test_result(self, log, log_list), cache, self.num_of_b_queries)
