from validation.States import SuperState as Sup


class StartState(Sup.SuperState):

    def __init__(self, log, get_result):
        Sup.SuperState.__init__(self, "START", log, get_result)

