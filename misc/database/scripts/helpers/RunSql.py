import os
from subprocess import Popen, PIPE, DEVNULL
import time
import random

def call_firebird_sql(sql, debug=False):
    if type(sql) == str:
        sql = sql.encode('utf-8')
    FBPATH = os.getenv("FBPATH")
    out = (PIPE if debug else DEVNULL)
    isql = Popen([f'{FBPATH}/bin/isql', '-user', 'sysdba'], stderr=out, stdin=PIPE, stdout=out)
    output = isql.communicate(
        sql
    )
    isql.wait(1)
    if debug or isql.returncode != 0:
        print("firebird", sql)
        print("firebird", output)

    assert isql.returncode == 0
    return output

def call_postgres_sql(sql, debug=False):
    if type(sql) == str:
        sql = sql.encode('utf-8')

    out = (PIPE if debug else DEVNULL)
    psql = Popen([f'psql', '-U', 'postgres'], stdin=PIPE, stderr=out, stdout=out)
    output = psql.communicate(
        sql
    )
    psql.wait(1)
    if debug  or psql.returncode != 0:
        print("postgres ", sql)
        print("postgres ", output[0])
    assert psql.returncode == 0
    return output
