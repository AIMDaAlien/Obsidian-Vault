# Python Advanced Topics

#programming #python #advanced #error-handling #file-io #modules #walrus-operator

> **Prerequisites**: [[Programming/Python Functions]]  
> **See Also**: [[Programming/Python Fundamentals]] | [[Programming/Computer Science Concepts]]

## Overview
Advanced Python concepts that take your programming to the next level. These topics help you write more robust, efficient, and professional code.

## Error Handling

### The Problem
Programs often encounter unexpected situations: files don't exist, users enter invalid input, network connections fail. Without proper handling, your program crashes.

### Try-Except Blocks
Handle errors gracefully instead of crashing:

```python
def get_user_age():
    """Get user age with error handling"""
    while True:
        try:
            age = int(input("Enter your age: "))
            if age < 0:
                print("Age cannot be negative!")
                continue
            return age
        except ValueError:
            print("Please enter a valid number!")
        except KeyboardInterrupt:
            print("\nProgram interrupted by user")
            return None

age = get_user_age()
if age is not None:
    print(f"You are {age} years old")
```

### Exception Types
```python
def demonstrate_exceptions():
    """Show different types of exceptions"""
    
    # ValueError - wrong value type
    try:
        number = int("not_a_number")
    except ValueError as e:
        print(f"ValueError: {e}")
    
    # ZeroDivisionError - division by zero
    try:
        result = 10 / 0
    except ZeroDivisionError as e:
        print(f"ZeroDivisionError: {e}")
    
    # KeyError - dictionary key doesn't exist
    try:
        data = {"name": "Alice"}
        print(data["age"])
    except KeyError as e:
        print(f"KeyError: {e}")
    
    # IndexError - list index out of range
    try:
        numbers = [1, 2, 3]
        print(numbers[10])
    except IndexError as e:
        print(f"IndexError: {e}")

demonstrate_exceptions()
```

### Finally Blocks
Code that always runs, regardless of errors:

```python
def read_config_file():
    """Read configuration with proper cleanup"""
    file_handle = None
    try:
        file_handle = open("config.txt", "r")
        config_data = file_handle.read()
        return config_data
    except FileNotFoundError:
        print("Config file not found, using defaults")
        return "default_config"
    except PermissionError:
        print("Permission denied to read config file")
        return None
    finally:
        # This always runs
        if file_handle:
            file_handle.close()
            print("File closed successfully")
```

## File Handling

### Reading Files
```python
def read_text_file(filename):
    """Read and return contents of a text file"""
    try:
        with open(filename, "r", encoding="utf-8") as file:
            content = file.read()
            return content
    except FileNotFoundError:
        print(f"File '{filename}' not found")
        return None
    except PermissionError:
        print(f"Permission denied to read '{filename}'")
        return None

# Read line by line (better for large files)
def read_file_lines(filename):
    """Read file line by line"""
    try:
        with open(filename, "r", encoding="utf-8") as file:
            lines = []
            for line_number, line in enumerate(file, 1):
                lines.append(f"Line {line_number}: {line.strip()}")
            return lines
    except Exception as e:
        print(f"Error reading file: {e}")
        return []
```

### Writing Files
```python
def write_text_file(filename, content):
    """Write content to a text file"""
    try:
        with open(filename, "w", encoding="utf-8") as file:
            file.write(content)
        print(f"Successfully wrote to '{filename}'")
    except PermissionError:
        print(f"Permission denied to write to '{filename}'")
    except Exception as e:
        print(f"Error writing file: {e}")

def append_to_file(filename, new_content):
    """Append content to existing file"""
    try:
        with open(filename, "a", encoding="utf-8") as file:
            file.write(f"\n{new_content}")
        print(f"Content appended to '{filename}'")
    except Exception as e:
        print(f"Error appending to file: {e}")

# Example usage
log_entry = f"[{datetime.now()}] User logged in"
append_to_file("app.log", log_entry)
```

### File Modes
| Mode | Description | Creates New? | Overwrites? |
|------|-------------|--------------|-------------|
| `"r"` | Read only | No | N/A |
| `"w"` | Write only | Yes | Yes |
| `"a"` | Append only | Yes | No |
| `"r+"` | Read & Write | No | No |
| `"w+"` | Read & Write | Yes | Yes |

### Working with CSV Files
```python
import csv

def read_csv_file(filename):
    """Read CSV file and return data"""
    try:
        with open(filename, "r", newline="", encoding="utf-8") as file:
            csv_reader = csv.DictReader(file)
            data = []
            for row in csv_reader:
                data.append(row)
            return data
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return []

def write_csv_file(filename, data, fieldnames):
    """Write data to CSV file"""
    try:
        with open(filename, "w", newline="", encoding="utf-8") as file:
            csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
            csv_writer.writeheader()
            csv_writer.writerows(data)
        print(f"CSV data written to '{filename}'")
    except Exception as e:
        print(f"Error writing CSV: {e}")

# Example: Student grades
students = [
    {"name": "Alice", "grade": 92, "subject": "Math"},
    {"name": "Bob", "grade": 87, "subject": "Science"},
    {"name": "Charlie", "grade": 95, "subject": "English"}
]

write_csv_file("grades.csv", students, ["name", "grade", "subject"])
```

## Libraries and Modules

### Import Strategies
```python
# Different ways to import
import math                    # Use as math.sqrt()
from math import sqrt, pi      # Use directly: sqrt(), pi
from datetime import datetime as dt  # Use as dt.now()
import random as rnd           # Use as rnd.randint()

# Avoid this (imports everything)
from math import *  # ❌ Can cause naming conflicts
```

### Creating Your Own Modules
**file: math_utils.py**
```python
"""Custom math utilities module"""

def factorial(n):
    """Calculate factorial of n"""
    if n <= 1:
        return 1
    return n * factorial(n - 1)

def is_prime(num):
    """Check if a number is prime"""
    if num < 2:
        return False
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            return False
    return True

def fibonacci(n):
    """Generate first n fibonacci numbers"""
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    
    fib_sequence = [0, 1]
    for i in range(2, n):
        fib_sequence.append(fib_sequence[i-1] + fib_sequence[i-2])
    return fib_sequence

# Module-level constants
PI = 3.14159265359
E = 2.71828182846
```

**Using your module:**
```python
import math_utils

# Use functions from your module
result = math_utils.factorial(5)
print(f"5! = {result}")

primes = [num for num in range(1, 20) if math_utils.is_prime(num)]
print(f"Primes 1-20: {primes}")

fib_numbers = math_utils.fibonacci(10)
print(f"First 10 Fibonacci numbers: {fib_numbers}")
```

### Popular Libraries
```python
# Random number generation
import random

# Generate random numbers
random_int = random.randint(1, 100)
random_float = random.uniform(0.0, 1.0)
random_choice = random.choice(["red", "blue", "green"])

# Shuffle a list
cards = ["A", "K", "Q", "J"]
random.shuffle(cards)

# Mathematical operations
import math

# Common math functions
sqrt_16 = math.sqrt(16)
log_value = math.log(10)
sin_value = math.sin(math.pi / 2)

# Date and time
from datetime import datetime, timedelta

# Current time
now = datetime.now()
print(f"Current time: {now.strftime('%Y-%m-%d %H:%M:%S')}")

# Date arithmetic
tomorrow = now + timedelta(days=1)
last_week = now - timedelta(weeks=1)
```

## Modern Python Features

### The Walrus Operator (:=)
**Assignment expressions** let you assign and use values in one line:

```python
# Traditional approach
user_input = input("Enter a number: ")
if user_input.isdigit():
    number = int(user_input)
    print(f"You entered: {number}")

# With walrus operator (Python 3.8+)
if (user_input := input("Enter a number: ")).isdigit():
    number = int(user_input)
    print(f"You entered: {number}")

# Useful in loops
numbers = []
while (value := input("Enter number (or 'quit'): ")) != "quit":
    if value.isdigit():
        numbers.append(int(value))

print(f"Numbers entered: {numbers}")
```

### List Comprehensions
Create lists efficiently:

```python
# Traditional loop
squares = []
for x in range(10):
    squares.append(x**2)

# List comprehension
squares = [x**2 for x in range(10)]

# With conditions
even_squares = [x**2 for x in range(10) if x % 2 == 0]

# Nested comprehensions
matrix = [[i*j for j in range(3)] for i in range(3)]
# Creates: [[0, 0, 0], [0, 1, 2], [0, 2, 4]]
```

### Dictionary and Set Comprehensions
```python
# Dictionary comprehension
word_lengths = {word: len(word) for word in ["python", "java", "javascript"]}
# {'python': 6, 'java': 4, 'javascript': 10}

# Set comprehension (unique values only)
unique_lengths = {len(word) for word in ["python", "java", "javascript", "go"]}
# {2, 4, 6, 10}
```

## Practical Applications

### Configuration Manager
```python
import json
from pathlib import Path

class ConfigManager:
    """Manage application configuration"""
    
    def __init__(self, config_file="config.json"):
        self.config_file = Path(config_file)
        self.config = self.load_config()
    
    def load_config(self):
        """Load configuration from file"""
        try:
            if self.config_file.exists():
                with open(self.config_file, "r") as file:
                    return json.load(file)
            else:
                return self.get_default_config()
        except Exception as e:
            print(f"Error loading config: {e}")
            return self.get_default_config()
    
    def get_default_config(self):
        """Return default configuration"""
        return {
            "app_name": "My Application",
            "version": "1.0.0",
            "debug": False,
            "database": {
                "host": "localhost",
                "port": 5432
            }
        }
    
    def save_config(self):
        """Save current configuration to file"""
        try:
            with open(self.config_file, "w") as file:
                json.dump(self.config, file, indent=2)
            print("Configuration saved successfully")
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def get(self, key, default=None):
        """Get configuration value"""
        keys = key.split(".")
        value = self.config
        for k in keys:
            value = value.get(k, default) if isinstance(value, dict) else default
        return value
    
    def set(self, key, value):
        """Set configuration value"""
        keys = key.split(".")
        config = self.config
        for k in keys[:-1]:
            config = config.setdefault(k, {})
        config[keys[-1]] = value

# Usage
config = ConfigManager()
db_host = config.get("database.host")
config.set("debug", True)
config.save_config()
```

### Log Analyzer
```python
import re
from collections import Counter
from datetime import datetime

def analyze_log_file(filename):
    """Analyze web server log file"""
    ip_pattern = r'\d+\.\d+\.\d+\.\d+'
    status_pattern = r'" (\d{3}) '
    
    try:
        with open(filename, "r") as file:
            lines = file.readlines()
        
        ips = []
        status_codes = []
        
        for line in lines:
            # Extract IP addresses
            ip_match = re.search(ip_pattern, line)
            if ip_match:
                ips.append(ip_match.group())
            
            # Extract status codes
            status_match = re.search(status_pattern, line)
            if status_match:
                status_codes.append(status_match.group(1))
        
        # Analyze data
        ip_counts = Counter(ips)
        status_counts = Counter(status_codes)
        
        print(f"Total requests: {len(lines)}")
        print(f"Unique IPs: {len(ip_counts)}")
        
        print("\nTop 5 IP addresses:")
        for ip, count in ip_counts.most_common(5):
            print(f"  {ip}: {count} requests")
        
        print("\nStatus code distribution:")
        for status, count in status_counts.most_common():
            print(f"  {status}: {count} ({count/len(status_codes)*100:.1f}%)")
    
    except FileNotFoundError:
        print(f"Log file '{filename}' not found")
    except Exception as e:
        print(f"Error analyzing log file: {e}")

# Usage
analyze_log_file("access.log")
```

## Best Practices

### 1. Use Context Managers
Always use `with` for file operations:
```python
# ❌ Bad - file might not close if error occurs
file = open("data.txt", "r")
data = file.read()
file.close()

# ✅ Good - file automatically closes
with open("data.txt", "r") as file:
    data = file.read()
```

### 2. Handle Specific Exceptions
```python
# ❌ Too broad
try:
    risky_operation()
except Exception:
    print("Something went wrong")

# ✅ Specific and informative
try:
    risky_operation()
except FileNotFoundError:
    print("File not found")
except PermissionError:
    print("Permission denied")
except ValueError as e:
    print(f"Invalid value: {e}")
```

### 3. Use Pathlib for File Paths
```python
from pathlib import Path

# ✅ Modern approach
config_dir = Path.home() / ".config" / "myapp"
config_file = config_dir / "settings.json"

if not config_dir.exists():
    config_dir.mkdir(parents=True)
```

## Next Steps
You now have the tools to build robust Python applications! Consider exploring:
- **Web Development**: Flask, Django
- **Data Science**: pandas, numpy, matplotlib  
- **Machine Learning**: scikit-learn, tensorflow
- **GUI Development**: tkinter, PyQt
- **Automation**: selenium, requests

---
*Tags: #programming #python #advanced #error-handling #file-io #modules*  
*Related: [[Programming/Python Functions]] | [[Programming/Computer Science Concepts]] | [[Systems/Development Tools]]*