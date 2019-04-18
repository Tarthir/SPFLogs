from validation.state_objs import SuperState as Sup


class FailureState(Sup.SuperState):
    def __init__(self, log, get_result):
        Sup.SuperState.__init__(self, "FAILURE", log, get_result)
