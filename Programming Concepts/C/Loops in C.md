
![[Pasted image 20230616112817.png]]
Is the same as:
```C
int counter = 0;
while (counter < 3)
{
	printf("meow/n");
	counter = counter + 1;
}
```

But can be more simplified (look into [[Syntactic Sugar]]):
```C
int i = 0;
while (i < 3)
{
	printf("meow/n");
	i++;
}
```

[[For Loops in C]]
