from typing import List

def RunInScope(sql: List[str]):
    return "\n".join([
        "SET TERM #;",
        "execute block as ",
        "BEGIN",
        "\n ".join(
            sql
        ),
        "\n",
        "END#",
        "SET TERM ;#",
        "COMMIT;",
    ])
