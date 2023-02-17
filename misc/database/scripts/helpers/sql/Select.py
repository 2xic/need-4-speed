from .Like import Like
from .Between import Between
from .batch_array import batch_array
from .StandardOperators import StandardOperators

class Select(StandardOperators):
    def __init__(self, table) -> None:
        super().__init__(table)
        self.table = table
        self.columns = "count(*)"
        self.joins = []
        self.where_str = ""

    def select(self, columns=None):
        if type(columns) == list:
            self.columns = "".join(columns)
        elif columns is not None:
            raise Exception("Expected columns to be set")
        return self
