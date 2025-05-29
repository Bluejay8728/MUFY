def calculate(a, operation, b):
    if operation == "+":
        return a + b
    elif operation =="-":
        return a - b
    elif operation == "*":
        return a * b
    elif operation == "/":
        return a / b
    else:
        return "Invalid operation"
print(calculate(10, "+", 10))
print(calculate(10, "-", 10))
print(calculate(10, "*", 10))
print(calculate(10, "/", 10))