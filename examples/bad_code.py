"""
Example Python code with intentional issues for code review demonstration.

This file contains various security vulnerabilities, style issues, and bugs
to demonstrate the capabilities of the code review agent.
"""

def calculate_user_score(user_input):
    # Security Issue: Using eval on user input!
    score = eval(user_input)

    # Style Issue: Using print instead of logging
    print("Calculating score...")

    # Bug: No validation that score is a number
    result = score * 100

    return result


def process_database_query(table, condition):
    # Security Issue: SQL Injection vulnerability
    query = "SELECT * FROM %s WHERE %s" % (table, condition)

    # Bug: No error handling
    result = execute(query)

    return result


def read_config_file(filename="config.txt"):
    # Bug: File operation without 'with' statement (resource leak)
    f = open(filename)
    data = f.read()

    # Bug: File not closed!
    return data


def get_item_from_list(items, index=5):
    # Bug: No bounds checking - potential IndexError
    return items[index]


def divide_numbers(a, b):
    # Bug: No zero division check
    return a / b


# Bug: Mutable default argument!
def append_to_list(item, my_list=[]):
    my_list.append(item)
    return my_list


class UserManager:
    def __init__(self):
        pass

    # Style: Missing docstring
    # Style: Missing type hints
    def create_user(self, name, email):
        user_data = {
            'name': name,
            'email': email
        }

        # Security: Potential pickle vulnerability
        import pickle
        serialized = pickle.dumps(user_data)

        return serialized

    def execute_command(self, cmd):
        # Security: Command injection risk with shell=True
        import subprocess
        result = subprocess.run(cmd, shell=True, capture_output=True)
        return result.stdout


# Style: Magic numbers
def calculate_discount(price):
    if price > 1000:
        return price * 0.15
    elif price > 500:
        return price * 0.10
    else:
        return price * 0.05


# Bug: Catching all exceptions
def risky_operation():
    try:
        # Some operation
        data = fetch_data()
        process(data)
    except:  # Bad: Bare except clause
        pass  # Swallowing errors!


# Missing type hints throughout
# No docstrings for most functions
# Using print() instead of logging module
