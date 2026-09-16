import csv

# Initial hypothesis
hypothesis = ["∅", "∅", "∅", "∅", "∅"]

# Open CSV file
with open("workload_data.csv", "r", newline="", encoding="utf-8-sig") as file:

    reader = csv.reader(file)

    # Skip the header row
    header = next(reader)

    # Process each row
    for row in reader:

        instance = row[:5]
        target = row[5]

        # Process only positive examples
        if target == "Yes":

            # First positive example
            if hypothesis[0] == "∅":
                hypothesis = instance.copy()

            else:
                # Generalize hypothesis
                for i in range(5):
                    if hypothesis[i] != instance[i]:
                        hypothesis[i] = "?"

        # Print after every row
        print("Instance:", instance)
        print("Target:", target)
        print("Hypothesis:", hypothesis)
        print("-" * 50)

# Final hypothesis
print("Final Most Specific Hypothesis:")
print(hypothesis)