from .Like import Like
from .Between import Between
from .batch_array import batch_array
from .StandardOperators import StandardOperators

class UpdateOrInsert(StandardOperators):
    def __init__(self, table) -> None:
        super().__init__(table)
        self.table = table
        self.columns = "count(*)"
        self.joins = []
        self.set_str = ""
        self.where_str = ""

        self.insert_columns = []
        self.insert_values = []
        self.matching_values = []

    def update_or_insert(self, columns=None):
        return self

    def values(self, columns):
        for key, value in columns.items():
            self.insert_columns.append(key)
            if type(value) == str:
                value = f"'{value}'"
            self.insert_values.append(value)
        return self

    def matching(self, columns):
        if type(columns) == list:
            self.matching_values = columns
        else:
            self.matching_values.append(columns)
        return self

    def sql(self):
        base = "CONNECT 'test_database';"
        base += f"update or insert into {self.table}\n"
        cols = ",".join(self.insert_columns)
        base += f"({cols})"
        values = ",".join(list(map(str, self.insert_values)))
        base += f"values ({values})\n"
        matching = ",".join(self.matching_values)
        matching += f"matching ({matching})\n"
        base += f"RETURNING ({self.matching_values[0]});"
        return base
