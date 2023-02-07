
def get_foreign_key_constraint(table_name, column, reference_table_name, reference_column, is_firebird):
    if is_firebird:
        return f"ALTER TABLE {table_name} ADD FOREIGN KEY ({column}) REFERENCES {reference_table_name}({reference_column}); "
    else:
        raise Exception("Not added")
