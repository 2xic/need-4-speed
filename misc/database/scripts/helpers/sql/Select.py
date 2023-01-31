from .Like import Like

class Select:
    def __init__(self, table) -> None:
        self.table = table
        self.columns = "*"
        self.where = []

    def select(self, columns=None):
        if type(columns) == list:
            self.columns = "".join(columns)
        elif columns is not None:
            raise Exception("Expected columns to be set")
        return self

    def where_and(self, column, value):
        if type(value) == list:
            joined_list = self.join_list(
                column, value
            )
            if type(joined_list) == list:
                joined = ",".join(joined_list)
                self.where.append(
                    f" {column} in ({joined}) "
                )
            else:
                self.where.append(
                    f" {joined_list} "
                )
        else:
            self.where.append(
                f" {column} = {value} "
            )
        return self

    def sql(self):
        base = f"SELECT {self.columns} from {self.table} "
        if len(self.where):
            base += f" WHERE {'AND'.join(self.where)}"
        return base

    def join_list(self, col, items):
        results = []
        or_query = []
        for i in items:
            if type(i) in [str, int]:
                results.append(str(i))
            elif type(i) == list:
                results.append(",".join(i))
            elif type(i) == Like:
                or_query.append(i.sql(col))

        if len(or_query) > 0:
            return " OR ".join(
                or_query
            )
        return results
