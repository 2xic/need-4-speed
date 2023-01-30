import random
from python.RunSql import call_firebird_sql, call_postgres_sql
from python.SqlBuilder import SqlBuilder
from python.TimeIt import TimeIt
from python.Table import Table
from python.Column import Column

"""
TODO:
    - Create an abstract table class with column definition
        -> Columns should have possibility to generate new values directly
        -> 
    - Instead of tracking is_firebird outside, add it in the call in call_firebird_sql
"""

firebird = TimeIt("Firebird")
postgres = TimeIt("Postgres")

table = Table(
    "short_table",
).add_column(
    Column("id", int)
).add_column(
    Column("text", str)
)

print(call_firebird_sql(
    SqlBuilder().create(table),
    debug=True
))

print(call_postgres_sql(
    SqlBuilder(
        is_firebird=False
    ).create(table),
    debug=True
))
debug = False

def testing_insert_speed(count=1):
    with firebird('insert'):
        ([call_firebird_sql(
           SqlBuilder().insert_based_columns(
                table,
                table.columns,
                count=count,
            ),
            debug=debug
        )])

    with postgres('insert'):
        ([call_postgres_sql(
           SqlBuilder(
            is_firebird=False
           ).insert_based_columns(
                table,
                table.columns,
                count=count,
            ),
            debug=debug
        )])

def testing_random_select(count):
    with firebird('select'):
        ([call_postgres_sql(
            SqlBuilder(
                is_firebird=True
            ).select(
                columns={
                    id:[
                        random.randint(0, count)
                        for _ in range(rows)
                    ]
                }
            )
        )])

    with postgres('select'):
        ([call_postgres_sql(
            SqlBuilder(
                is_firebird=False
            ).select(
                columns={
                    id:[
                        random.randint(0, count)
                        for _ in range(rows)
                    ]
                }
            )
        )])


rows = 1_000
steps = 10
for i in range(0, steps):
    testing_insert_speed(
        count=(rows // steps)
    )
    testing_random_select(
        count=(rows // steps)
    )

print(call_firebird_sql(
    SqlBuilder().count(
        table.name
    ),
    debug=True
))
print(call_postgres_sql(
    SqlBuilder(
        is_firebird=False
    ).count(
        table.name
    ),
    debug=True
))

print(postgres)
print(firebird)
