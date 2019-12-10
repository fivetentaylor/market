import pudb
import dson

import dataclasses as dcs
from enum import Enum, auto

class TestEnum(Enum):
    RED = auto()
    GREEN = auto()
    BLUE = auto()

@dcs.dataclass
class TestDClass:
    account: str
    kind: str

def test_dson_dumps():
    pudb.set_trace()
    x = dson.dumps(TestDClass(account='test', kind='test'))
    y = dson.dumps(TestEnum.RED)
    z = 0

