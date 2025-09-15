# Computer Science Concepts

#computer-science #hardware #cpu #programming #theory #cs50

> **Related**: [[Programming/Python Fundamentals]] | [[Systems/Operating Systems]]

## Overview
Fundamental computer science concepts that every programmer should understand. These concepts form the foundation for understanding how computers work and how to write efficient code.

## How Computers Work

### Binary and Information
Computer science is fundamentally the study of **information** (情報 - じょうほう). Everything in a computer is represented using binary digits (bits):

- **Bit**: A single binary digit (0 or 1)
- **Byte**: 8 bits (can represent 0-255)
- **Information Encoding**: Numbers, text, images, and even emojis are all stored as patterns of 0s and 1s

```
Example: The letter 'A' in ASCII is 65 in decimal
65 in binary: 01000001
```

### How CPUs Work
When you write software, you're creating instructions that will be executed as **machine code** by the CPU (Central Processing Unit).

#### CPU Components
**Transistors** → **Logic Gates** → **Complex Operations**

1. **Transistors**: Tiny electronic switches (billions in modern CPUs)
2. **Logic Gates**: Groups of transistors that perform basic operations:
   - **AND gate**: Output is 1 only if both inputs are 1
   - **OR gate**: Output is 1 if at least one input is 1  
   - **NOT gate**: Output is opposite of input
3. **Arithmetic Logic Unit (ALU)**: Combines logic gates to perform math

#### From Code to Execution
```
Your Python Code → Interpreter → Machine Code → CPU Instructions → Results
```

**Example**: When you write `5 + 3`, the CPU:
1. Loads the values 5 and 3 into registers
2. Uses logic gates in the ALU to perform binary addition
3. Stores the result (8) in memory
4. Returns the result to your program

### Memory Hierarchy
Computers use different types of memory with different speeds and capacities:

| Type | Speed | Size | Purpose |
|------|-------|------|---------|
| **CPU Registers** | Fastest | Tiny | Currently processed data |
| **Cache** | Very Fast | Small | Recently used data |
| **RAM** | Fast | Medium | Running programs |
| **Storage** | Slower | Large | Permanent files |

## Programming Fundamentals

### Computational Thinking
The application of computer science ideas to solve problems in any domain:

1. **Decomposition**: Break complex problems into smaller parts
2. **Pattern Recognition**: Identify similarities and recurring themes
3. **Abstraction**: Focus on important details, ignore irrelevant ones
4. **Algorithms**: Create step-by-step solutions

#### Example: Making Toast (Algorithm)
```
1. Get bread from bag
2. Put bread slice in toaster
3. Set timer to desired darkness
4. Press down lever
5. Wait for toast to pop up
6. Remove toast carefully
7. Add butter if desired
```

### Pseudocode
English-like syntax for planning programs before writing actual code:

```
ALGORITHM: Find largest number in a list
INPUT: list of numbers
OUTPUT: largest number

SET largest = first number in list
FOR each remaining number in list:
    IF current number > largest:
        SET largest = current number
RETURN largest
```

### Data Representation

#### Unicode and Character Encoding
Modern computers use **Unicode** to represent text from all languages:
- ASCII: Basic English characters (127 characters)
- UTF-8: Supports all world languages (millions of characters)
- Emojis, fonts, and special symbols are all Unicode characters

#### Number Systems
```python
# Different ways to represent the same number
decimal = 42      # Base 10 (human-friendly)
binary = 0b101010 # Base 2 (computer-friendly)  
hex = 0x2A        # Base 16 (programmer-friendly)

print(decimal, binary, hex)  # All print: 42 42 42
```

## Programming Language Concepts

### Compiled vs Interpreted Languages

**Compiled Languages** (C, C++, Rust):
```
Source Code → Compiler → Machine Code → Execute
```
- Faster execution
- Platform-specific
- Errors caught before running

**Interpreted Languages** (Python, JavaScript):
```
Source Code → Interpreter → Execute line by line
```
- Slower execution
- Platform-independent  
- Errors caught during execution

### Programming Paradigms

#### Procedural Programming
Code organized as a sequence of functions:
```python
def calculate_area(length, width):
    return length * width

def calculate_perimeter(length, width):  
    return 2 * (length + width)

# Usage
area = calculate_area(5, 3)
perimeter = calculate_perimeter(5, 3)
```

#### Object-Oriented Programming (OOP)
Code organized around objects that contain data and methods:
```python
class Rectangle:
    def __init__(self, length, width):
        self.length = length
        self.width = width
    
    def area(self):
        return self.length * self.width
    
    def perimeter(self):
        return 2 * (self.length + self.width)

# Usage
rect = Rectangle(5, 3)
area = rect.area()
perimeter = rect.perimeter()
```

#### Functional Programming
Code organized around functions that don't modify state:
```python
# Pure functions - same input always gives same output
def add(x, y):
    return x + y

def multiply(x, y):
    return x * y

# Function composition
def calculate_compound(principal, rate, years):
    return multiply(principal, (1 + rate) ** years)
```

## Algorithms and Complexity

### Common Algorithms

#### Searching
```python
def linear_search(arr, target):
    """Search through array one by one"""
    for i, value in enumerate(arr):
        if value == target:
            return i
    return -1

def binary_search(sorted_arr, target):
    """Efficient search in sorted array"""
    left, right = 0, len(sorted_arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        if sorted_arr[mid] == target:
            return mid
        elif sorted_arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1
```

#### Sorting
```python
def bubble_sort(arr):
    """Simple but slow sorting algorithm"""
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

# Python's built-in sort is much more efficient
numbers = [64, 34, 25, 12, 22, 11, 90]
sorted_numbers = sorted(numbers)  # Use this in practice!
```

### Big O Notation
Describes how algorithm performance scales with input size:

| Notation | Name | Example | Performance |
|----------|------|---------|-------------|
| O(1) | Constant | Array access | Excellent |
| O(log n) | Logarithmic | Binary search | Good |
| O(n) | Linear | Linear search | Okay |
| O(n²) | Quadratic | Bubble sort | Poor |
| O(2ⁿ) | Exponential | Recursive fibonacci | Terrible |

```python
# O(1) - Constant time
def get_first_item(arr):
    return arr[0]  # Always same speed regardless of array size

# O(n) - Linear time  
def find_max(arr):
    max_val = arr[0]
    for item in arr:  # Checks every item once
        if item > max_val:
            max_val = item
    return max_val

# O(n²) - Quadratic time
def find_duplicates(arr):
    duplicates = []
    for i in range(len(arr)):           # Outer loop: n times
        for j in range(i + 1, len(arr)):  # Inner loop: up to n times
            if arr[i] == arr[j]:
                duplicates.append(arr[i])
    return duplicates
```

## Data Structures

### Arrays and Lists
**Fixed vs Dynamic Size:**
- **Arrays** (C): Fixed size, elements stored contiguously
- **Lists** (Python): Dynamic size, can grow/shrink

**Time Complexities:**
- Access by index: O(1)
- Search: O(n)
- Insert at end: O(1) amortized
- Insert at beginning: O(n)

### Hash Tables (Dictionaries)
Use hash functions to map keys to array indices for fast lookup:

```python
# Python dictionaries use hash tables internally
student = {
    "name": "Alice",    # Hash("name") → index 5
    "age": 20,          # Hash("age") → index 12  
    "grade": "A"        # Hash("grade") → index 3
}

# Average case: O(1) for access, insert, delete
print(student["name"])  # Very fast lookup
```

### Stacks and Queues

**Stack** (LIFO - Last In, First Out):
```python
# Using list as stack
stack = []
stack.append(1)    # Push
stack.append(2)    # Push
stack.append(3)    # Push
top = stack.pop()  # Pop (returns 3)
```

**Queue** (FIFO - First In, First Out):
```python
from collections import deque

queue = deque()
queue.append(1)      # Enqueue
queue.append(2)      # Enqueue  
queue.append(3)      # Enqueue
first = queue.popleft()  # Dequeue (returns 1)
```

## Real-World Applications

### Web Development Stack
```
Frontend (Browser):
├── HTML (Structure)
├── CSS (Styling)  
└── JavaScript (Interactivity)

Backend (Server):
├── Python/Node.js/Java (Logic)
├── Database (Data Storage)
└── API (Communication)
```

### Database Fundamentals
```sql
-- Relational databases organize data in tables
CREATE TABLE students (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    age INTEGER,
    grade TEXT
);

-- CRUD Operations
INSERT INTO students (name, age, grade) VALUES ('Alice', 20, 'A');
SELECT * FROM students WHERE grade = 'A';
UPDATE students SET age = 21 WHERE name = 'Alice';
DELETE FROM students WHERE id = 1;
```

### Network Concepts
```
Client ←→ Internet ←→ Server

HTTP Request:
GET /api/users HTTP/1.1
Host: example.com

HTTP Response:
HTTP/1.1 200 OK
Content-Type: application/json
{"users": [...]}
```

## CS50 Concepts Review
These concepts from Harvard's CS50 course are foundational:

### Problem-Solving Approach
1. **Understand** the problem completely
2. **Plan** your approach (pseudocode)
3. **Implement** the solution
4. **Test** with various inputs
5. **Debug** and refine

### Memory Management
- **Stack**: Function calls, local variables (automatic cleanup)
- **Heap**: Dynamic memory allocation (manual cleanup in some languages)
- **Memory Leaks**: Forgetting to free allocated memory

### Abstraction Layers
```
High Level: Python, JavaScript (easy to use)
    ↓
Medium Level: C, C++ (more control)
    ↓
Low Level: Assembly (direct CPU instructions)
    ↓
Machine Code: Binary (what CPU actually executes)
```

## Key Takeaways

1. **Everything is data**: Text, images, sound are all binary patterns
2. **Algorithms matter**: Good algorithms can make impossible problems possible
3. **Trade-offs exist**: Speed vs memory, simplicity vs efficiency
4. **Abstraction is powerful**: Higher-level languages let you focus on problems, not implementation
5. **Practice thinking computationally**: Break problems down, find patterns, create step-by-step solutions

Understanding these fundamentals will make you a better programmer in any language and help you tackle complex problems systematically.

---
*Tags: #computer-science #algorithms #data-structures #cpu #programming #theory*  
*Related: [[Programming/Python Fundamentals]] | [[Systems/Operating Systems]] | [[Programming/Web Development]]*