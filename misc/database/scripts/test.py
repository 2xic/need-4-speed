from .helpers.SqlBuilder import SqlBuilder
from .helpers.sql.Like import Like
from .helpers.sql.Between import Between
from .helpers.sql.Select import Select

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

output = SqlBuilder(
    is_firebird=False
).select(
    columns={
        "counter":[Between(20, 50)]
    }
)
print(output)

sql = Select("items").left_join(
    "purchases",
    "id",
    "item_id"
).where(
    [
        {"counter":[
            Between(i, i + 100)
            for i in [100, 200]
        ]},
        {"id":[
            Between(i, i + 100)
            for i in [100, 200]
        ]}
    ]
)
print(sql.sql())

