# Python Fundamentals

#programming #python #fundamentals #beginner

> **Learning Path**: [[Programming/Python Data Structures]] → [[Programming/Python Control Flow]] → [[Programming/Python Functions]]

## Overview
Python is a versatile, beginner-friendly programming language used for web development, data science, automation, and more. This guide covers the essential building blocks you need to start programming in Python.

## Getting Started

### Development Environment
**IDE (統合開発環境 - とうごうかいはつかんきょう)**: An Integrated Development Environment provides a user-friendly workspace for programmers. Popular Python IDEs include:
- **Replit** (browser-based, great for beginners)
- **Visual Studio Code** (powerful, free)
- **PyCharm** (feature-rich)
- **Komodo** (cross-platform)

### Your First Program
The `print()` function displays text in the terminal:

```python
# This is a comment - Python ignores anything after #
print("Hello, World!")
print("Welcome to Python!")
```

## Variables and Data Types

Variables are named containers that store data in computer memory. Think of them as labeled boxes where you keep information.

### Variable Rules
- Use descriptive names (`student_name` not `x`)
- No spaces (use underscores: `home_team_score`)
- Can't start with numbers (`1st_place` ❌, `first_place` ✅)
- Case sensitive (`Name` ≠ `name`)
- Can't use reserved words (`if`, `for`, `True`, etc.)

### Common Data Types

```python
# Strings (text) - always in quotes
name = "Alice"
message = "Welcome to programming!"

# Integers (whole numbers)
age = 25
score = 100

# Floats (decimal numbers)  
height = 5.8
percentage = 73.81

# Booleans (True/False)
is_student = True
has_license = False
```

### Memory Management
Python automatically manages memory for you. Each value gets stored at a specific memory address (like `id201`), and variables simply point to these locations. You don't need to worry about memory addresses - Python handles this behind the scenes.

## User Input and Output

### Getting Input
```python
# Basic input (always returns a string)
name = input("What's your name? ")
print("Hello, " + name + "!")

# Converting input to numbers
age = int(input("How old are you? "))
height = float(input("How tall are you? "))
```

### Displaying Output
```python
# Print variables
print(name)
print("Your age is:", age)

# Combine text and variables
print("Hello, " + name + "! You are " + str(age) + " years old.")
```

## Basic Operations

### Arithmetic Operations
```python
x = 10
y = 3

sum_result = x + y      # Addition: 13
difference = x - y      # Subtraction: 7  
product = x * y         # Multiplication: 30
quotient = x / y        # Division: 3.333...
remainder = x % y       # Modulus: 1
power = x ** y          # Exponentiation: 1000
```

### String Operations
```python
message = "Hello, World!"

print(len(message))                    # Length: 13
print(message.upper())                 # "HELLO, WORLD!"
print(message.lower())                 # "hello, world!"
print(message.startswith("Hello"))     # True

# String concatenation
greeting = "Hello, " + "Python!"
print(greeting)  # "Hello, Python!"
```

## Key Concepts to Remember

- **Comments** (`#`) help document your code
- **Variables** store data and should have descriptive names
- **Data types** determine what kind of information you're working with
- **Functions** like `print()` and `input()` perform specific tasks
- **String conversion** with `str()` when combining text and numbers

## Common Beginner Mistakes

1. **Forgetting quotes** around strings: `name = Alice` ❌ → `name = "Alice"` ✅
2. **Case sensitivity**: `Print()` ❌ → `print()` ✅  
3. **Not converting input**: `age = input()` gives you text, not a number
4. **Reserved words**: Don't name variables `if`, `for`, `while`, etc.

## Next Steps
Ready to work with multiple values? Head to [[Programming/Python Data Structures]] to learn about lists and dictionaries.

---
*Tags: #programming #python #variables #input-output #basics*  
*Related: [[Programming/Python Data Structures]] | [[Programming/Python Control Flow]]*