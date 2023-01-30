

class Table:
    def __init__(self, name) -> None:
        self.name = name
        self.columns = []

    def add_column(self, column):
        self.columns.append(column)
        return self

    def sql(self):
        return "\n".join([
            f"CREATE TABLE {self.name} (",
            ",".join(
                i.sql() for i in self.columns
            ),
            ");"
        ])
    
    