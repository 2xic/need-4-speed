

class Table:
    def __init__(self, name) -> None:
        self.name = name
        self.columns = []

    def add_column(self, column):
        self.columns.append(column)
        return self

    def sql(self, is_firebird):
        return "\n".join([
            f"CREATE TABLE {self.name} (",
            ",\n".join(
                i.sql(is_firebird) for i in self.columns
            ),
            ");"
        ])

