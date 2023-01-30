"""
TODO, this is complicated, fix it.
"""

class SqlBuilder:
    def __init__(self, is_firebird=True) -> None:
        self.sql = []
        self.is_firebird = is_firebird

    def select(self, table="ARKIV", columns={}):
        where_query = " AND ".join(
            f"{key} in ({','.join(list(map(lambda x: f'{x}', value)))})" if type(value) == list else f"{key} = {value}"
            for key, value in columns.items()
        )
        statements = self._merge_db_specific([
            f"SELECT * FROM {table}",
            (f"WHERE {where_query}" if len(columns) else ""),
            ";",
        ])
        return " ".join(statements).encode("utf-8")

    def count(self, table):
        statements = self._merge_db_specific([
            f"SELECT count(*) FROM {table};"
        ])
        return " ".join(statements).encode("utf-8")

    def insert_based_columns(self, table, columns, count=1):
        names = [
            f'{i.name}' for i in columns if not i.generated
        ]
        values = [
            [
                str(i.generate()) for i in columns if not i.generated
            ]
            for _ in range(count)
        ]

        return self.insert(names, values, table=table.name)

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