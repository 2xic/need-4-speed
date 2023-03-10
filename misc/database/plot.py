import json
import matplotlib.pyplot as plt
import os

root = os.path.dirname(__file__)

def join(paths):
    return list(map(lambda x: os.path.join(root, x), paths))

for i in join([
    "output/insert.json",
    "output/select_like_text.json",
    "output/select_greater_than_less_than.json",
    "output/select_join.json",
    "output/select_left_join.json",
]):
    print(i)
    with open(i, "r") as file:
        data = json.load(file)
        plt.plot(data['x'], data['firebird'], label='firebird', color="orange")
        plt.plot(data['x'], data['postgres'], label='postgres', color="blue")
        plt.xlabel('Rows in table when running query')
        plt.ylabel('Time to respond (in seconds)')
        plt.title(data['description'])
        plt.legend(loc="upper left")
        plt.savefig(
            (join([f"plots/{data['name']}"]))[0]
        )
        plt.clf()

for i in join([
    "output/firebird_update_operator.json",
]):
    print(i)
    with open(i, "r") as file:
        data = json.load(file)
        plt.plot(data['x'], data['operator_1'], label=data['operator_1_name'], color="orange")
        plt.plot(data['x'], data['operator_2'], label=data['operator_2_name'], color="red")
        plt.xlabel('Rows in table when running query')
        plt.ylabel('Time to respond (in seconds)')
        plt.title(data['description'])
        plt.legend(loc="upper left")
        plt.savefig(
            (join([f"plots/{data['name']}"]))[0]
        )
        plt.clf()
