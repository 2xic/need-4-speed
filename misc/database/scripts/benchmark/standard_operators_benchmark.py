from ..helpers.TimeIt import TimeIt
from ..helpers.RunSql import call_firebird_sql, call_postgres_sql
from ..helpers.SqlBuilder import SqlBuilder
from ..helpers.TimeIt import TimeIt
from ..helpers.Table import Table
from ..helpers.Column import Column
from ..helpers.TableValueGenerator import generate
from ..helpers.sql.Like import Like
from ..helpers.sql.Between import Between
from ..helpers.sql.Select import Select
import random
import json

debug = False

class Benchmark:
    def __init__(self) -> None:
        self.firebird = TimeIt("Firebird")
        self.postgres = TimeIt("Postgres")
        self.items_table = Table(
            "item",
        ).add_column(
            Column("id", int)
        ).add_column(
            Column("title", str)
        ).add_column(
            Column("description", str).set_length(512)
        ).add_column(
            Column("counter", int)
        )
        self.purchase_table = Table(
            "purchases"
        ).add_column(
            Column("item_id", int, create_index=False)
        ).add_column(
            Column("purchase_id", int , generate=True)
        )

        self.rows = 3000 if not debug else 100
        self.steps = 30 if not debug else 1

    def _setup(self):
        for table in [self.purchase_table, self.items_table]:
            print(call_firebird_sql(
                SqlBuilder().create(
                    table,
                ),
                debug=True
            ))

            print(call_postgres_sql(
                SqlBuilder(
                    is_firebird=False
                ).create(
                    table,
                ),
                debug=True
            ))

    def execute(self):
        self._setup()
        for i in range(0, self.steps):
            values = self.testing_insert_speed(
                count_rows=(self.rows // (self.steps) + 1)
            )
            self.testing_random_select(
                max_id=(self.rows * (i + 1))
            )
            self.testing_random_select_like(
                strings=values
            )
            self.testing_greater_than_less_than(
                max_id=(self.rows * (i + 1))
            )
            self.testing_left_join_statements(
                max_id=(self.rows * (i + 1))
            )
            self.testing_join_statements(
                max_id=(self.rows * (i + 1))
            )
        return self

    def testing_insert_speed(self, count_rows=1):
        (items_table, names, values) = generate(
            self.items_table,
            self.items_table.columns,
            count_rows
        )
        with self.firebird('insert'):
            call_firebird_sql(
                SqlBuilder().insert(
                    names,
                    values,
                    items_table
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
                    items_table
                ),
                debug=debug
            )
        string_values = []
        for rows in values:
            for index, value in enumerate(rows):
                col = self.items_table.columns[index]
                if col.type == str:
                    string_values.append(
                        value
                    )
        return string_values

    def testing_random_select(self, max_id):
        ids = [
            random.randint(0, max_id)
            for _ in range(self.rows)
        ]
        with self.firebird('select_id'):
            call_firebird_sql(
                SqlBuilder(
                    is_firebird=True
                ).select(
                    table=self.items_table.name,
                    columns={
                        "id":ids
                    }
                ),
                debug=debug
            )

        with self.postgres('select_id'):
            call_postgres_sql(
                SqlBuilder(
                    is_firebird=False
                ).select(
                    table=self.items_table.name,
                    columns={
                        "id":ids
                    }
                ),
                debug=debug
            )

    def testing_random_select_like(self, strings):
        with self.firebird('select_like_text'):
            call_firebird_sql(
                SqlBuilder(
                    is_firebird=True
                ).select(
                    table=self.items_table.name,
                    columns={
                        "title":[
                            Like(i)
                            for i in strings
                        ]
                    }
                ),
                debug=debug
            )

        with self.postgres('select_like_text'):
            call_postgres_sql(
                SqlBuilder(
                    is_firebird=False
                ).select(
                    table=self.items_table.name,
                    columns={
                        "title":[
                            Like(i)
                            for i in strings
                        ]
                    }
                ),
                debug=debug
            )


    def testing_greater_than_less_than(self, max_id):
        between = [
            random.randint(0, max_id - 1)
            for _ in range(self.rows // self.steps + 1)
        ]
        with self.firebird('select_greater_than_less_than'):
            call_firebird_sql(
                SqlBuilder(
                    is_firebird=True
                ).select(
                    table=self.items_table.name,
                    columns={
                        "counter":[
                            Between(i, i + 100)
                            for i in between
                        ]
                    }
                ),
                debug=debug
            )

        with self.postgres('select_greater_than_less_than'):
            call_postgres_sql(
                SqlBuilder(
                    is_firebird=False
                ).select(
                    table=self.items_table.name,
                    columns={
                        "counter":[
                            Between(i, i + 100)
                            for i in between
                        ]
                    }
                ),
                debug=debug
            )

    def testing_left_join_statements(self, max_id):
        (purchases, names, values) = generate(
            self.purchase_table,
            self.purchase_table.columns,
            100
        )
        call_firebird_sql(
            SqlBuilder().insert(
                names,
                values,
                purchases
            ),
            debug=debug
        )
        call_postgres_sql(
            SqlBuilder(
                is_firebird=False
            ).insert(
                names,
                values,
                purchases
            ),
            debug=debug
        )

        with self.firebird('select_left_join'):
            call_firebird_sql(
                SqlBuilder(
                    is_firebird=True
                ).run(
                    Select(self.items_table.name).
                    left_join(
                        purchases,
                        "id",
                        "item_id"
                    ).sql()
                ),
                debug=debug
            )

        with self.postgres('select_left_join'):
            call_postgres_sql(
                SqlBuilder(
                    is_firebird=False
                ).run(
                    Select(self.items_table.name).
                    left_join(
                        purchases,
                        "id",
                        "item_id"
                     ).sql()
                ),
                debug=debug
            )

    def testing_join_statements(self, max_id):
        with self.firebird('select_join'):
            call_firebird_sql(
                SqlBuilder(
                    is_firebird=True
                ).run(
                    Select(self.items_table.name).
                    left_join(
                        self.purchase_table.name,
                        "id",
                        "item_id"
                    ).sql()
                ),
                debug=debug
            )

        with self.postgres('select_join'):
            call_postgres_sql(
                SqlBuilder(
                    is_firebird=False
                ).run(
                    Select(self.items_table.name).
                    left_join(
                        self.purchase_table.name,
                        "id",
                        "item_id"
                     ).sql()
                ),
                debug=debug
            )

    def plot(self):
        batch_size = int(self.rows / self.steps)
        with open("/output/insert.json", "w") as file:
            file.write(json.dumps(
                {
                    "firebird": self.firebird.get_time_seconds('insert'),
                    "postgres": self.postgres.get_time_seconds('insert'),
                    "x": list(map(lambda x: x * self.rows /self.steps,list(range(1, self.steps + 1)))),
                    "description": f'Insert time, {self.steps} batches with size {batch_size}',
                    "name": "insert.png"
                }
            ))
        with open("/output/select_id.json", "w") as file:
            file.write(json.dumps(
                {
                    "firebird": self.firebird.get_time_seconds('select_id'),
                    "postgres": self.postgres.get_time_seconds('select_id'),
                    "x": list(map(lambda x: x * self.rows /self.steps,list(range(1, self.steps + 1)))),
                    "description": f'select time based on id, {self.steps} batches with size {batch_size}',
                    "name": "select_where_id.png"
                }
            ))
        with open("/output/select_like_text.json", "w") as file:
            file.write(json.dumps(
                {
                    "firebird": self.firebird.get_time_seconds('select_like_text'),
                    "postgres": self.postgres.get_time_seconds('select_like_text'),
                    "x": list(map(lambda x: x * self.rows /self.steps,list(range(1, self.steps + 1)))),
                    "description": f'select where like text field, {self.steps} batches with size {batch_size}',
                    "name": "select_where_like_text.png"
                }
            ))
        with open("/output/select_greater_than_less_than.json", "w") as file:
            file.write(json.dumps(
                {
                    "firebird": self.firebird.get_time_seconds('select_greater_than_less_than'),
                    "postgres": self.postgres.get_time_seconds('select_greater_than_less_than'),
                    "x": list(map(lambda x: x * self.rows /self.steps,list(range(1, self.steps + 1)))),
                    "description": f'select where between range, {self.steps} batches with size {batch_size}',
                    "name": "select_greater_than_less_than.png"
                }
            ))
        with open("/output/select_join.json", "w") as file:
            file.write(json.dumps(
                {
                    "firebird": self.firebird.get_time_seconds('select_join'),
                    "postgres": self.postgres.get_time_seconds('select_join'),
                    "x": list(map(lambda x: x * self.rows /self.steps,list(range(1, self.steps + 1)))),
                    "description": f'select join, {self.steps} batches with size {batch_size}',
                    "name": "select_join.png"
                }
            ))

        with open("/output/select_left_join.json", "w") as file:
            file.write(json.dumps(
                {
                    "firebird": self.firebird.get_time_seconds('select_left_join'),
                    "postgres": self.postgres.get_time_seconds('select_left_join'),
                    "x": list(map(lambda x: x * self.rows /self.steps,list(range(1, self.steps + 1)))),
                    "description": f'select left join, {self.steps} batches with size {batch_size}',
                    "name": "select_left_join.png"
                }
            ))
