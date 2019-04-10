import validation.States as MyEnum
import validation.TestBase as BaseClass


class Test05(BaseClass.TestBase):

    def check_testing(self, log_list):
        self.state = MyEnum.States.START
        for log in log_list:
            # b means we have succeeded, all other queries are fine, no need to check
            if log.level == "b":
                return MyEnum.States.SUCCESS
            elif log.level == "l11" and self.state != MyEnum.States.SUCCESS:
                return MyEnum.States.FAIL
            elif log.rec_queried != "l11" and log.rec_queried == "TXT" and self.state != MyEnum.States.SUCCESS:
                self.state = MyEnum.States.BASE
        return self.state

    # def evaluate_line(self, line_list):
    #     # print("CLASS 5 EVALUATE_LINE FUNCTION")
    #     if line_list[6] is None or line_list[7] is None or line_list[8] is None:
    #         print("Inconclusive Generated Name")
    #     else:
    #         # print(self.state)
    #         pass
    #     # print(self.state)
    #     if line_list[1] is None and line_list[2] is None and line_list[3] is None and line_list[5] is None and \
    #             line_list[9] is None and line_list[10] is None and line_list[11] == 'TXT' and self.state == START_STATE:
    #             self.state = BASE_STATE
    #
    #     elif line_list[1] is None and line_list[2] is None and line_list[3] is None and line_list[5] == 'l11' and \
    #             line_list[9] is None and line_list[10] is None and (
    #             line_list[11] == 'A' or line_list[11] == 'AAAA' or line_list[11] == 'TXT'):
    #         self.state = FAIL_STATE
    #
    #     return self.state
