# Homework 2

## Homework 2-1
> Hubo plans a train route

Your task is to implement a function `demo_route(function_type, a, b, c)` in which Hubo drops beepers in the city along the graph of the given function as instructed.

### IMPORTANT CHANGE
**You should use `round` function to calculate the nearest integer. Otherwise, your code cannot pass some test cases.**

### Condition
You’ll be given a 10x10 city (i.e., 10 horizontal lines, 10 vertical lines).

### Task
Implement a function `demo_route` where Hubo drops beepers as follows for xx=1, 2, …, 10:

1. Hubo calculates the function value $f(x)$.
2. Hubo then drops beeper(s) as follows:
  * If $0.5 \le f(x) < 10.5$, Hubo drops a beeper at `(x, round( f(x) ))` where `round` finds the nearest even integer to `f(x)`.  
    Please use the built-in round function as it behaves slightly different from mathematical round.

  * If $f(x) < 0.5$, Hubo drops three beepers at $(x, 1)$ to mark that the proposed route hits the bottom boundary of the city.
  
  * If $10.5 \le f(x)$, Hubo drops three beepers at $(x, 10)$ to mark that the proposed route hits the top boundary of the city.

### Input
The function `demo_route` takes four parameters as its input - one string type parameter *function_type* and three float type parameters a, b, and c.

* *function_type*: ‘quad’ (quadratic) or ‘trig’ (trigonometric). You do not need to consider other inputs for function_type.
* *a, b, c*: three coefficients of the function.
  * When the function_type is ‘quad’, Hubo should drop beepers along the graph of $f(x) = ax^2+bx+c$.
  * When the function_type is ‘trig’, Hubo should drop beepers along the graph of $f(x) = asin(bx)+c$. Make sure that the input of sine function is radian.

### Output
The city with the beepers dropped along the graph of the given function.

----

## Homework 2-2
> Get distance between the train route and each town

Your task is to implement a function `calculate_distance(function_type, a, b, c)` in which Hubo investigates the vertical distance between towns and the train route.

### Condition
You’ll be given an 11x10 city (i.e., 11 horizontal lines, 10 vertical lines).

1. The bottom 10x10 area represents the city where citizens live. For simplicity, we assume that **only one beeper** is dropped on each vertical line in the area. A beeper represents a town in the city.
2. On the top (11th) horizontal line, Hubo reports the calculated vertical distance using beepers.
   Thus, there will be no beepers on the line right after you load the `*.wld` file, but Hubo should drop beeper(s) as the program runs.

### Task
Implement a function calculate_distance where Hubo drops beepers as follows for xx=1, 2, …, 10:

1. Hubo first calculates the function value at $x=1$ and use the built-in round function to find the nearest integer as described in HW 2-1.
   You may assume the input parameters will be chosen so that $0.5 \le f(x) < 10.5$ for all $x=1, 2, …, 10$.

2. Hubo finds a town on the vertical line and calculates the vertical distance between a town and the train route on the the vertical line.

3. Hubo moves to the 11th horizontal line($y$ = 11) and drops beeper(s) with the amount of calculated distance.
   For example, if the proposed train route passes through (1, 7) and the town is located at (1, 10), Hubo should drop three beepers on (1, 11).
   If the vertical distance is zero, Hubo should not drop a beeper on the 11th horizontal line.

### Input
The function `calculate_distance` takes the same four parameters as HW 2-1. The function value should be computed in the same manner with given inputs.

### Output
The 11th horizontal line ($y$ = 11) will be used only as a report to citizens, so **TAs will only check the number of beepers dropped in the 11th horizontal line.**

----

## Homework 2-3-a

> Detour practice
Your task is to implement a function `detour_obstacle(hubo)` in which Hubo prepares for taking a detour when walking around the city in HW 2-3-b.

### IMPORTANT CHANGE
**All user-defined functions in your code should take a robot object as an argument. Otherwise, the grading code will not behave properly. For example,**

* GOOD: `def turn_right(hubo):`
* BAD: `def turn_right():`

### Types of obstacles
There are four types of obstacles as depicted below.

* horizontal (type A)
* perpendicular (type B, **rotatable**)
* opened-rectangular (type C, **either the west or the east side is opened**)
* rectangular (type D)

The length of any side in obstacles can vary. In addition, for type C and type D, to follow the definition of a rectangle, the length of parallel sides will be the same.

### Condition
You’ll be given an 11x10 city (i.e., 11 horizontal lines, 10 vertical lines) and at the beginning, Hubo is fixed at (5, 2) facing towards the north.
There will be an obstacle of random type in front of Hubo (in the north direction).

### Task
Implement a function `detour_obstacle` that makes Hubo move to the next available position in the same vertical line.
Then it returns the vertical distance between the start and end positions of Hubo. The examples below will help you understand the tasks.

### Input
The function `detour_obstacle(hubo)` takes a robot object hubo as an argument. All user-defined functions in your code should take a robot object as an argument.
Otherwise, the grading code will not behave properly. For example,

* GOOD: `def turn_right(hubo):`
* BAD: `def turn_right():`

### Output
* The function should return the vertical distance between the start and end positions.
* Hubo moves to the next available position on the same vertical line.

----

## Homework 2-3-b
> Get distance between the train route and each town when there exist many obstacles.

Your task is to implement a function `calculate_distance_with_obstacles(function_type, a, b, c)` in which Hubo calculates the vertical distance in a more realistically simulated city.

### Condition
You’ll be given an 11x10 city (i.e., 11 horizontal lines, 10 vertical lines) where **only one beeper** is dropped on each vertical line as same as HW 2-2 with one or more obstacles placed.

* For the sake of simplicity, we assume the followings.
  * Sides of any two different obstacles does not touch or overlap each other.
  * No obstacles touch the boundary of the city.
* There will be no obstacles above the 10th horizontal line.

### Task
Implement a function `calculate_distance_with_obstacles` where Hubo does the same as HW 2-2 except that Hubo should consider obstacles on the city.
For each vertical line, Hubo needs to check every reachable point until it finds a beeper.
If Hubo cannot access a beeper as it is located inside the obstacle, Hubo should drop **ten beepers** on the 11th horizontal line as Hubo cannot calculate the vertical distance.
The function `detour_obstacle()` you wrote in HW 2-3-a will help you solve this task.

### Input
The function `calculate_distance_with_obstacles` takes the same four parameters as HW 2-1. The way to compute the function value with given inputs is also the same.

### Output
The 11th horizontal line will be used as a report to the citizen, so **TAs will only check the number of beepers dropped on the 11th horizontal line**.