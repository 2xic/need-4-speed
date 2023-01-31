
def generate(table, columns, count):
    names = [
        f'{i.name}' for i in columns if not i.generated
    ]
    values = [
        [
            str(i.generate()) for i in columns if not i.generated
        ]
        for _ in range(count)
    ]
    return table.name, names, values
