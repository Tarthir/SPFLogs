import validation.TestBase as BaseClass
import validation.States as MyEnum


class Test06(BaseClass.TestBase):

    def check_testing(self, log_list):
        self.state = MyEnum.States.START
        for log in log_list:
            if self.state == MyEnum.States.START and log.rec_queried == "TXT":
                self.state = MyEnum.States.BASE
            elif log.rec_queried == "b" and self.state == MyEnum.States.BASE:
                self.state = MyEnum.States.SUCCESS
            elif self.state == MyEnum.States.SUCCESS and log.rec_queried == "c": # TODO does this work? Do i need to look for other queries after?
                return MyEnum.States.FAIL
        return self.state
