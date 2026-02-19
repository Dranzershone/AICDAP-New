import pandas as pd

# Load full files
nodes = pd.read_csv("nodes.csv")
edges = pd.read_csv("edges.csv")

# Select first N users
N = 10
selected_users = (
    nodes[nodes["Type"] == "user"]
    .head(N)["Id"]
    .tolist()
)

# Keep edges where user is source or target
filtered_edges = edges[
    edges["Source"].isin(selected_users) |
    edges["Target"].isin(selected_users)
]

# Keep only nodes that appear in filtered edges
connected_nodes = set(filtered_edges["Source"]) | set(filtered_edges["Target"])
filtered_nodes = nodes[nodes["Id"].isin(connected_nodes)]

# Save reduced files
filtered_nodes.to_csv("nodes_small.csv", index=False)
filtered_edges.to_csv("edges_small.csv", index=False)

print("Reduced graph saved as nodes_small.csv & edges_small.csv")