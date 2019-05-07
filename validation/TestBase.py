from abc import ABC, abstractmethod

from validation.state_objs.StartState import StartState


# Serves as the base class for all testing classes
class TestBase(ABC):
    def __init__(self, test_def):
        self.state = None
        self.test_def = test_def

    @abstractmethod
    def do_testing(self, log_list):
        return TestBase.check_testing(self, log_list)

    # called my subclasses to check current state of test
    # PARAM: log_list the list of log objects for a given generated name
    def check_testing(self, log_list):
        self.state = StartState(log_list[0], self.get_test_result)
        for log in log_list:
            print(str(log))
            self.test_def(log)
        return self.state.get_final_result(log_list)

    # This method is the definition of the test. Basically you pass in a query(log) and this method
    # changes self.state to reflect where in the test we are currently for a given test number.
    @abstractmethod
    def test_def(self, log):
        pass

    # The method to be used in order to write results out to file
    @abstractmethod
    def get_test_result(self, log, log_list):
        return "Gen:{:24} State:{:8}".format(str(log.generated_name), str(self.state.name))
