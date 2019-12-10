import pudb
import dataclasses, json
from enum import Enum

class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            out = {
                'module': o.__class__.__module__,
                'class': o.__class__.__name__,
            }
            out.update(dataclasses.asdict(o))
            return out
        if isinstance(o, Enum):
            return {
                'module': o.__class__.__module__,
                'class': o.__class__.__name__,
                'name': o.name,
            }
        return super().default(o)

def dumps(obj):
    return json.dumps(obj, cls=EnhancedJSONEncoder)

def loads(string, dataclass):
    return dataclass(json.loads(string))
