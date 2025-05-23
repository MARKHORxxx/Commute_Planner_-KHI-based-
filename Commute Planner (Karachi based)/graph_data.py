# graph_data.py

karachi_graph = {
    'Gulshan': {'Johar': 7, 'Saddar': 12},
    'Johar': {'Gulshan': 7, 'Malir': 10},
    'Saddar': {'Gulshan': 12, 'Clifton': 5, 'Korangi': 8},
    'Clifton': {'Saddar': 5, 'DHA': 4},
    'Malir': {'Johar': 10, 'Landhi': 6},
    'Landhi': {'Malir': 6, 'Korangi': 4},
    'Korangi': {'Landhi': 4, 'Saddar': 8},
    'DHA': {'Clifton': 4}
}

# Heuristic values (straight-line distances to destination - for A* guidance)
heuristic = {
    'Gulshan': 12,
    'Johar': 10,
    'Saddar': 6,
    'Clifton': 3,
    'Malir': 14,
    'Landhi': 10,
    'Korangi': 8,
    'DHA': 0  # Let's say DHA is always the destination
}
