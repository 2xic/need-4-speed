import os
from subprocess import Popen, PIPE, DEVNULL
import time
import random

def call_firebird_sql(sql, debug=False):
    if type(sql) == str:
        sql = sql.encode('utf-8')
   # print(sql)
    FBPATH = os.getenv("FBPATH")
    out = (PIPE if debug else DEVNULL)
    isql = Popen([f'{FBPATH}/bin/isql', '-user', 'sysdba'], stderr=out, stdin=PIPE, stdout=out)
    output = isql.communicate(
        sql
    )
    isql.wait(3)
    if debug:
        print("firebird", sql)
        print("firebird", output)
    return output # "".join(list(list(filter(lambda x: x is not None, output))))

def call_postgres_sql(sql, debug=False):
    if type(sql) == str:
        sql = sql.encode('utf-8')

    #sql = sql.replace("CONNECT 'test_database';", "")
    out = (PIPE if debug else DEVNULL)
    psql = Popen([f'psql', '-U', 'postgres'], stdin=PIPE, stderr=out, stdout=out)
    output = psql.communicate(
        sql
    )
    if debug:
        print("postgres ", sql)
        print("postgres ", output)
    psql.wait(3)
    return output
