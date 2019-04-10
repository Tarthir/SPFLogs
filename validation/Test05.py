

class Test05():

    def check_testing(self, log, test_name):
        if log.rec_queried

    def evaluate_line(self, line_list):
        # print("CLASS 5 EVALUATE_LINE FUNCTION")
        if line_list[6] is None or line_list[7] is None or line_list[8] is None:
            print("Inconclusive Generated Name")
        else:
            # print(self.state)
            pass
        # print(self.state)
        if line_list[1] is None and line_list[2] is None and line_list[3] is None and line_list[5] is None and \
                line_list[9] is None and line_list[10] is None and line_list[11] == 'TXT' and self.state == START_STATE:
                self.state = BASE_STATE

        elif line_list[1] is None and line_list[2] is None and line_list[3] is None and line_list[5] == 'l11' and \
                line_list[9] is None and line_list[10] is None and (
                line_list[11] == 'A' or line_list[11] == 'AAAA' or line_list[11] == 'TXT'):
            self.state = FAIL_STATE

        return self.state
