# Experiment: Implementation of Candidate Elimination Algorithm

# Training Dataset
data = [
    (["Sunny", "Warm", "Normal", "Strong"], "Yes"),   # D1
    (["Sunny", "Warm", "High", "Strong"], "Yes"),     # D2
    (["Rainy", "Cold", "High", "Strong"], "No"),      # D3
    (["Sunny", "Warm", "High", "Weak"], "Yes")        # D4
]

# Initialize Specific and General boundaries
S = ["∅", "∅", "∅", "∅"]
G = [["?", "?", "?", "?"]]


# Function to check whether hypothesis covers an instance
def covers(h, instance):
    for i in range(len(h)):
        if h[i] != "?" and h[i] != instance[i]:
            return False
    return True


# Function to check whether hypothesis h1 is more general than h2
def more_general(h1, h2):
    for i in range(len(h1)):
        if h1[i] != "?" and h1[i] != h2[i]:
            return False
    return True


# Process each training instance
for step, (instance, target) in enumerate(data, start=1):

    print(f"\nAfter processing D{step}: {instance} -> {target}")

    if target == "Yes":

        # Generalize S to cover the positive instance
        for i in range(len(S)):
            if S[i] == "∅":
                S[i] = instance[i]
            elif S[i] != instance[i]:
                S[i] = "?"

        # Remove hypotheses from G that do not cover positive instance
        G = [g for g in G if covers(g, instance)]

    else:

        # Specialize G to exclude the negative instance
        new_G = []

        for g in G:
            if covers(g, instance):

                for i in range(len(g)):
                    if g[i] == "?":
                        # Create specialization using S
                        if S[i] != "∅" and S[i] != instance[i]:
                            new_h = g.copy()
                            new_h[i] = S[i]

                            if covers(new_h, instance) is False:
                                new_G.append(new_h)

            else:
                new_G.append(g)

        G = new_G

        # Remove hypotheses in G that are less general than S
        G = [g for g in G if more_general(g, S)]

    print("Specific Boundary (S):", S)
    print("General Boundary (G):", G)


# Final Version Space
print("\n===================================")
print("FINAL VERSION SPACE")
print("===================================")
print("Specific Boundary (S):", S)
print("General Boundary (G):", G)