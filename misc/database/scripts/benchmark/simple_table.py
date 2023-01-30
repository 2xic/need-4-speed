from ..helpers.TimeIt import TimeIt
from ..helpers.RunSql import call_firebird_sql, call_postgres_sql
from ..helpers.SqlBuilder import SqlBuilder
from ..helpers.TimeIt import TimeIt
from ..helpers.Table import Table
from ..helpers.Column import Column
import random

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
        self.rows = 1000
        self.steps = 10

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
            self.testing_insert_speed(
                max_id=(self.rows * (i + 1))
            )
            self.testing_random_select(
                max_id=(self.rows * (i + 1))
            )
        return self

    def testing_insert_speed(self, max_id=1):
        with self.firebird('insert'):
            call_firebird_sql(
                SqlBuilder().insert_based_columns(
                    self.table,
                    self.table.columns,
                    count=max_id,
                ),
                debug=debug
            )

        with self.postgres('insert'):
            call_postgres_sql(
                SqlBuilder(
                    is_firebird=False
                ).insert_based_columns(
                        self.table,
                        self.table.columns,
                        count=max_id,
                    ),
                    debug=debug
            )

    def testing_random_select(self, max_id):
        with self.firebird('select'):
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

        with self.postgres('select'):
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
