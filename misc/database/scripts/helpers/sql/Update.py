from .Like import Like
from .Between import Between
from .batch_array import batch_array
from .StandardOperators import StandardOperators

class Update(StandardOperators):
    def __init__(self, table) -> None:
        super().__init__(table)
        self.table = table
        self.columns = "count(*)"
        self.joins = []
        self.set_str = ""
        self.where_str = ""

    def update(self, columns=None):
        if type(columns) == list:
            self.columns = "".join(columns)
        elif columns is not None:
            raise Exception("Expected columns to be set")
        return self

    def set_value(self, columns):
        sets = []
        for key, value in columns.items():
            if type(value) == str:
                value = f"'{value}'"
            cmd = f"{key} = {value}"
            if len(sets):
                cmd += (",")
            sets.append(cmd)
        self.set_str = "\n".join(sets)
        return self

    def sql(self):
        base = "CONNECT 'test_database';"
        base += f"UPDATE {self.table}\n"
        if len(self.set_str):
            base += f" set {self.set_str}"
        if len(self.joins):
            base += '\n'.join(self.joins) + "\n"
        if len(self.where_str):
            base += f" WHERE {self.where_str}"
        base += ";"
        return base
