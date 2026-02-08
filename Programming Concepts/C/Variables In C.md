In C, variables end with semicolon
![[Pasted image 20230607141247.png]]


Int x = 50;
Create  integer that called x that gets the value 50

### Why does C care about data types
- Different memory amounts to allocate
- Specificity 

![[Pasted image 20230607141820.png]]
We initialize and declare

![[Pasted image 20230607144454.png]]


In this case its better to read right to left when seeing function call.
The function will run and then  give back a return value. and maybe asks for the integer and stores a value 
![[Pasted image 20230607144708.png]]


#### Printing Values
The % is a placeholder and "i"  means integer
![[Pasted image 20230607144910.png]]

![[Pasted image 20230607144940.png]]
The long (%li) and double (%f) are basically utilizing more memory to show more digits or numbers. 


Phonebook Program
```C
#include <stdio.h>
#include <cs50.io

int main (void)
{
	string name = get_string("What's your name? ");
	int age = get_int("What is your age? ");
	string number = get_string("What's your phone number? ");

	printf("Age is %i. Name is %s. Phone number is %s.", age, name, number); 
}

```
Another building blocks are these conditionals and loops.
Firstly, we have a question: have i called less than one time, and if i have then ill say, ill call more often.


```C
int i = 0;
while (i < 10)
{
	printf("%i/n", i);
	i = i + 1;
}
```

We have our initialization: i is first set to 0, then we have our boolean expression, *i < 10*  is it true or false?. And then this incrementation, *i = i +1* changing this value as we go through. And finally when our boolean is no longer true, we wont be inside that loop there. 


We can make our code run a certain amount of times. C has  a syntax where you can write the code in even an abbreviated format.

### For Loop 
Here we have a for loop that has all the same elements but now just on one clean line. 
```C
for (int i = 0; i <10; i++)
{
	printf("%i/n", i);
}
```
