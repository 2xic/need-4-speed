import random

random.seed(10)

class Column:
    def __init__(self, name, type, generate=False, create_index=False) -> None:
        self.name = name
        self.type = type
        assert type in [str, int]

        self.varchar_length = 128
        self.generated = (self.name  == "id" or generate)
        self.create_index = create_index

    def set_length(self, varchar_length):
        self.varchar_length = varchar_length
        return self

    def index(self, table):
        if self.create_index:
            return f"CREATE UNIQUE INDEX UNQ_{self.name} ON {table} ({self.name});"
        return ""

    def get_additional_sql(self, table_name, is_firebird):
        """
        This should be equivalent with what we are currently doing ...
        """
        if (self.name == "id" and is_firebird) and False:
            return f"ALTER TABLE {table_name} ADD PRIMARY KEY ({self.name}); "
        return None

    def sql(self, is_firebird):
        if self.generated:
            if is_firebird:
                return f"{self.name} INTEGER generated by default as identity primary key"
            else:
                return f"{self.name} SERIAL PRIMARY KEY"
        elif self.type == str:
            return f"{self.name} VARCHAR({self.varchar_length})"
        elif self.type == int:
            return f"{self.name} INTEGER"
        else:
            raise Exception("Unknown")

    def generate(self):
        if self.type == str:
            words = "".join([
                chr(random.randint(65, 65 + 20)) for i in range(self.varchar_length - 1)
            ])
            return f"'{words}'"
        else:
            return random.randint(100, 1000)
