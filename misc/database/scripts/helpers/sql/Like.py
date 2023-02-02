

class Like:
    def __init__(self, value) -> None:
        # TODO: Fix this, it should not do this here.
        self.value = value.replace("'", "")

    def sql(self, column):
        return f"{column} like '%{self.value}%'"
