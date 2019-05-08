from validation.TestBase import TestBase
from validation.state_objs.SuccessState import SuccessState
from validation.state_objs.StartState import StartState
from validation.state_objs.BaseState import BaseState
from validation.state_objs.FailureState import FailureState
from validation.state_objs.StateUtils import check_a
from validation.state_objs.StateUtils import do_state_change
from validation.state_objs.StateUtils import get_class
import math

# meaning lets have a dict for each test, we can add states as needed?
class Test09(TestBase):

    def __init__(self):
        TestBase.__init__(self, self.test_def)
        self.highest_level = -math.inf
        self.dyn_classes = {"l1": get_class("l1"), "l2": get_class("l2"), "l3": get_class("l3"),
                            "l4": get_class("l4"), "l5": get_class("l5"), "l6": get_class("l6"),
                            "l7": get_class("l7"), "l8": get_class("l8"), "l9": get_class("l9"),
                            "l10": get_class("l10"), "l11": get_class("l11"), "l12": get_class("l12"),
                            "l13": get_class("l13"), "l14": get_class("l14"), "l15": get_class("l15"),
                            "l16": get_class("l16"), "l17": get_class("l17"), "l18": get_class("l18"),
                            "l19": get_class("l19"), "l20": get_class("l20"), "l21": get_class("l21"),
                            "l22": get_class("l22")}

    def get_test_result(self, log, log_list):
        return TestBase.get_test_result(self, log, log_list)

    def do_testing(self, log_list):
        #print("\n")
        self.highest_level = -math.inf
        return TestBase.check_testing(self, log_list)

    def test_def(self, log):
        #print(str(log))
        if log.level is not None:
            if log.level[:1] == "l":
                level_num = int(log.level[1:])
                if level_num > self.highest_level:
                    self.highest_level = level_num
        #print(self.highest_level)
        class_level = self.switch_method(self.highest_level)
        #print("upper class levels: %s" % class_level)
        if class_level == None:
            if isinstance(self.state, StartState) and log.rec_queried == "TXT" and log.level == None:
                self.state = BaseState(log, self.get_test_result)
            else:
                pass
        else:
            self.state = do_state_change(class_level, log, self.dyn_classes, self.get_test_result)
        #print("class levels: %s" % class_level)

    def switch_method( self, argument ):
        switcher = {
            1: "l1",
            2: "l2",
            3: "l3",
            4: "l4",
            5: "l5",
            6: "l6",
            7: "l7",
            8: "l8",
            9: "l9",
            10: "l10",
            11: "l11",
            12: "l12",
            13: "l13",
            14: "l14",
            15: "l15",
            16: "l16",
            17: "l17",
            18: "l18",
            19: "l19",
            20: "l20",
            21: "l21",
            22: "l22"
        }
        return switcher.get(argument, None)

        # if isinstance(self.state, StartState) and log.rec_queried == "TXT" and log.level == None:
        #     self.state = BaseState(log, self.get_test_result)
        #
        # elif (isinstance(self.state, BaseState) or isinstance(self.state, SuccessState)) and log.level != "l10" \
        #         and log.rec_queried == "TXT":
        #     self.state = FailureState(log, self.get_test_result)  # logic flow lets us know when it stopped
        # elif isinstance(self.state, FailureState) and log.level == "l10" and log.rec_queried == "TXT":
        #     self.state = SuccessState(log, self.get_test_result)
