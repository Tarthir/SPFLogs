from validation.TestBase import TestBase
from validation.state_objs.SuccessState import SuccessState
from validation.state_objs.StartState import StartState
from validation.state_objs.BaseState import BaseState
from validation.state_objs.FailureState import FailureState
from validation.state_objs.StateUtils import check_a

class Test12(TestBase):
    def __init__(self):
        TestBase.__init__(self, self.test_def)

    def do_testing(self, log_list):
        # call to super class
        print("\n")
        return TestBase.check_testing(self, log_list)

    def test_def(self, log):
        print(str(log))
        if isinstance(self.state, StartState) and log.rec_queried == "TXT":
            self.state = BaseState(log, self.get_test_result)
        elif isinstance(self.state, BaseState) and log.level == "b" and log.rec_queried == "MX":
            self.state = SuccessState(log, self.get_test_result)
        #elif isinstance(self.state, SuccessState):
            #self.state = FailureState(log, self.get_test_result)
        elif isinstance(self.state, SuccessState) and log.level == "b" and check_a(log.rec_queried): # for queries after initial failure
            self.state = FailureState(log, self.get_test_result)

    def get_test_result(self, log, log_list):
        return TestBase.get_test_result(self, log, log_list)


# what happens with this one?
#
# log(generated_name:braveness,test_name:t12,level:None,rec_queried:A,time_1970:1554515099.704629)
# log(generated_name:braveness,test_name:t12,level:None,rec_queried:TXT,time_1970:1554515099.766765)
# log(generated_name:braveness,test_name:t12,level:None,rec_queried:A,time_1970:1554515099.83052)
# log(generated_name:braveness,test_name:t12,level:b,rec_queried:A,time_1970:1554515099.882785)
# log(generated_name:braveness,test_name:t12,level:b,rec_queried:MX,time_1970:1554515099.942067)
