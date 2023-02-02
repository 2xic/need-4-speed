
class Table:
    def __init__(self, name) -> None:
        self.name = name
        self.columns = []

    def add_column(self, column):
        self.columns.append(column)
        return self

    def sql(self, is_firebird):
        items = [
            f"CREATE TABLE {self.name} (",
            ",\n".join(
                i.sql(is_firebird) for i in self.columns
            ),
            ");"
        ]
        if is_firebird:
            items.append("commit;")
        for i in self.columns:
            if i.create_index:
                items.append(
                    i.index(self.name)
                )

        return "\n".join(items)
