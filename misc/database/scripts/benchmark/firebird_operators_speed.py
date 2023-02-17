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
from ..helpers.sql.Update import Update
from ..helpers.sql.UpdateOrInsert import UpdateOrInsert
from ..helpers.FirebirdRunScope import RunInScope
debug = False

class FirebirdOperatorsBenchmark:
    def __init__(self) -> None:
        self.operator_1 = TimeIt("Firebird operator")
        self.operator_2 = TimeIt("Firebird operator 2")
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
        self.rows = 5_000 if not debug else 2_000
        self.steps = 100 if not debug else 10

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

    def execute(self):
        self._setup()
        for i in range(0, self.steps):
            values = self.insert_rows(
                count_rows=(self.rows // self.steps)
            )
            self.testing_updates(
                max_id=((self.rows // self.steps) * (i + 1))
            )
        return self

    def insert_rows(self, count_rows=1):
        (items_table, names, values) = generate(
            self.items_table,
            self.items_table.columns,
            count_rows
        )
        call_firebird_sql(
            SqlBuilder().insert(
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

    def testing_updates(self, max_id):
        ids = [
            random.randint(0, max_id)
            for _ in range(self.rows)
        ]
        firebird_output = None
        with self.operator_1('update_or_insert'):
            firebird_output = call_firebird_sql(
                RunInScope([
                    UpdateOrInsert(
                        self.items_table.name
                    ).values(
                        {
                            "id": id_,
                            "title": "test"
                        }
                    ).matching(
                        'id'
                    ).sql()
                    for id_ in ids
                ]),
                debug=debug
            )
        postgres_output = None
        with self.operator_2('update'):
            firebird_output = call_firebird_sql(
                RunInScope([
                    Update(
                        self.items_table.name
                    ).set_value(
                        {
                            "title": "fest"
                        }
                    ).where({
                        "id": id_
                    }).sql()
                    for id_ in ids
                ]),
                debug=debug
            )
        #assert postgres_output == firebird_output, f"{firebird_output} vs {postgres_output}"

    def plot(self):
        batch_size = int(self.rows / self.steps)
        with open("/output/firebird_update_operator.json", "w") as file:
            file.write(json.dumps(
                {
                    "operator_1": self.operator_1.get_time_seconds('update_or_insert'),
                    "operator_2": self.operator_2.get_time_seconds('update'),

                    "operator_1_name": 'update_or_insert',
                    "operator_2_name": 'update',

                    "x": list(map(lambda x: x * self.rows /self.steps,list(range(1, self.steps + 1)))),
                    "description": f'Time difference between update and update or insert',
                    "name": "update_or_update_or_insert.png"
                }
            ))
