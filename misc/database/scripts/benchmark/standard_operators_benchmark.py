from ..helpers.get_foreign_key_constraint import get_foreign_key_constraint
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

debug = True

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

        # TODO: Figure out why problems appear after 2_000 rows
        self.rows = 3000 if not debug else 2_000
        self.steps = 30 if not debug else 10

    def _setup(self):
        for table in [self.purchase_table, self.items_table]:
            print(call_firebird_sql(
                SqlBuilder().create(
                    table,
                ),
                debug=True
            ))
            print(call_firebird_sql(
                get_foreign_key_constraint(
                    self.purchase_table.name,
                    "item_id",
                    self.items_table.name,
                    "id",
                    is_firebird=True
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
        firebird_output = None
        with self.firebird('select_id'):
            firebird_output = call_firebird_sql(
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
        postgres_output = None
        with self.postgres('select_id'):
            postgres_output = call_postgres_sql(
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
        assert postgres_output == firebird_output, f"{firebird_output} vs {postgres_output}"

    def testing_random_select_like(self, strings):
        firebird_output = None
        with self.firebird('select_like_text'):
            firebird_output = call_firebird_sql(
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
        postgres_output = None
        with self.postgres('select_like_text'):
            postgres_output = call_postgres_sql(
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
        assert postgres_output == firebird_output, f"{firebird_output} vs {postgres_output}"

    def testing_greater_than_less_than(self, max_id):
        between = [
            random.randint(0, max_id - 1)
            for _ in range(self.rows // self.steps + 1)
        ]
        firebird_output = None
        with self.firebird('select_greater_than_less_than'):
            firebird_output = call_firebird_sql(
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
        postgres_output = None
        with self.postgres('select_greater_than_less_than'):
            postgres_output = call_postgres_sql(
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
        assert postgres_output == firebird_output, f"{firebird_output} vs {postgres_output}"

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

        firebird_output = None
        with self.firebird('select_left_join'):
            firebird_output = call_firebird_sql(
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
        postgres_output = None
        with self.postgres('select_left_join'):
            postgres_output = call_postgres_sql(
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
        assert postgres_output == firebird_output, f"{firebird_output} vs {postgres_output}"

    def testing_join_statements(self, max_id):
        firebird_output = None
        with self.firebird('select_join'):
            firebird_output = call_firebird_sql(
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
        postgres_output = None
        with self.postgres('select_join'):
            postgres_output = call_postgres_sql(
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
        assert postgres_output == firebird_output, f"{firebird_output} vs {postgres_output}"

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
