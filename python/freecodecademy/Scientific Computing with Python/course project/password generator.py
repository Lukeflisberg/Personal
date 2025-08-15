import re
import secrets
import string


def generate_password(length=100, nums=69, special_chars=10, uppercase=10, lowercase=10):
    # Define the possible characters for the password
    letters = string.ascii_letters
    digits = string.digits
    symbols = string.punctuation
    try_count = 0

    # Combine all characters
    all_characters = letters + digits + symbols

    while True:
        try_count += 1
        password = ''
        # Generate password
        for _ in range(length):
            password += secrets.choice(all_characters)
        
        constraints = [
            (nums, r'\d'),
            (special_chars, fr'[{symbols}]'),
            (uppercase, r'[A-Z]'),
            (lowercase, r'[a-z]')
        ]

        # Check constraints        
        if all(
            constraint <= len(re.findall(pattern, password))
            for constraint, pattern in constraints
        ):
            break
    
    print(f"Nr tries: {try_count}")
    return password

new_password = generate_password()
print('Generated password:', new_password)