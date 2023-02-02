from .Like import Like
from .Between import Between
from .batch_array import batch_array

class Select:
    def __init__(self, table) -> None:
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

    def where(self, and_or):
        self.where_str = self.set_where(and_or)
        return self

    def set_where(self, and_or):
        if type(and_or) == list:
            return " OR ".join([
                self.set_where(i) for i in and_or
            ])
        elif type(and_or) == dict:
            return " AND ".join(
                [
                    self._where_and(column, value)
                    for column, value in and_or.items()
                ]
            )
        else:
            raise Exception("opsi")

    def _where_and(self, column, value):
        statements = []
        if type(value) == list:
            joined_list = self._join_list(
                column, value
            )
            if type(joined_list) == list:
                items = map(lambda x:f" {column} in (" +",". join(x) + ")", batch_array(
                    joined_list,
                    1400
                ))
                statements.append(
                    "(" +" OR ".join(items) + ")"
                )
            else:
                statements.append(
                    f" {joined_list} "
                )
        else:
            statements.append(
                f" {column} = {value} "
            )
        return " AND ".join(statements)

    def left_join(self, table_name, current_table_column, join_table_column):
        self.joins.append(
            f"LEFT JOIN {table_name} on {self.table}.{current_table_column} = {table_name}.{join_table_column}"
        )
        return self

    def sql(self):
        base = f"SELECT {self.columns} from {self.table}\n"
        if len(self.joins):
            base += '\n'.join(self.joins) + "\n"
        if len(self.where_str):
            base += f" WHERE {self.where_str}"
        return base

    def _join_list(self, col, items):
        results = []
        or_query = []
        for i in items:
            if type(i) in [str, int]:
                results.append(str(i))
            elif type(i) == list:
                results.append(",".join(i))
            elif type(i) == Like:
                or_query.append(i.sql(col))
            elif type(i) == Between:
                or_query.append(i.sql(col))
            else:
                raise Exception("Unknown type")
        if len(or_query) > 0:
            return " OR ".join(
                or_query
            )
        return results
