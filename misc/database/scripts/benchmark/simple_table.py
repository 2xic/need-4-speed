from ..helpers.TimeIt import TimeIt
from ..helpers.RunSql import call_firebird_sql, call_postgres_sql
from ..helpers.SqlBuilder import SqlBuilder
from ..helpers.TimeIt import TimeIt
from ..helpers.Table import Table
from ..helpers.Column import Column
from ..helpers.TableValueGenerator import generate
from ..helpers.sql.Like import Like
import random
import json

debug = False

class Benchmark:
    def __init__(self) -> None:
        self.firebird = TimeIt("Firebird")
        self.postgres = TimeIt("Postgres")
        self.table = Table(
            "short_table",
        ).add_column(
            Column("id", int)
        ).add_column(
            Column("text", str)
        )
        self.rows = 100_000
        self.steps = 100

    def _setup(self):
        print(call_firebird_sql(
            SqlBuilder().create(self.table),
            debug=True
        ))

        print(call_postgres_sql(
            SqlBuilder(
                is_firebird=False
            ).create(self.table),
            debug=True
        ))

    def execute(self):
        self._setup()
        for i in range(0, self.steps):
            values = self.testing_insert_speed(
                count_rows=(self.rows // (self.steps))
            )
            self.testing_random_select(
                max_id=(self.rows * (i + 1))
            )
            self.testing_random_select_like(
                strings=values
            )
        return self

    def testing_insert_speed(self, count_rows=1):
        (table, names, values) = generate(
            self.table, 
            self.table.columns,
            count_rows
        )
        with self.firebird('insert'):
            call_firebird_sql(
                SqlBuilder().insert(
                    names,
                    values,
                    table
                ),
                debug=debug
            )

        with self.postgres('insert'):
            call_postgres_sql(
                SqlBuilder(
                    is_firebird=False
                ).insert(
                    names,
                    values,
                    table
                ),
                debug=debug
            )
        values = []
        for rows in values:
            for index, value in rows:
                col = table.columns[index]
                if col.type == str:
                    values.append(
                        value
                    )
        return values

    def testing_random_select(self, max_id):
        with self.firebird('select_id'):
            call_postgres_sql(
                SqlBuilder(
                    is_firebird=True
                ).select(
                    columns={
                        id:[
                            random.randint(0, max_id)
                            for _ in range(self.rows)
                        ]
                    }
                )
            )

        with self.postgres('select_id'):
            call_postgres_sql(
                SqlBuilder(
                    is_firebird=False
                ).select(
                    columns={
                        id:[
                            random.randint(0, max_id)
                            for _ in range(self.rows)
                        ]
                    }
                )
            )

    def testing_random_select_like(self, strings):
        with self.firebird('select_like_text'):
            call_postgres_sql(
                SqlBuilder(
                    is_firebird=True
                ).select(
                    columns={
                        "text":[
                            Like(i)
                            for i in strings
                        ]
                    }
                )
            )

        with self.postgres('select_like_text'):
            call_postgres_sql(
                SqlBuilder(
                    is_firebird=False
                ).select(
                    columns={
                        "text":[
                            Like(i)
                            for i in strings
                        ]
                    }
                )
            )

    def plot(self):
        with open("/output/insert.json", "w") as file:
            file.write(json.dumps(
                {
                    "firebird": self.firebird.entry['insert'],
                    "postgres": self.postgres.entry['insert'],
                    "x": list(map(lambda x: x * self.rows /self.steps,list(range(1, self.steps + 1)))),
                    "description": f'Insert time for {self.rows} with {self.steps} equal size batches',
                    "name": "insert.png"
                }
            ))
        with open("/output/select_id.json", "w") as file:
            file.write(json.dumps(
                {
                    "firebird": self.firebird.entry['select_id'],
                    "postgres": self.postgres.entry['select_id'],
                    "x": list(map(lambda x: x * self.rows /self.steps,list(range(1, self.steps + 1)))),
                    "description": f'select time for {self.rows} with {self.steps} equal size batches',
                    "name": "select_where_id.png"
                }
            ))
        with open("/output/select_like_text.json", "w") as file:
            file.write(json.dumps(
                {
                    "firebird": self.firebird.entry['select_like_text'],
                    "postgres": self.postgres.entry['select_like_text'],
                    "x": list(map(lambda x: x * self.rows /self.steps,list(range(1, self.steps + 1)))),
                    "description": f'select time for {self.rows} with {self.steps} equal size batches',
                    "name": "select_where_like_text.png"
                }
            ))
