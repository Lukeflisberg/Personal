import secrets

class RandomSelector:
    def __init__(self, items, display=3, attempts=10, div=1):
        self.items = items
        self.attempts = attempts
        self.display = display
        self.div = div
        self.results = {}

    def populate_random(self): 
        if not self.items:
            raise ValueError("Item list is empty.")
        self.results = {item: 0 for item in self.items}
        for _ in range(self.attempts):
            self.results[secrets.choice(self.items)] += 1

    def get_results(self): 
        # Only show items with count perfectly divisible by div and not zero
        filtered = [
            (item, count)
            for item, count in self.results.items()
            if count != 0 and count % self.div == 0
        ]
        filtered.sort(key=lambda x: x[1], reverse=True)
        top_items = filtered[:self.display]
        return "\n".join(
            f"{i+1}. \"{item}\" appeared {count} times"
            for i, (item, count) in enumerate(top_items)
        )

def varify(variable, fail_value):
    if not variable.isdigit() or int(variable) <= 0:
        return fail_value
    return int(variable)

if __name__ == "__main__":
    c_0 = input("Numbers[0] or Names[1]: ")

    if c_0 == "0":
        low = input("Low: ")
        high = input("High: ")
        items = [str(i) for i in range(int(low), int(high) + 1)]
    elif c_0 == "1":
        items = [name.strip() for name in input("Names (comma separated): ").split(",")]
    else:
        items = []
    
    display = varify(input("Display: "), 3)
    attempts = varify(input("Attempts: "), 10)
    div = varify(input("Div: "), 1)

    selector = RandomSelector(items, display, attempts, div)
    selector.populate_random()
    print(selector.get_results())