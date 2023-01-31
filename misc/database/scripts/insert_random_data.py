print("v3")

from .helpers.RunSql import call_firebird_sql, call_postgres_sql
from .helpers.SqlBuilder import SqlBuilder
from .benchmark.simple_table import Benchmark

"""
TODO:
    - Create an abstract table class with column definition
        -> Columns should have possibility to generate new values directly
        -> 
    - Instead of tracking is_firebird outside, add it in the call in call_firebird_sql
"""

debug = False

benchmark = Benchmark().execute()

print(call_firebird_sql(
    SqlBuilder().count(
        benchmark.table.name
    ),
    debug=True
))
print(call_postgres_sql(
    SqlBuilder(
        is_firebird=False
    ).count(
        benchmark.table.name
    ),
    debug=True
))

print("OK?")
print(benchmark.postgres)
print(benchmark.firebird)

benchmark.plot()
