from validation.state_objs.StartState import StartState
from abc import ABC, abstractmethod
from validation import state_objs as s


# Serves as the base class for all testing classes
class TestBase(ABC):
    def __init__(self, test_def):
        self.state = None
        self.test_def = test_def

    @abstractmethod
    def do_testing(self, log_list):
        return TestBase.check_testing(self, log_list)

    # called my subclasses to check current state of test
    # PARAM: func - the function which will be passed a log object the current state and is compared
    # to the state this log object would place the test in
    def check_testing(self, log_list):
        self.state = StartState(log_list[0], self.get_test_result)
        for log in log_list:
            self.test_def(log)
        return self.state.get_final_result(log_list)

    # This method is the definition of the test. Basically you pass in a query(log) and this method
    # changes self.state to reflect where in the test we are currently for a given test number.
    @abstractmethod
    def test_def(self, log):
        pass

    @abstractmethod
    def get_test_result(self, log, log_list):
        return "Gen:{:24} tName:{:8} Level:{:18} Rec:{:6}\n".format(log.generated_name, self.state.name, str(self.state.ending_log.level),
                                      self.state.ending_log.rec_queried)
