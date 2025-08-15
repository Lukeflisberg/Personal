import re
import secrets
import string


def generate_password(length=100, nums=69, special_chars=10, uppercase=10, lowercase=10):
    # Define the possible characters for the password
    letters = string.ascii_letters
    digits = string.digits
    symbols = string.punctuation

    # Combine all characters
    all_characters = letters + digits + symbols
    password = ''

    constraints = [
            (nums, r'\d'),
            (special_chars, fr'[{symbols}]'),
            (uppercase, r'[A-Z]'),
            (lowercase, r'[a-z]')
        ]
    
    for _ in range(length):
        while True:
            choice = secrets.choice(all_characters)

            if all(
                constraint > len(re.findall(pattern, password + choice)) for constraint, pattern in constraints
            ):
                password += choice
                break
    
    return password

new_password = generate_password()
print('Generated password:', new_password)