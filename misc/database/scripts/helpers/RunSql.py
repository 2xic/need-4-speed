import os
from subprocess import Popen, PIPE, DEVNULL
from .clear_space import trim_space

def call_firebird_sql(sql, debug=False):
    if type(sql) == str:
        sql = sql.encode('utf-8')
    FBPATH = os.getenv("FBPATH")
    out = (PIPE if debug else DEVNULL)
    isql = Popen([f'{FBPATH}/bin/isql', '-user', 'sysdba'], stderr=out, stdin=PIPE, stdout=out)
    output = isql.communicate(
        sql,
        timeout=10
    )
#    isql.wait(3)
    if debug or isql.returncode != 0:
      #  print("firebird", sql)
#        print("firebird", output)

        if "count(*)" in sql.decode('utf-8'):
            print("firebird rows: ", output[0].decode("utf-8").split("\n")[3])
        else:
            print("firebird sql", sql)
            print("firebird", output)

    if output[0] is None:
        print("NONE", sql)
        print(output)

    if "count(*)" in sql.decode('utf-8'):
        return trim_space(output[0].decode("utf-8").split("\n")[3])

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
       # print("postgres ", sql)
        if "count(*)" in sql.decode('utf-8'):
            print("postgres rows: ", output[0].decode("utf-8").split("\n")[2])
            print("")
    assert psql.returncode == 0
    if "count(*)" in sql.decode('utf-8'):
        return trim_space(output[0].decode("utf-8").split("\n")[2])
    return output
