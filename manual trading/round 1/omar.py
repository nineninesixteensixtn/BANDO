import numpy as np
import pandas as pd

# Data setup
data = {
    "snowballs": {"snowballs": 1, "pizzas": 1.45, "nuggets": 0.52, "seashells": 0.72},
    "pizzas": {"snowballs": 0.7, "pizzas": 1, "nuggets": 0.31, "seashells": 0.48},
    "nuggets": {"snowballs": 1.95, "pizzas": 3.1, "nuggets": 1, "seashells": 1.49},
    "seashells": {"snowballs": 1.34, "pizzas": 1.98, "nuggets": 0.64, "seashells": 1}
}
df = pd.DataFrame(data)

# Feel free to edit these
starting_capital = 500
items = ["snowballs", "pizzas", "nuggets", "seashells"]
items_count = len(items)
max_trades = 5

# Global variables don't edit
best_capital = 0
best_path = []

# Rules for trade is that you must start and end with seashells and you trade all available capital
# and maximise profit, 5 trades allowed
    
def search(steps: int = 0, path: list = ["seashells"], current_item: str = "seashells", capital: float = 500):
    global best_capital, best_path

    if steps == max_trades:
        if current_item == "seashells" and capital > best_capital:
            best_capital = capital
            best_path = path[:]
        return
    
    for next_item in items:
        new_capital = capital * df.loc[current_item, next_item]
        new_path = path + [next_item]

        search(steps=steps + 1, path=new_path, current_item=next_item, capital=new_capital)

search()
print("Best final capital in seashells:", best_capital)
print("Best path:", " -> ".join(best_path))