"""
TODO, this is complicated, fix it.
"""
from .sql.Like import Like
from .sql.Select import Select

class SqlBuilder:
    def __init__(self, is_firebird=True) -> None:
        self.sql = []
        self.is_firebird = is_firebird

    def run(self, raw_sql):
        statements = self._merge_db_specific([
            raw_sql,
            ";",
        ])
        return " ".join(statements).encode("utf-8")

    def select(self, table="ARKIV", columns={}):
        select = Select(
            table
        ).select().where(columns)
#        for key, value in columns.items():
 #           if type(value) in [str, int, Like]:
  #              select = select.where_and(
   #                 key, value
    #            )
     #       elif type(value) == list:
      #          select = select.where_and(
       #             key, value
        #        )
         #   else:
          #      raise Exception("Unknown")

        statements = self._merge_db_specific([
            select.sql(),
            ";",
        ])
        return " ".join(statements).encode("utf-8")

    def count(self, table):
        statements = self._merge_db_specific([
            f"SELECT count(*) FROM {table};"
        ])
        return " ".join(statements).encode("utf-8")

    def insert(self, columns, values, table="ARKIV"):
        if self.is_firebird:
            statements = self._merge_db_specific([
                "SET TERM #;",
                "execute block as ",
                "BEGIN",
                "\n ".join(
                   [ self._insert(table, columns, row)
                    for row in values]
                ),
                "\n",
                "END#",
                "SET TERM ;#",
            ])
        else:
            statements = [self._insert(table, columns, values)]
        return " ".join(statements).encode("utf-8")


    def create(self, table):
        return " ".join(self._merge_db_specific([
            table.sql()
        ]))

    def _insert(self, table, columns, values):
    #    print(values)
        return "\n".join([
            f"INSERT INTO {table} (",
                ",".join(columns),
            ")",
            "VALUES",
            "",
                ",".join([
                    "(" + ",".join(row) + ")"
                    for row in values
                ]),
            ";"
        ])

    def _merge_db_specific(self, items):
        return [
            ("CONNECT 'test_database';" if self.is_firebird else "")
        ] + items + [
            ("commit;" if self.is_firebird else ""),
            ("quit;" if self.is_firebird else ""),
        ]