class Category:
    def __init__(self, name):
        self.name = name
        self.balance = 0
        self.withdrawals_total = 0
        self.ledger = []

    def deposit(self, amount, description=''):
        self.ledger.append({'amount': amount, 'description': description})
        self.balance += amount

    def withdraw(self, amount, description=''):
        if self.check_funds(amount):
            self.withdrawals_total += amount
            self.ledger.append({'amount': -amount, 'description': description})
            self.balance -= amount
            return True
        return False
    
    def get_balance(self):
        return self.balance

    def transfer(self, amount, category):
        if self.check_funds(amount):
            self.withdraw(amount, f'Transfer to {category.name}')
            category.deposit(amount, f'Transfer from {self.name}')
            return True
        return False
    
    def check_funds(self, amount):
        if self.balance >= amount:
            return True
        return False

    def __str__(self):
        output = []

        # Title formatting
        line_length = 30

        write_length = line_length - len(self.name)
        first = write_length // 2
        second = write_length - first 

        output.append('*'*first + self.name + '*'*second)

        # Ledger formatting
        max_description = 23
        max_amount = 7

        for entry in self.ledger:
            amount = entry['amount']
            description = entry['description']

            format_description = description[:max_description]
            format_amount = f'{amount:.2f}'
            format_amount = format_amount[-max_amount:]

            space_length = line_length - len(format_description) - len(format_amount)

            output.append(format_description + ' '*space_length + format_amount)

        # Total formatting
        output.append(f'Total: {self.balance}')
        # output.append('Total: ' + str(sum([entry['amount'] for entry in self.ledger])))
        
        return '\n'.join(output)

def create_spend_chart(categories):
    total_spent = sum(c.withdrawals_total for c in categories)
    percentages = [int(c.withdrawals_total / total_spent * 100 // 10) * 10 for c in categories]

    lines = ["Percentage spent by category"]

    # Bars
    for i in range(100, -10, -10):
        line = f"{str(i).rjust(3)}|"
        for percent in percentages:
            line += " o " if percent >= i else "   "
        line += " "  # space after last bar
        lines.append(line)

    # Divider
    lines.append("    " + "-" * (3 * len(categories) + 1))

    # Vertical names
    max_len = max(len(c.name) for c in categories)
    names = [c.name.ljust(max_len) for c in categories]  # pad names to equal length

    for i in range(max_len):
        line = "     "
        for j, name in enumerate(names):
            line += name[i]
            if j < len(names) - 1:
                line += "  "  # 2 spaces between categories
            else:
                line += "  "  # 2 spaces after the last category
        lines.append(line)

    return "\n".join(lines)

food = Category("Food")
food.deposit(1000, "deposit")
food.withdraw(500.00, "groceries")

clothing = Category("Clothing")
clothing.deposit(1000, "deposit")
clothing.withdraw(100.00, "buying new clothes")

auto = Category("Auto")
auto.deposit(1000, "deposit")
auto.withdraw(200.00, "fuel")

food.transfer(200, clothing)


categories = [food, clothing, auto]
chart_str = create_spend_chart(categories)

print(clothing)
print(chart_str)