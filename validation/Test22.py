from validation.TestBase import TestBase
from validation.state_objs.BaseState import BaseState
from validation.state_objs.StartState import StartState
from validation.state_objs.StateUtils import check_a
from validation.state_objs.StateUtils import do_state_change
from validation.state_objs.StateUtils import get_class

class Test22(TestBase):
    def __init__(self):
        TestBase.__init__(self, self.test_def)

    def do_testing(self, log_list):
        # call to super class
        #print("\n")
        self.mail_map = { "mail01":0, "mail02":0, "mail03":0, "mail04":0, "mail05":0 }
        return TestBase.check_testing(self, log_list)

    def test_def(self, log):
        #print(str(log))
        try:
            if isinstance(self.state, StartState) and log.rec_queried == "TXT" and log.level is None:
                #print("we are in the first if statement")
                self.state = BaseState(log, self.get_test_result)
            elif isinstance(self.state, BaseState) and check_a(log.rec_queried) and log.level is not None:
                if "mail" in log.level:
                    self.mail_map[log.level] += 1
                    #print(self.mail_map)
        except Exception as err:
            print("------Error: %s" % str(err))

    def get_test_result(self, log, log_list):
        result = ""
        total = 0
        for key in self.mail_map:
            result += key + ":" + str(self.mail_map[key]) + " "
            total += self.mail_map[key]
        return "{} {} Total:{}".format(TestBase.get_test_result(self, log, log_list), result, str(total))
