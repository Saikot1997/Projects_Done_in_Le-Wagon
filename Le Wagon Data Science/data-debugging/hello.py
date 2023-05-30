# pylint: disable=missing-docstring

import sys

def full_name(first_name, last_name):
    """returns the full name"""
    if first_name == "" and last_name == "":
        return ""
    if first_name == "":
        name = f"{last_name.capitalize()}"
        return name
    if last_name == "":
        name = f"{first_name.capitalize()}"
        return name
    name = f"{first_name.capitalize()} {last_name.capitalize()}"
    return name

if __name__ == "__main__":
    if len(sys.argv) == 1:
        # => ['hello.py']
        print(f'Hello{full_name("", "")}!')
    elif len(sys.argv) == 2:
        # => ['hello.py', 'John' ]
        print(f'Hello {full_name(sys.argv[1], " ")}!')
    else:
        # => ['hello.py', 'John', 'Lennon']
        print(f"Hello {full_name(sys.argv[1], sys.argv[2])}!")
