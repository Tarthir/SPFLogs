from validation.state_objs.SuperState import SuperState


# https://stackoverflow.com/questions/15247075/how-can-i-dynamically-create-derived-classes-from-a-base-class
def class_factory(name, argnames, BaseClass=SuperState):
    def __init__(self, **kwargs):
        vals = []
        for key, value in kwargs.items():
            # here, the argnames variable is the one passed to the
            # ClassFactory call
            if key not in argnames:
                raise TypeError("Argument %s not valid for %s"
                    % (key, self.__class__.__name__))
            setattr(self, key, value)
            vals.append(value)
        BaseClass.__init__(self, vals[0], vals[1], vals[2] )
    newclass = type(name, (BaseClass,),{"__init__": __init__})
    return newclass


# returns a dynamic class based on SuperState
def get_class(name, func):
    args = "name ending_log get_result_method".split()
    my_c = class_factory(name, args)
    return my_c(name=name, ending_log=None, get_result_method=func)


def do_state_change(name, log, dyn):
    new_state = dyn[name]
    new_state.ending_log = log
    return new_state


def check_a(rec):
    return rec == s.States.A or rec == s.States.AAAA