# Python Data Structures

#programming #python #data-structures #lists #dictionaries

> **Prerequisites**: [[Programming/Python Fundamentals]]  
> **Next**: [[Programming/Python Control Flow]]

## Overview
Data structures let you organize and store multiple pieces of related information efficiently. Think of them as different types of containers - some better for certain tasks than others.

## Lists - Ordered Collections

Lists store multiple items in a single variable, maintaining their order. Perfect for sequences like shopping lists, student names, or game scores.

### Creating and Accessing Lists
```python
# Creating lists
fruits = ["apple", "banana", "orange"]
numbers = [1, 2, 3, 4, 5]
mixed = ["Alice", 25, True, 3.14]

# Accessing elements (索引 - さくいん = index)
print(fruits[0])    # "apple" (first item)
print(fruits[1])    # "banana" (second item) 
print(fruits[-1])   # "orange" (last item)
```

**Important**: List indexing starts at 0, not 1!

### List Operations
```python
fruits = ["apple", "banana", "orange"]

# Adding elements
fruits.append("grape")           # Add to end
fruits.insert(1, "kiwi")         # Insert at position 1

# Removing elements  
fruits.remove("banana")          # Remove specific item
last_fruit = fruits.pop()        # Remove and return last item

# List information
print(len(fruits))               # Get number of items
print("apple" in fruits)         # Check if item exists

# Final result
print(fruits)  # ["apple", "kiwi", "orange"]
```

### List Methods Summary
| Method | Purpose | Example |
|--------|---------|---------|
| `append(item)` | Add to end | `fruits.append("grape")` |
| `insert(index, item)` | Add at position | `fruits.insert(0, "kiwi")` |
| `remove(item)` | Remove first match | `fruits.remove("apple")` |
| `pop()` | Remove & return last | `last = fruits.pop()` |
| `len(list)` | Get count | `count = len(fruits)` |

## Dictionaries - Key-Value Pairs

Dictionaries store data as key-value pairs, like a real dictionary where you look up words (keys) to find definitions (values). Perfect for storing related information about a single entity.

### Creating and Using Dictionaries
```python
# Creating a dictionary  
student = {
    "name": "Alice",
    "age": 20,
    "grade": "A",
    "enrolled": True
}

# Accessing values
print(student["name"])     # "Alice"
print(student["age"])      # 20
print(student["grade"])    # "A"
```

### Dictionary Operations
```python
student = {"name": "Alice", "age": 20}

# Adding/updating entries
student["grade"] = "A"           # Add new key-value pair
student["age"] = 21              # Update existing value

# Removing entries
del student["grade"]             # Remove specific key
removed_age = student.pop("age") # Remove and return value

# Dictionary information
print(len(student))              # Number of key-value pairs
print("name" in student)         # Check if key exists
print(student.keys())            # Get all keys
print(student.values())          # Get all values
```

### When to Use Each Structure

**Use Lists When:**
- Order matters (first, second, third...)
- You have a sequence of similar items
- You need to access items by position
- Examples: shopping list, test scores, menu items

**Use Dictionaries When:**
- You need to look up values by meaningful names
- You're storing related attributes of one thing
- Order doesn't matter as much
- Examples: student record, game settings, user profile

## Practical Examples

### Contact Book (Dictionary)
```python
contact = {
    "name": "John Smith",
    "phone": "555-0123", 
    "email": "john@example.com",
    "address": "123 Main St"
}

print(f"Calling {contact['name']} at {contact['phone']}")
```

### Shopping List (List)
```python
shopping_list = ["milk", "bread", "eggs"]

# Add items
shopping_list.append("cheese")
shopping_list.append("apples")

# Check what we need
print(f"Need to buy {len(shopping_list)} items:")
for item in shopping_list:
    print(f"- {item}")
```

### Combining Both - Class Roster
```python
# List of dictionaries - each student is a dictionary
class_roster = [
    {"name": "Alice", "grade": 92, "year": "sophomore"},
    {"name": "Bob", "grade": 87, "year": "junior"}, 
    {"name": "Charlie", "grade": 95, "year": "senior"}
]

# Print each student's info
for student in class_roster:
    print(f"{student['name']}: {student['grade']}% ({student['year']})")
```

## Common Patterns

### List Comprehensions (Advanced)
```python
# Create new list from existing one
numbers = [1, 2, 3, 4, 5]
squares = [x**2 for x in numbers]  # [1, 4, 9, 16, 25]
```

### Dictionary from Lists
```python
names = ["Alice", "Bob", "Charlie"]
scores = [92, 87, 95]
grade_book = dict(zip(names, scores))
# {"Alice": 92, "Bob": 87, "Charlie": 95}
```

## Next Steps
Now that you can store and organize data, learn how to make decisions and repeat actions with [[Programming/Python Control Flow]].

---
*Tags: #programming #python #lists #dictionaries #data-structures*  
*Related: [[Programming/Python Fundamentals]] | [[Programming/Python Control Flow]] | [[Programming/Python Functions]]*