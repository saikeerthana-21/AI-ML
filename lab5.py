import math
import matplotlib.pyplot as plt


# Training dataset
data = [
    {"Day": "D1", "Outlook": "Sunny", "Temperature": "Hot", "Humidity": "High", "Wind": "Weak", "Play Tennis": "No"},
    {"Day": "D2", "Outlook": "Sunny", "Temperature": "Hot", "Humidity": "High", "Wind": "Strong", "Play Tennis": "No"},
    {"Day": "D3", "Outlook": "Overcast", "Temperature": "Hot", "Humidity": "High", "Wind": "Weak", "Play Tennis": "Yes"},
    {"Day": "D4", "Outlook": "Rain", "Temperature": "Mild", "Humidity": "High", "Wind": "Weak", "Play Tennis": "Yes"},
    {"Day": "D5", "Outlook": "Rain", "Temperature": "Cool", "Humidity": "Normal", "Wind": "Weak", "Play Tennis": "Yes"},
    {"Day": "D6", "Outlook": "Rain", "Temperature": "Cool", "Humidity": "Normal", "Wind": "Strong", "Play Tennis": "No"},
    {"Day": "D7", "Outlook": "Overcast", "Temperature": "Cool", "Humidity": "Normal", "Wind": "Strong", "Play Tennis": "Yes"},
    {"Day": "D8", "Outlook": "Sunny", "Temperature": "Mild", "Humidity": "High", "Wind": "Weak", "Play Tennis": "No"},
    {"Day": "D9", "Outlook": "Sunny", "Temperature": "Cool", "Humidity": "Normal", "Wind": "Weak", "Play Tennis": "Yes"},
    {"Day": "D10", "Outlook": "Rain", "Temperature": "Mild", "Humidity": "Normal", "Wind": "Weak", "Play Tennis": "Yes"},
    {"Day": "D11", "Outlook": "Sunny", "Temperature": "Mild", "Humidity": "Normal", "Wind": "Strong", "Play Tennis": "Yes"},
    {"Day": "D12", "Outlook": "Overcast", "Temperature": "Mild", "Humidity": "High", "Wind": "Strong", "Play Tennis": "Yes"},
    {"Day": "D13", "Outlook": "Overcast", "Temperature": "Hot", "Humidity": "Normal", "Wind": "Weak", "Play Tennis": "Yes"},
    {"Day": "D14", "Outlook": "Rain", "Temperature": "Mild", "Humidity": "High", "Wind": "Strong", "Play Tennis": "No"}
]

target = "Play Tennis"
attributes = ["Outlook", "Temperature", "Humidity", "Wind"]


# -------------------------------------------------
# ENTROPY
# -------------------------------------------------

def entropy(rows):

    total = len(rows)

    if total == 0:
        return 0

    counts = {}

    for row in rows:
        label = row[target]
        counts[label] = counts.get(label, 0) + 1

    result = 0

    for count in counts.values():
        probability = count / total
        result -= probability * math.log2(probability)

    return result


# -------------------------------------------------
# INFORMATION GAIN
# -------------------------------------------------

def information_gain(rows, attribute):

    total_entropy = entropy(rows)
    total = len(rows)

    values = set(row[attribute] for row in rows)

    weighted_entropy = 0

    for value in values:

        subset = [
            row for row in rows
            if row[attribute] == value
        ]

        weighted_entropy += (
            len(subset) / total
        ) * entropy(subset)

    return total_entropy - weighted_entropy


# -------------------------------------------------
# ID3 DECISION TREE
# -------------------------------------------------

def id3(rows, remaining_attributes):

    labels = [row[target] for row in rows]

    # All records belong to same class
    if len(set(labels)) == 1:
        return labels[0]

    # No attributes remain
    if not remaining_attributes:
        return max(set(labels), key=labels.count)

    # Find best attribute
    best_attribute = max(
        remaining_attributes,
        key=lambda attribute:
        information_gain(rows, attribute)
    )

    tree = {
        best_attribute: {}
    }

    values = set(
        row[best_attribute]
        for row in rows
    )

    for value in values:

        subset = [
            row for row in rows
            if row[best_attribute] == value
        ]

        new_attributes = [
            attribute
            for attribute in remaining_attributes
            if attribute != best_attribute
        ]

        tree[best_attribute][value] = id3(
            subset,
            new_attributes
        )

    return tree


# -------------------------------------------------
# PRINT TREE
# -------------------------------------------------

def print_tree(tree, indent=""):

    if not isinstance(tree, dict):
        print(indent + "-> " + tree)
        return

    attribute = next(iter(tree))

    print(indent + attribute + "?")

    for value, subtree in tree[attribute].items():

        print(indent + "|-- " + value)

        print_tree(
            subtree,
            indent + "|   "
        )


# -------------------------------------------------
# DRAW TREE AS IMAGE
# -------------------------------------------------

def draw_tree(tree):

    fig, ax = plt.subplots(figsize=(12, 7))

    ax.axis("off")

    # Store node positions
    positions = {}

    # Find the width of each level
    def count_leaves(node):

        if not isinstance(node, dict):
            return 1

        attribute = next(iter(node))

        total = 0

        for child in node[attribute].values():
            total += count_leaves(child)

        return total

    # Assign positions
    def assign_positions(node, depth=0, left=0):

        if not isinstance(node, dict):
            return left + 0.5

        attribute = next(iter(node))

        children = list(node[attribute].items())

        child_centers = []

        current_left = left

        for value, child in children:

            leaves = count_leaves(child)

            center = assign_positions(
                child,
                depth + 1,
                current_left
            )

            child_centers.append(
                (value, child, center)
            )

            current_left += leaves

        center = (
            child_centers[0][2] +
            child_centers[-1][2]
        ) / 2

        positions[id(node)] = (
            center,
            depth
        )

        return center

    assign_positions(tree)

    # Draw nodes and connections
    def draw_nodes(node, depth=0):

        if not isinstance(node, dict):
            return

        attribute = next(iter(node))

        x, y = positions[id(node)]

        # Draw decision node
        ax.text(
            x,
            -y,
            attribute,
            ha="center",
            va="center",
            fontsize=14,
            fontweight="bold",
            bbox=dict(
                boxstyle="round,pad=0.5",
                facecolor="lightblue",
                edgecolor="black"
            )
        )

        children = list(node[attribute].items())

        current_left = 0

        for value, child in children:

            leaves = count_leaves(child)

            # Get child position
            if isinstance(child, dict):

                child_x, child_y = positions[id(child)]

            else:

                child_x = (
                    x - sum(
                        count_leaves(c)
                        for _, c in children
                    ) / 2
                    + current_left
                    + leaves / 2
                )

                child_y = depth + 1

            # Draw child leaf
            if not isinstance(child, dict):

                ax.text(
                    child_x,
                    -child_y,
                    child,
                    ha="center",
                    va="center",
                    fontsize=13,
                    fontweight="bold",
                    bbox=dict(
                        boxstyle="round,pad=0.5",
                        facecolor="lightgreen"
                        if child == "Yes"
                        else "lightcoral",
                        edgecolor="black"
                    )
                )

            # Draw connecting line
            ax.plot(
                [x, child_x],
                [-depth, -child_y],
                "k-"
            )

            # Branch label
            mid_x = (x + child_x) / 2
            mid_y = (-depth - child_y) / 2

            ax.text(
                mid_x,
                mid_y + 0.08,
                str(value),
                fontsize=11,
                ha="center"
            )

            # Recursively draw child
            if isinstance(child, dict):
                draw_nodes(
                    child,
                    depth + 1
                )

            current_left += leaves

    draw_nodes(tree)

    plt.title(
        "ID3 Decision Tree - Play Tennis",
        fontsize=18,
        fontweight="bold"
    )

    plt.tight_layout()

    # Save image
    plt.savefig(
        "ID3_Decision_Tree.png",
        dpi=300,
        bbox_inches="tight"
    )

    # Show image
    plt.show()

    print("\nDecision tree image created!")
    print("Saved as: ID3_Decision_Tree.png")


# -------------------------------------------------
# MAIN PROGRAM
# -------------------------------------------------

print("ENTROPY OF COMPLETE DATASET:")
print(f"{entropy(data):.3f}")


print("\nINFORMATION GAIN:")

for attribute in attributes:

    gain = information_gain(
        data,
        attribute
    )

    print(
        f"{attribute}: {gain:.3f}"
    )


# Build ID3 tree
tree = id3(
    data,
    attributes
)


print("\nFINAL ID3 DECISION TREE:")

print_tree(tree)


# Create graphical tree
draw_tree(tree)