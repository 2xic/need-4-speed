"""
TODO, this is complicated, fix it.
"""

class SqlBuilder:
    def __init__(self, is_firebird=True) -> None:
        self.sql = []
        self.is_firebird = is_firebird

    def select(self, table="ARKIV", columns={}):
        statements = [
            ("CONNECT 'test_database';" if self.is_firebird else ""),
            "\n",
            f"SELECT * FROM {table}",
            ("WHERE " + " AND ".join(
                f"{key} in ({','.join(list(map(lambda x: f'{x}', value)))})" if type(value) == list else f"{key} = {value}"
                for key, value in columns.items()
                )
                if len(columns) else ""
            ),
            ";",
            ("quit;" if self.is_firebird else ""),
        ]
        return " ".join(statements).encode("utf-8")

    def count(self, table):
        statements = [
            ("CONNECT 'test_database';" if self.is_firebird else ""),
            "\n",
            f"SELECT count(*) FROM {table}"
            ";",
            ("quit;" if self.is_firebird else ""),
        ]
        return " ".join(statements).encode("utf-8")

    def insert_based_columns(self, table, columns, count=1):
        names = [
#            f'"{i.name}"' for i in columns if not i.generated
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
            statements = [
                ("CONNECT 'test_database';" if self.is_firebird else ""),
                "\n",
                "SET TERM #;",
                "execute block as ",
                "BEGIN",
                "\n ".join(
                    " ".join([f"INSERT INTO {table} (",
                        ",".join(columns),
                        ")",
                        "VALUES",
                        "",
                        "(" + ",".join(row) + ")",
                        ";"
                    ])
                    for row in values
                ),
                "\n",
#                ";",
                "END#",
                "SET TERM ;#",
                ("commit;" if self.is_firebird else ""),            
                ("quit;" if self.is_firebird else ""),
            ]
        else:
            statements = [
                ("CONNECT 'test_database';" if self.is_firebird else ""),
                "\n",
                f"INSERT INTO {table} (",
                ",".join(columns),
                ")",
                "VALUES",
                "",
                    ",".join([
                        "(" + ",".join(row) + ")"
                        for row in values
                    ]),
                ";",
                ("commit;" if self.is_firebird else ""),            
                ("quit;" if self.is_firebird else ""),
            ]
        return " ".join(statements).encode("utf-8")

    def create(self, table):
        return " ".join([
            ("CONNECT 'test_database';" if self.is_firebird else ""),
            table.sql(),
            ("commit;" if self.is_firebird else ""),
            ("quit;" if self.is_firebird else ""),
        ])
