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
        return "\n".join(statements).encode("utf-8")

    def select(self, table="ARKIV", columns={}):
        select = Select(
            table
        ).select([
            "count(*)"
        ]).where(columns)

        statements = self._merge_db_specific([
            select.sql(),
            ";",
        ])
        return "\n".join(statements).encode("utf-8")

    def count(self, table):
        statements = self._merge_db_specific([
            f"SELECT count(*) FROM {table};"
        ])
        return "\n".join(statements).encode("utf-8")

    def insert(self, columns, values, table="ARKIV"):
        if self.is_firebird:
            statements = self._merge_db_specific([
                "SET TERM #;",
                "execute block as ",
                "BEGIN",
                "\n ".join(
                   [ self._firebird_insert(table, columns, row)
                    for row in values]
                ),
                "\n",
                "END#",
                "SET TERM ;#",
                "COMMIT;",
                f"SELECT COUNT(*) from {table};",
            ])
        else:
            statements = [self._insert(table, columns, values)]
        return " ".join(statements).encode("utf-8")


    def create(self, table):
        return "\n".join(self._merge_db_specific([
            table.sql(
                is_firebird=self.is_firebird
            )
        ]))

    def _firebird_insert(self, table, columns, values):
        return "\n".join([
            f"INSERT INTO {table} (",
                ",".join(columns),
            ")",
            "VALUES",
            "(" + ",".join([
                    row
                    for row in values
                ]) + ")"
            ,
            ";"
        ])

    def _insert(self, table, columns, values):
        return "\n".join([
            f"INSERT INTO {table} (",
                ",".join(columns),
            ")",
            "VALUES",
                ",\n".join([
                    "(" + ",".join(row) + ")"
                    for row in values
                ]),
            ";"
        ])

    def _merge_db_specific(self, items, is_commit=False):
        combined = []
        if self.is_firebird:
            combined.append("CONNECT 'test_database';")

        combined += items
        if self.is_firebird:
            combined += [
                ("commit;" if "insert" in "".join(combined).lower() else ""),
                "quit;"
            ]

        return combined
