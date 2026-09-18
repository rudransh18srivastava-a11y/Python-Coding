#!/usr/bin/env python3
"""
Scientific Calculator
----------------------
A command-line scientific calculator supporting basic arithmetic plus
trigonometry, logarithms, powers, roots, and more.

Run it with:
    python3 scientific_calculator.py
"""

import math

# Names allowed inside eval() -- keeps the calculator safe from
# executing arbitrary Python code.
SAFE_NAMES = {
    'abs': abs, 'round': round,
    'pi': math.pi, 'e': math.e, 'tau': math.tau,
    'sqrt': math.sqrt, 'cbrt': lambda x: math.copysign(abs(x) ** (1 / 3), x),
    'log': math.log, 'log10': math.log10, 'log2': math.log2,
    'exp': math.exp, 'pow': math.pow,
    'factorial': math.factorial,
    'sin': math.sin, 'cos': math.cos, 'tan': math.tan,
    'asin': math.asin, 'acos': math.acos, 'atan': math.atan, 'atan2': math.atan2,
    'sinh': math.sinh, 'cosh': math.cosh, 'tanh': math.tanh,
    'degrees': math.degrees, 'radians': math.radians,
    'floor': math.floor, 'ceil': math.ceil,
    'gcd': math.gcd,
}


class Calculator:
    def __init__(self):
        self.angle_mode = 'rad'  # 'rad' or 'deg'
        self.history = []

    def set_angle_mode(self, mode):
        mode = mode.strip().lower()
        if mode in ('rad', 'deg'):
            self.angle_mode = mode
            print(f"Angle mode set to {'radians' if mode == 'rad' else 'degrees'}.")
        else:
            print("Invalid mode. Use 'mode rad' or 'mode deg'.")

    def _namespace(self):
        ns = dict(SAFE_NAMES)
        if self.angle_mode == 'deg':
            ns['sin'] = lambda x: math.sin(math.radians(x))
            ns['cos'] = lambda x: math.cos(math.radians(x))
            ns['tan'] = lambda x: math.tan(math.radians(x))
            ns['asin'] = lambda x: math.degrees(math.asin(x))
            ns['acos'] = lambda x: math.degrees(math.acos(x))
            ns['atan'] = lambda x: math.degrees(math.atan(x))
        return ns

    def evaluate(self, expression):
        expr = expression.replace('^', '**')  # allow ^ for power
        try:
            ns = self._namespace()
            ns['__builtins__'] = {}
            result = eval(expr, ns, {})
            self.history.append((expression, result))
            return result
        except ZeroDivisionError:
            raise ValueError("Error: division by zero")
        except (SyntaxError, NameError) as exc:
            raise ValueError(f"Error: invalid expression ({exc})")
        except Exception as exc:
            raise ValueError(f"Error: {exc}")


HELP_TEXT = """
Scientific Calculator - Commands
---------------------------------
Type any math expression to evaluate it, e.g.:
    2 + 3 * 4
    sin(30)                (uses the current angle mode)
    sqrt(16) + log10(100)
    2^10                   (power, same as 2**10)
    factorial(5)

Available functions:
    sqrt, cbrt, exp, log, log10, log2, pow
    sin, cos, tan, asin, acos, atan, atan2
    sinh, cosh, tanh
    factorial, floor, ceil, gcd, abs, round, degrees, radians

Constants:
    pi, e, tau

Commands:
    mode deg     - switch angle mode to degrees
    mode rad     - switch angle mode to radians (default)
    history      - show calculation history
    clear        - clear the screen
    help         - show this help message
    quit / exit  - close the calculator
"""


def main():
    calc = Calculator()
    print("=" * 50)
    print("        SCIENTIFIC CALCULATOR")
    print("=" * 50)
    print("Type 'help' for instructions, 'quit' to exit.\n")

    while True:
        try:
            user_input = input(f"[{calc.angle_mode}] >> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not user_input:
            continue

        cmd = user_input.lower()

        if cmd in ('quit', 'exit', 'q'):
            print("Goodbye!")
            break
        elif cmd == 'help':
            print(HELP_TEXT)
        elif cmd == 'clear':
            print("\n" * 50)
        elif cmd == 'history':
            if not calc.history:
                print("No history yet.")
            else:
                for i, (expr, res) in enumerate(calc.history, 1):
                    print(f"  {i}. {expr} = {res}")
        elif cmd.startswith('mode '):
            calc.set_angle_mode(cmd.split(' ', 1)[1])
        else:
            try:
                result = calc.evaluate(user_input)
                print(f"= {result}")
            except ValueError as exc:
                print(exc)


if __name__ == "__main__":
    main()
