import dataclasses, json

class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        return super().default(o)

def dumps(obj):
    return json.dumps(obj, cls=EnhancedJSONEncoder)

def loads(string, dataclass):
    return dataclass(json.loads(string))
