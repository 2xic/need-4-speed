from ..helpers.sql.Like import Like
from ..helpers.TableValueGenerator import generate
from ..helpers.SqlBuilder import SqlBuilder
from ..helpers.Table import Table
from ..helpers.Column import Column
from .Snapshot import Snapshot
from ..helpers.SqlBuilder import SqlBuilder
from ..helpers.sql.Between import Between
from ..helpers.sql.Select import Select
import random

table = Table(
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

purchase_table = Table(
    "purchases"
).add_column(
    Column("item_id", int)
).add_column(
    Column("purchase_id", int)
)

def test_firebird_create():
    sql = SqlBuilder().create(table)
    assert Snapshot("create_firebird").create_or_save(sql) == sql

def test_postgres_create():
    sql = SqlBuilder(
        is_firebird=False
    ).create(table)
    assert Snapshot("create_postgres").create_or_save(sql) == sql

def test_firebird__select_number():
    sql = SqlBuilder(
        is_firebird=True
    ).select(
        columns={
            "counter":list(range(2200))
        }
    ).decode('utf-8')
    assert Snapshot("select_firebird").create_or_save(sql) == sql

def test_postgres__select_number():
    sql = SqlBuilder(
        is_firebird=False
    ).select(
        columns={
            "counter":list(range(2200))
        }
    ).decode('utf-8')
    assert Snapshot("select_postgres").create_or_save(sql) == sql

def test_select_like():
    strings = [
        'test',
        'fest'
    ]
    sql =                 SqlBuilder(
        is_firebird=True
    ).select(
        columns={
            "title":[
                Like(i)
                for i in strings
            ]
        }
    ).decode('utf-8')
    assert Snapshot("select_like_firebird").create_or_save(sql) == sql

def test_firebird_insert():
    (table_name, names, values) = generate(
        table,
        table.columns,
        5
    )
    sql = SqlBuilder().insert(
        names,
        values,
        table_name
    ).decode('utf-8')
    assert Snapshot("firebird_test_insert").create_or_save(sql) == sql

def test_insert_postgres():
    (table_name, names, values) = generate(
        table,
        table.columns,
        5
    )
    sql = SqlBuilder(
        is_firebird=False
    ).insert(
        names,
        values,
        table_name
    ).decode('utf-8')
    assert Snapshot("postgres_test_insert").create_or_save(sql) == sql

def test_postgres_select_like():
    strings = [
        'test',
        'fest'
    ]
    sql = SqlBuilder(
        is_firebird=False
    ).select(
        columns={
            "title":[
                Like(i)
                for i in strings
            ]
        }
    ).decode('utf-8')
    assert Snapshot("select_like_postgres").create_or_save(sql) == sql

def test_firebird_left_join():
    between = [
        random.randint(0, 5 - 1)
        for _ in range(10)
    ]
    sql = SqlBuilder(
        is_firebird=False
    ).run(
        Select(table.name).
        left_join(
            purchase_table.name,
            "id",
            "item_id"
        ).where(
            [
                {
                    "counter":[
                        Between(i, i + 100)
                        for i in between
                    ]
                },
                {
                    "purchase_id":[
                        Between(i, i + 100)
                        for i in between
                    ]
                }
            ]
        ).sql()
    ).decode('utf-8')
    assert Snapshot("select_left_join_firebird").create_or_save(sql) == sql

def test_postgres_select_left_join():
    between = [
        random.randint(0, 5 - 1)
        for _ in range(10)
    ]
    sql = SqlBuilder(
        is_firebird=False
    ).run(
        Select(table.name).
        left_join(
            purchase_table.name,
            "id",
            "item_id"
        ).where(
            [
                {
                    "counter":[
                        Between(i, i + 100)
                        for i in between
                    ]
                },
                {
                    "purchase_id":[
                        Between(i, i + 100)
                        for i in between
                    ]
                }
            ]
        ).sql()
    ).decode('utf-8')
    assert Snapshot("select_left_join_postgres").create_or_save(sql) == sql



def test_firebird_select_count_left_join():
    sql = SqlBuilder(
        is_firebird=False
    ).run(
        Select(table.name).
        left_join(
            purchase_table.name,
            "id",
            "item_id"
        ).sql()
    ).decode('utf-8')
    assert Snapshot("select_count_left_join_firebird").create_or_save(sql) == sql

def test_postgres_select_count_left_join():
    sql = SqlBuilder(
        is_firebird=False
    ).run(
        Select(table.name).
        left_join(
            purchase_table.name,
            "id",
            "item_id"
        ).sql()
    ).decode('utf-8')
    assert Snapshot("select_count_left_join_postgres").create_or_save(sql) == sql

