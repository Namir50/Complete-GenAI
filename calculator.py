def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

def power(a, b):
    return a ** b

def modulo(a, b):
    if b == 0:
        raise ValueError("Cannot perform modulo by zero")
    return a % b

OPERATIONS = {
    "1": ("Addition (+)", add),
    "2": ("Subtraction (-)", subtract),
    "3": ("Multiplication (*)", multiply),
    "4": ("Division (/)", divide),
    "5": ("Power (^)", power),
    "6": ("Modulo (%)", modulo),
}

def get_number(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a number.")

def main():
    print("=== Python Calculator ===")
    while True:
        print("\nOperations:")
        for key, (name, _) in OPERATIONS.items():
            print(f"  {key}. {name}")
        print("  q. Quit")

        choice = input("\nSelect an operation: ").strip().lower()
        if choice == "q":
            print("Goodbye!")
            break

        if choice not in OPERATIONS:
            print("Invalid choice. Try again.")
            continue

        a = get_number("Enter first number: ")
        b = get_number("Enter second number: ")

        try:
            result = OPERATIONS[choice][1](a, b)
            print(f"Result: {result}")
        except ValueError as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
