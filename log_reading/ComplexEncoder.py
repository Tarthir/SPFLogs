import json
import log_reading.LogHolder as Log


class ComplexEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, Log.LogHolder):
            return obj.__dict__
        return json.JSONEncoder.default(self, obj)

    def decode(self, j_obj):
        if 'ip' in j_obj:
            x = Log.LogHolder(j_obj['ip'])
            w = 6
        else:
            return j_obj
