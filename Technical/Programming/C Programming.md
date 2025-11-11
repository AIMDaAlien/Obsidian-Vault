# C Programming Fundamentals

#programming #c #low-level #systems #cs50

> **Related**: [[Programming/Computer Science Concepts]] | [[Systems/Operating Systems]]

## Overview
C is a foundational programming language that sits "under the hood" of most modern languages. Learning C helps you understand how computers actually work at a lower level.

## Why Learn C?

C is **everywhere** and influences most modern programming languages:
- **Operating Systems**: Linux, Windows kernels written in C
- **Embedded Systems**: IoT devices, microcontrollers
- **Performance-Critical Software**: Games, databases, compilers
- **Foundation Knowledge**: Understanding C makes other languages easier

## C vs Python: Key Differences

| Aspect | Python | C |
|--------|--------|---|
| **Memory Management** | Automatic | Manual |
| **Data Types** | Dynamic | Must declare explicitly |
| **Speed** | Slower (interpreted) | Faster (compiled) |
| **Syntax** | Simple, readable | More verbose |
| **Error Handling** | Runtime errors | Compile-time + runtime |

## Data Types and Memory

### Why C Cares About Data Types
Unlike Python, C needs to know **exactly** how much memory to allocate for each variable:

```c
#include <stdio.h>

int main(void) {
    // Different types use different amounts of memory
    int age = 25;           // 4 bytes (32 bits)
    long population = 8000000L;  // 8 bytes (64 bits)
    float height = 5.8f;    // 4 bytes
    double precise = 3.14159265359;  // 8 bytes
    char grade = 'A';       // 1 byte
    
    // Show memory usage
    printf("int: %zu bytes\n", sizeof(int));
    printf("long: %zu bytes\n", sizeof(long));
    printf("float: %zu bytes\n", sizeof(float));
    printf("double: %zu bytes\n", sizeof(double));
    printf("char: %zu bytes\n", sizeof(char));
    
    return 0;
}
```

### Memory Addresses
Every value in C has a specific memory address:

```c
#include <stdio.h>

int main(void) {
    int x = 50;
    
    printf("Value of x: %i\n", x);
    printf("Address of x: %p\n", &x);  // & gets the address
    
    // Memory address might look like: 0x7fff5fbff6ac
    return 0;
}
```

**Memory Concept**: Think of memory as a giant array of boxes, each with a unique address (like house numbers on a street).

## Variables and Declaration

### Variable Rules in C
```c
#include <stdio.h>

int main(void) {
    // Must declare type before using
    int x = 50;              // Initialize when declaring
    int y;                   // Declare first...
    y = 100;                 // ...assign later
    
    // All statements end with semicolon
    char letter = 'A';
    float price = 19.99f;
    
    return 0;
}
```

### Input and Output

#### Getting User Input
```c
#include <stdio.h>
#include <cs50.h>  // CS50 library for easier input

int main(void) {
    // Using CS50 library (easier)
    string name = get_string("What's your name? ");
    int age = get_int("What is your age? ");
    string phone = get_string("What's your phone number? ");
    
    // Display information
    printf("Name: %s, Age: %i, Phone: %s\n", name, age, phone);
    
    return 0;
}
```

#### Format Specifiers
| Type | Specifier | Example |
|------|-----------|---------|
| `int` | `%i` or `%d` | `printf("%i", 42)` |
| `long` | `%li` | `printf("%li", 1000000L)` |
| `float` | `%f` | `printf("%.2f", 3.14f)` |
| `double` | `%f` | `printf("%.6f", 3.14159)` |
| `char` | `%c` | `printf("%c", 'A')` |
| `string` | `%s` | `printf("%s", "Hello")` |

## Control Flow

### Conditionals
```c
#include <stdio.h>
#include <cs50.h>

int main(void) {
    int score = get_int("Enter your test score: ");
    
    if (score >= 90) {
        printf("Your grade is an A\n");
    }
    else if (score >= 80) {
        printf("Your grade is a B\n");
    }
    else if (score >= 70) {
        printf("Your grade is a C\n");
    }
    else if (score >= 60) {
        printf("Your grade is a D\n");
    }
    else {
        printf("Your grade is an F\n");
    }
    
    return 0;
}
```

### Loops

#### While Loops
```c
#include <stdio.h>

int main(void) {
    int counter = 0;
    
    while (counter < 3) {
        printf("meow\n");
        counter = counter + 1;  // Can also write: counter++
    }
    
    return 0;
}
```

#### For Loops
All loop logic in one clean line:

```c
#include <stdio.h>

int main(void) {
    // Initialization; Condition; Increment
    for (int i = 0; i < 3; i++) {
        printf("meow\n");
    }
    
    return 0;
}
```

**For Loop Breakdown:**
1. **`int i = 0`**: Initialize counter variable
2. **`i < 3`**: Continue while this condition is true
3. **`i++`**: Increment after each iteration (same as `i = i + 1`)

#### Loop Comparison
```c
// These three loops do exactly the same thing:

// Version 1: Basic while loop
int counter = 0;
while (counter < 3) {
    printf("meow\n");
    counter = counter + 1;
}

// Version 2: Shorter variable names and increment
int i = 0;
while (i < 3) {
    printf("meow\n");
    i++;
}

// Version 3: For loop (most concise)
for (int i = 0; i < 3; i++) {
    printf("meow\n");
}
```

## Memory and Pointers

### Understanding Memory Layout
```c
#include <stdio.h>

int main(void) {
    int numbers[] = {10, 20, 30, 40};
    
    // Arrays are stored contiguously in memory
    for (int i = 0; i < 4; i++) {
        printf("numbers[%i] = %i (address: %p)\n", 
               i, numbers[i], &numbers[i]);
    }
    
    return 0;
}

/*
Output might look like:
numbers[0] = 10 (address: 0x7fff5fbff6a0)
numbers[1] = 20 (address: 0x7fff5fbff6a4)  // 4 bytes later
numbers[2] = 30 (address: 0x7fff5fbff6a8)  // 4 bytes later
numbers[3] = 40 (address: 0x7fff5fbff6ac)  // 4 bytes later
*/
```

### Basic Pointers
```c
#include <stdio.h>

int main(void) {
    int x = 50;
    int *px = &x;  // px "points to" x
    
    printf("Value of x: %i\n", x);        // 50
    printf("Address of x: %p\n", &x);     // Memory address
    printf("Value of px: %p\n", px);      // Same address
    printf("Value at px: %i\n", *px);     // 50 (dereference)
    
    // Change value through pointer
    *px = 100;
    printf("New value of x: %i\n", x);    // 100
    
    return 0;
}
```

## Practical Examples

### Simple Calculator
```c
#include <stdio.h>
#include <cs50.h>

int main(void) {
    // Get user input
    float x = get_float("Enter first number: ");
    char operator = get_char("Enter operator (+, -, *, /): ");
    float y = get_float("Enter second number: ");
    
    float result;
    bool valid = true;
    
    // Perform calculation
    switch (operator) {
        case '+':
            result = x + y;
            break;
        case '-':
            result = x - y;
            break;
        case '*':
            result = x * y;
            break;
        case '/':
            if (y != 0) {
                result = x / y;
            } else {
                printf("Error: Division by zero!\n");
                valid = false;
            }
            break;
        default:
            printf("Error: Invalid operator!\n");
            valid = false;
    }
    
    if (valid) {
        printf("%.2f %c %.2f = %.2f\n", x, operator, y, result);
    }
    
    return 0;
}
```

### Grade Calculator
```c
#include <stdio.h>
#include <cs50.h>

float calculate_average(int scores[], int count);
char letter_grade(float average);

int main(void) {
    int num_tests = get_int("How many test scores? ");
    int scores[num_tests];  // Variable-length array
    
    // Get all scores
    for (int i = 0; i < num_tests; i++) {
        scores[i] = get_int("Test %i score: ", i + 1);
    }
    
    // Calculate results
    float average = calculate_average(scores, num_tests);
    char grade = letter_grade(average);
    
    printf("Average: %.1f%% (Grade: %c)\n", average, grade);
    
    return 0;
}

float calculate_average(int scores[], int count) {
    int sum = 0;
    for (int i = 0; i < count; i++) {
        sum += scores[i];
    }
    return (float) sum / count;  // Cast to float for decimal result
}

char letter_grade(float average) {
    if (average >= 90) return 'A';
    else if (average >= 80) return 'B';
    else if (average >= 70) return 'C';
    else if (average >= 60) return 'D';
    else return 'F';
}
```

### String Processing
```c
#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>

int main(void) {
    string text = get_string("Enter some text: ");
    
    int length = strlen(text);
    int letters = 0, digits = 0, spaces = 0;
    
    for (int i = 0; i < length; i++) {
        if (isalpha(text[i])) {
            letters++;
        } else if (isdigit(text[i])) {
            digits++;
        } else if (isspace(text[i])) {
            spaces++;
        }
    }
    
    printf("Text analysis:\n");
    printf("Length: %i characters\n", length);
    printf("Letters: %i\n", letters);
    printf("Digits: %i\n", digits);
    printf("Spaces: %i\n", spaces);
    
    return 0;
}
```

## Key Differences from Python

### Memory Management
```c
// C: You must manage memory manually
#include <stdlib.h>

int main(void) {
    // Allocate memory for 10 integers
    int *numbers = malloc(10 * sizeof(int));
    
    if (numbers == NULL) {
        printf("Memory allocation failed!\n");
        return 1;
    }
    
    // Use the memory...
    for (int i = 0; i < 10; i++) {
        numbers[i] = i * i;
    }
    
    // MUST free the memory when done
    free(numbers);
    
    return 0;
}
```

### Error Handling
```c
// C: Check return values and handle errors explicitly
#include <stdio.h>

int main(void) {
    FILE *file = fopen("data.txt", "r");
    
    if (file == NULL) {
        printf("Error: Could not open file\n");
        return 1;  // Return error code
    }
    
    // Read from file...
    char buffer[100];
    while (fgets(buffer, sizeof(buffer), file)) {
        printf("%s", buffer);
    }
    
    fclose(file);  // Always close files
    return 0;      // Return success code
}
```

## C Best Practices

### 1. Always Check Return Values
```c
// ❌ Bad - ignoring potential errors
FILE *file = fopen("data.txt", "r");
char buffer[100];
fgets(buffer, sizeof(buffer), file);

// ✅ Good - checking for errors
FILE *file = fopen("data.txt", "r");
if (file == NULL) {
    perror("fopen");
    return 1;
}

char buffer[100];
if (fgets(buffer, sizeof(buffer), file) == NULL) {
    if (feof(file)) {
        printf("End of file reached\n");
    } else {
        perror("fgets");
    }
}
```

### 2. Initialize Variables
```c
// ❌ Bad - uninitialized variable
int count;
printf("%i\n", count);  // Undefined behavior!

// ✅ Good - always initialize
int count = 0;
printf("%i\n", count);  // Prints 0
```

### 3. Use Descriptive Names
```c
// ❌ Bad
int x, y, z;
for (int i = 0; i < x; i++) {
    y += z;
}

// ✅ Good
int num_students, total_score, individual_score;
for (int student = 0; student < num_students; student++) {
    total_score += individual_score;
}
```

## Compilation Process

```bash
# Compile C program
gcc -o program program.c

# With CS50 library
gcc -o program program.c -lcs50

# With debugging info
gcc -g -o program program.c

# Run the program
./program
```

## Common Pitfalls

1. **Forgetting semicolons**: Every statement needs `;`
2. **Uninitialized variables**: Always set initial values
3. **Array bounds**: C doesn't check if you access `array[100]` when array only has 10 elements
4. **Memory leaks**: Every `malloc()` needs a matching `free()`
5. **Comparing strings**: Use `strcmp()`, not `==`

## Next Steps

C programming opens doors to:
- **Systems Programming**: Operating systems, device drivers
- **Embedded Programming**: Arduino, IoT devices  
- **Performance Computing**: Games, scientific computing
- **Understanding Other Languages**: Java, C++, Rust concepts become clearer

Master C, and you'll understand how computers really work!

---
*Tags: #programming #c #low-level #systems #memory-management*  
*Related: [[Programming/Computer Science Concepts]] | [[Systems/Operating Systems]] | [[Programming/Python Fundamentals]]*