print("v3")

from .helpers.RunSql import call_firebird_sql, call_postgres_sql
from .helpers.SqlBuilder import SqlBuilder
from .benchmark.standard_operators_benchmark import Benchmark

"""
TODO:
    - Instead of tracking is_firebird outside, add it in the call in call_firebird_sql
"""

debug = False

benchmark = Benchmark().execute()

print(call_firebird_sql(
    SqlBuilder().count(
        benchmark.items_table.name
    ),
    debug=True
))
print(call_postgres_sql(
    SqlBuilder(
        is_firebird=False
    ).count(
        benchmark.items_table.name
    ),
    debug=True
))

print("OK?")
print(benchmark.postgres)
print(benchmark.firebird)

benchmark.plot()
