from validation.States import SuperState as Sup


class BaseState(Sup.SuperState):

    def __init__(self, log, get_result):
        Sup.SuperState.__init__(self, "BASE", log, get_result)

