Sometimes decision structures are more complex than dual- alt decision statements. 

The following chart shows a program to figure a letter grade based on a user's score. We have a series of conditional statements with different criteria. 
![[Pasted image 20230520180516.png]]

Note at each decision point the program compares user's score to a criteria. For example, the first decision point is 90. If the score is >= 90, the condition is "True" and the program outputs "Your grade is an A". If the score is < 90, the program continues to the next statement.

This is where the term nested comes from; the program only evaluates the second conditional statement if the fiest statement is false. 

Nested `if-else` structures follow the same general rules as a single `if-else` statement. Let’s examine what this flowchart would look like in Python:

```python
# What is the score?
score = int(input("What is your test score?"))

# Determine the grade.
if score >= 90:
    print('Your grade is an A.')
else:
    if score >= 80:
        print('Your grade is a B.')
    else:
        if score >= 70:
            print('Your grade is a C.')
        else:
            if score >= 60:
                print('Your grade is a D.')
            else:
                print('Your grade is an F.')
```

These nested if else statements are complex and require various levels of indentation. Luckily, we can simplify this code using `if-elif-else` statements. The `elif` keyword stands for "else if"

With nested `if-elif-else` statements, we create a compound statement that combines our `if` and `else` statements into one line.

{ If you have to scroll horizontally on your computer  screen to view all the code in an `if-else` statement, then you should use an `if-elif-else` statement. }

```python
# What is the score?
score = int(input("What is your test score?"))

# Determine the grade.
if score >= 90:
    print('Your grade is an A.')
elif score >= 80:
    print('Your grade is a B.')
elif score >= 70:
    print('Your grade is a C.')
elif score >= 60:
    print('Your grade is a D.')
else:
    print('Your grade is an F.')
```

The compound statement, `elif`, is created like this:

-   The first `if` statement tests the condition.
-   The following `else` statement and the preceding `if` statement are compounded to make the `elif` statement.
-   This syntax continues until the last `else` statement.
-   In an `if-elif-else` statement, the `if`, `elif`, and `else` statements are all aligned, and the conditionally executed blocks are indented.