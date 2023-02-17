print("v3")

from .helpers.RunSql import call_firebird_sql, call_postgres_sql
from .helpers.SqlBuilder import SqlBuilder
from .benchmark.firebird_operators_speed import FirebirdOperatorsBenchmark

"""
TODO:
    - Instead of tracking is_firebird outside, add it in the call in call_firebird_sql
"""

debug = False

benchmark = FirebirdOperatorsBenchmark().execute()
benchmark.plot()
