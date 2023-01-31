from .helpers.SqlBuilder import SqlBuilder
from .helpers.sql.Like import Like

"""
Add some proper unit test for this
"""

output = SqlBuilder(
    is_firebird=False
).select(
    columns={
        "text":[
            Like(i)
            for i in [
                "test", "fest"
            ]
        ]
    }
)
print(output)

output = SqlBuilder(
    is_firebird=False
).select(
    columns={
        "text":[
            100, 20,
        ]
    }
)
print(output)

