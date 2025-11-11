# Python Functions

#programming #python #functions #modules #code-organization

> **Prerequisites**: [[Programming/Python Control Flow]]  
> **Next**: [[Programming/Python Advanced Topics]]

## Overview
Functions are reusable blocks of code that perform specific tasks. Think of them as 機能 (きのう - kinou) - tools in your programming toolbox that you can use whenever needed without rewriting code.

## Why Use Functions?

**Without Functions** (repetitive):
```python
print("Hello, Alice!")
print("Hello, Bob!")
print("Hello, Charlie!")
```

**With Functions** (efficient):
```python
def greet(name):
    print(f"Hello, {name}!")

greet("Alice")
greet("Bob") 
greet("Charlie")
```

**Benefits:**
- **Reusability**: Write once, use many times
- **Organization**: Break complex problems into smaller pieces  
- **Maintainability**: Fix bugs in one place
- **Readability**: Code becomes self-documenting

## Defining Functions

### Basic Function Structure
```python
def function_name(parameters):
    """Optional docstring explaining what the function does"""
    # Function body
    # Code to execute
    return result  # Optional
```

### Simple Functions
```python
def say_hello():
    """Prints a greeting message"""
    print("Hello, World!")
    print("Welcome to Python!")

# Call the function
say_hello()
```

### Functions with Parameters
```python
def greet_person(name, age):
    """Greet someone with their name and age"""
    print(f"Hello, {name}!")
    print(f"You are {age} years old.")

# Call with arguments
greet_person("Alice", 25)
greet_person("Bob", 30)
```

## Return Values

Functions can send data back to the caller using `return`:

### Functions That Return Values
```python
def add_numbers(x, y):
    """Add two numbers and return the result"""
    result = x + y
    return result

# Store the returned value
sum_result = add_numbers(5, 3)
print(f"5 + 3 = {sum_result}")  # Output: 5 + 3 = 8

# Use directly in expressions
total = add_numbers(10, 20) + add_numbers(5, 15)
print(f"Total: {total}")  # Output: Total: 50
```

### Multiple Return Values
```python
def calculate_stats(numbers):
    """Calculate min, max, and average of a list"""
    minimum = min(numbers)
    maximum = max(numbers)
    average = sum(numbers) / len(numbers)
    
    return minimum, maximum, average

# Unpack the returned tuple
min_val, max_val, avg_val = calculate_stats([1, 2, 3, 4, 5])
print(f"Min: {min_val}, Max: {max_val}, Avg: {avg_val}")
```

### Early Returns
```python
def check_password(password):
    """Validate a password"""
    if len(password) < 8:
        return "Password too short"
    
    if not any(c.isupper() for c in password):
        return "Password needs uppercase letter"
        
    if not any(c.isdigit() for c in password):
        return "Password needs a number"
    
    return "Password is valid"

result = check_password("mypass123")
print(result)
```

## Advanced Function Features

### Default Parameters
```python
def create_profile(name, age=18, city="Unknown"):
    """Create a user profile with default values"""
    return f"Name: {name}, Age: {age}, City: {city}"

# Different ways to call
print(create_profile("Alice"))                    # Uses defaults
print(create_profile("Bob", 25))                  # Overrides age
print(create_profile("Charlie", city="Tokyo"))    # Named parameter
print(create_profile("Diana", 30, "Paris"))       # All parameters
```

### Variable-Length Arguments
```python
def calculate_average(*numbers):
    """Calculate average of any number of arguments"""
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

print(calculate_average(5, 10, 15))           # 10.0
print(calculate_average(1, 2, 3, 4, 5, 6))   # 3.5
```

### Keyword Arguments
```python
def format_name(**kwargs):
    """Format a name from keyword arguments"""
    first = kwargs.get('first', '')
    last = kwargs.get('last', '')
    middle = kwargs.get('middle', '')
    
    if middle:
        return f"{first} {middle} {last}"
    else:
        return f"{first} {last}"

print(format_name(first="John", last="Doe"))
print(format_name(first="Jane", middle="Marie", last="Smith"))
```

## Practical Examples

### Calculator Functions
```python
def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    if y == 0:
        return "Error: Cannot divide by zero"
    return x / y

# Simple calculator
while True:
    operation = input("Enter operation (+, -, *, /) or 'quit': ")
    
    if operation == 'quit':
        break
        
    if operation in ['+', '-', '*', '/']:
        num1 = float(input("Enter first number: "))
        num2 = float(input("Enter second number: "))
        
        if operation == '+':
            result = add(num1, num2)
        elif operation == '-':
            result = subtract(num1, num2)
        elif operation == '*':
            result = multiply(num1, num2)
        elif operation == '/':
            result = divide(num1, num2)
            
        print(f"Result: {result}")
    else:
        print("Invalid operation")
```

### Text Processing Functions
```python
def clean_text(text):
    """Clean and normalize text"""
    # Remove extra whitespace and convert to lowercase
    return text.strip().lower()

def count_words(text):
    """Count words in a text"""
    words = text.split()
    return len(words)

def extract_emails(text):
    """Extract email-like patterns from text"""
    words = text.split()
    emails = []
    for word in words:
        if '@' in word and '.' in word:
            emails.append(word)
    return emails

# Usage
sample_text = "  Contact us at: admin@example.com or support@test.org  "
clean = clean_text(sample_text)
word_count = count_words(clean)
emails = extract_emails(clean)

print(f"Clean text: {clean}")
print(f"Word count: {word_count}")
print(f"Emails found: {emails}")
```

## Modules and Libraries

Python's power comes from its extensive library ecosystem. Import functionality from modules:

### Built-in Modules
```python
import random
import math
from datetime import datetime

# Random number generation
random_num = random.randint(1, 10)
print(f"Random number: {random_num}")

# Mathematical functions  
sqrt_value = math.sqrt(16)
print(f"Square root of 16: {sqrt_value}")

# Date and time
now = datetime.now()
print(f"Current time: {now}")
```

### Popular Third-Party Libraries
```python
# These require installation: pip install package_name

# requests - for web APIs
import requests
response = requests.get("https://api.github.com/users/octocat")

# pandas - for data analysis
import pandas as pd
data = pd.read_csv("data.csv")

# matplotlib - for plotting
import matplotlib.pyplot as plt
plt.plot([1, 2, 3, 4], [1, 4, 9, 16])
```

## Function Best Practices

### 1. Single Responsibility
Each function should do one thing well:
```python
# ❌ Bad - function does too many things
def process_user_data(name, email, age):
    print(f"Processing {name}")
    validate_email(email)
    save_to_database(name, email, age)
    send_welcome_email(email)
    return "Success"

# ✅ Good - separate concerns
def validate_user_data(name, email, age):
    """Only validate data"""
    # validation logic
    
def save_user(name, email, age):
    """Only save to database"""
    # saving logic
    
def send_welcome_email(email):
    """Only send email"""
    # email logic
```

### 2. Clear Naming
Function names should describe what they do:
```python
# ❌ Bad names
def calc(x, y):
def process(data):
def do_stuff():

# ✅ Good names  
def calculate_average(numbers):
def validate_email_format(email):
def format_phone_number(phone):
```

### 3. Documentation
```python
def calculate_compound_interest(principal, rate, time, compound_frequency=1):
    """
    Calculate compound interest.
    
    Args:
        principal (float): Initial amount of money
        rate (float): Annual interest rate (as decimal, e.g., 0.05 for 5%)
        time (float): Time in years
        compound_frequency (int): Number of times interest compounds per year
        
    Returns:
        float: Final amount after compound interest
        
    Example:
        >>> calculate_compound_interest(1000, 0.05, 2)
        1102.5
    """
    amount = principal * (1 + rate/compound_frequency) ** (compound_frequency * time)
    return round(amount, 2)
```

## Common Patterns

### Error Handling in Functions
```python
def safe_divide(x, y):
    """Safely divide two numbers"""
    try:
        result = x / y
        return result
    except ZeroDivisionError:
        return "Error: Division by zero"
    except TypeError:
        return "Error: Invalid number types"
```

### Function Factories
```python
def create_multiplier(factor):
    """Create a function that multiplies by a specific factor"""
    def multiplier(x):
        return x * factor
    return multiplier

# Create specialized functions
double = create_multiplier(2)
triple = create_multiplier(3)

print(double(5))  # 10
print(triple(5))  # 15
```

## Next Steps
Ready to level up? Explore [[Programming/Python Advanced Topics]] covering classes, file handling, error management, and more advanced concepts.

---
*Tags: #programming #python #functions #modules #code-organization*  
*Related: [[Programming/Python Control Flow]] | [[Programming/Python Advanced Topics]] | [[Programming/Python Data Structures]]*