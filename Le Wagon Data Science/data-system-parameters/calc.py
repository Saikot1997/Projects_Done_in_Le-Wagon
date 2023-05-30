# pylint: disable=missing-module-docstring,missing-function-docstring,eval-used
import sys


def main():
    """Implement the calculator"""
    args = sys.argv[1:]
    print(args)
    expression = " ".join(args)
    result = eval(expression)
    return result


if __name__ == "__main__":
    print(main())
