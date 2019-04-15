from validation.States import SuperState as Sup


class SuccessState(Sup.SuperState):

    def __init__(self, log, get_result):
        Sup.SuperState.__init__(self, "SUCCESS", log, get_result)

