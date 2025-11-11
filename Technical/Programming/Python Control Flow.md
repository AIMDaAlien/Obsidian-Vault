# Python Control Flow

#programming #python #conditionals #loops #control-flow

> **Prerequisites**: [[Programming/Python Fundamentals]] | [[Programming/Python Data Structures]]  
> **Next**: [[Programming/Python Functions]]

## Overview
Control flow determines the order in which your program executes code. Instead of just running line by line, you can make decisions, repeat actions, and create dynamic behavior.

## Conditional Logic - Making Decisions

Computers excel at automating decision-making through **conditional logic** (条件論理 - じょうけんろんり). These are essentially yes/no questions written in code syntax.

### Comparison Operators
These operators compare values and return `True` or `False`:

| Operator | Meaning | Example | Result |
|----------|---------|---------|---------|
| `==` | Equal to | `5 == 5` | `True` |
| `!=` | Not equal | `5 != 3` | `True` |
| `>` | Greater than | `7 > 3` | `True` |
| `<` | Less than | `2 < 8` | `True` |
| `>=` | Greater or equal | `5 >= 5` | `True` |
| `<=` | Less or equal | `3 <= 2` | `False` |

### Basic If Statements
```python
age = 16

if age >= 18:
    print("You can vote!")
    print("Democracy awaits!")
    
# Note: Indentation matters in Python!
```

**Indentation Rules:**
- Code inside `if` blocks must be indented (usually 4 spaces)
- All statements at the same level need consistent indentation
- Python uses indentation instead of curly braces `{}`

### If-Else Statements (Dual-Alternative)
Handle both true and false conditions:

```python
temperature = 85

if temperature > 80:
    print("Turn on the air conditioning")
    print("It's hot outside!")
else:
    print("Open the windows")
    print("Nice weather today!")
```

### Multi-Way Decisions with elif
Handle multiple conditions efficiently:

```python
# Grade calculator
score = int(input("Enter your test score: "))

if score >= 90:
    print("Your grade is an A")
elif score >= 80:
    print("Your grade is a B") 
elif score >= 70:
    print("Your grade is a C")
elif score >= 60:
    print("Your grade is a D")
else:
    print("Your grade is an F")
```

**Why elif vs Nested if?**
- **elif**: Cleaner, easier to read, only one condition checked per path
- **Nested if**: Can become deeply indented and hard to follow

### Logical Operators
Combine multiple conditions:

```python
age = 20
has_license = True
has_car = False

# AND - both conditions must be true
if age >= 18 and has_license:
    print("You can drive!")

# OR - at least one condition must be true  
if has_license or age >= 21:
    print("You have some adult privileges")
    
# NOT - reverses the condition
if not has_car:
    print("You might need public transportation")
```

## Loops - Repeating Actions

Loops let you repeat code multiple times without writing it over and over.

### While Loops - Conditional Repetition
Repeat **while** a condition remains true:

```python
count = 0

while count < 5:
    print(f"Count is: {count}")
    count += 1  # Same as: count = count + 1
    
print("Loop finished!")
```

**Warning**: Make sure the condition eventually becomes false, or you'll create an infinite loop!

### For Loops - Iteration Over Sequences
Repeat **for each** item in a sequence:

```python
# Loop through a list
fruits = ["apple", "banana", "orange"]

for fruit in fruits:
    print(f"I like {fruit}")

# Loop through a range of numbers
for i in range(5):  # 0, 1, 2, 3, 4
    print(f"Number: {i}")
    
# Range with start and stop
for i in range(1, 6):  # 1, 2, 3, 4, 5
    print(f"Number: {i}")
```

### Practical Loop Examples

#### Werewolf Detector
```python
user_howl = int(input("How many times did you howl last night? "))

if user_howl > 0:
    print("You may be a werewolf!")
    print("Seek immediate medical attention.")
else:
    print("You seem human enough.")
```

#### Number Guessing Game
```python
secret_number = 7
guess = 0

while guess != secret_number:
    guess = int(input("Guess the number (1-10): "))
    
    if guess < secret_number:
        print("Too low!")
    elif guess > secret_number:
        print("Too high!")
    else:
        print("Correct! You win!")
```

#### Processing a Shopping List
```python
shopping_list = ["milk", "bread", "eggs", "cheese"]
total_items = len(shopping_list)

print(f"Shopping list ({total_items} items):")

for i, item in enumerate(shopping_list, 1):
    print(f"{i}. {item}")
    
print("Don't forget your wallet!")
```

## Advanced Control Flow

### Loop Control
```python
# break - exit the loop immediately
for i in range(10):
    if i == 5:
        break  # Stop when i equals 5
    print(i)  # Prints 0, 1, 2, 3, 4

# continue - skip to next iteration
for i in range(5):
    if i == 2:
        continue  # Skip when i equals 2
    print(i)  # Prints 0, 1, 3, 4
```

### Nested Structures
```python
# Nested loops
for i in range(3):
    print(f"Outer loop: {i}")
    for j in range(2):
        print(f"  Inner loop: {j}")

# Nested conditionals within loops
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

for num in numbers:
    if num % 2 == 0:
        if num > 5:
            print(f"{num} is a large even number")
        else:
            print(f"{num} is a small even number")
```

## Design Patterns

### Input Validation
```python
while True:
    age = input("Enter your age: ")
    
    if age.isdigit():
        age = int(age)
        if 0 <= age <= 120:
            break
        else:
            print("Age must be between 0 and 120")
    else:
        print("Please enter a valid number")

print(f"You are {age} years old")
```

### Menu Systems
```python
while True:
    print("\n=== Menu ===")
    print("1. Option A")
    print("2. Option B") 
    print("3. Quit")
    
    choice = input("Choose an option: ")
    
    if choice == "1":
        print("You chose Option A")
    elif choice == "2":
        print("You chose Option B")
    elif choice == "3":
        print("Goodbye!")
        break
    else:
        print("Invalid choice. Try again.")
```

## Common Pitfalls

1. **Assignment vs Comparison**: `=` assigns, `==` compares
   ```python
   if x = 5:     # ❌ Error!
   if x == 5:    # ✅ Correct
   ```

2. **Infinite Loops**: Always ensure your while condition can become false
   ```python
   count = 0
   while count < 5:
       print(count)
       # ❌ Forgot to increment count!
   ```

3. **Indentation Errors**: Python is strict about indentation
   ```python
   if True:
   print("Hello")  # ❌ Must be indented
   ```

## Next Steps
Ready to organize your code into reusable pieces? Learn about [[Programming/Python Functions]] to make your programs more modular and efficient.

---
*Tags: #programming #python #conditionals #loops #if-else #while #for*  
*Related: [[Programming/Python Fundamentals]] | [[Programming/Python Data Structures]] | [[Programming/Python Functions]]*