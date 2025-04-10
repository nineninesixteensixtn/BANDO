import pandas as pd

data = {
    "Snowballs": {"Snowballs": 1, "Pizza's": 1.45, "Silicon Nuggets": 0.52, "SeaShells": 0.72},
    "Pizza's": {"Snowballs": 0.7, "Pizza's": 1, "Silicon Nuggets": 0.31, "SeaShells": 0.48},
    "Silicon Nuggets": {"Snowballs": 1.95, "Pizza's": 3.1, "Silicon Nuggets": 1, "SeaShells": 1.49},
    "SeaShells": {"Snowballs": 1.34, "Pizza's": 1.98, "Silicon Nuggets": 0.64, "SeaShells": 1}
}

df = pd.DataFrame.from_dict(data, orient="index")

starting_capital = 500
items = df.index.tolist()
max_trades = 5

def search(steps, path, current_item, capital):
    best_capital = 0
    best_path = None
    if current_item == "SeaShells" and steps > 0:
        best_capital = capital
        best_path = path
    if steps == max_trades:
        return best_capital, best_path
    for next_item in items:
        new_cap = capital * df.loc[current_item, next_item]
        new_path = path + [next_item]
        cand_cap, cand_path = search(steps + 1, new_path, next_item, new_cap)
        if cand_cap > best_capital:
            best_capital = cand_cap
            best_path = cand_path
    return best_capital, best_path

opt_cap, opt_path = search(0, ["SeaShells"], "SeaShells", starting_capital)
print("Optimal final capital in SeaShells:", round(opt_cap, 2))
if opt_path:
    print("Optimal path:", " -> ".join(opt_path))
else:
    print("No valid path found")
