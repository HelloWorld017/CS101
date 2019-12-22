## Homework 3
> Sandwich Order System

Read the homework description carefully and follow the instructions. Please be fully aware that this homework is an individual task;
you may discuss the problem with your friends, but you must not implement your ideas together.
You will fail the entire course (simply, you will be given an F for CS101 course) if you are found to be involved in any form of plagiarism.

* Customers can validate an order (menu + allergy).
* Recipes, ingredients, and allergy types are predefined and will be given.
* For each order, the system checks stocks and allergy in order to determine whether it can be served or not.
* If the order can be served, the system returns total price and nutrition information.
* Otherwise, it informs that it cannot be served along with predefined error messages, which explains the reason.
* Task 3.1 and Task 3.2 are for initializing and managing the stocks.
* Task 3.3 is for validating a customer’s order.
* Task 3.4 is for processing the order.
* The functions that you implemented will be imported and called in the grading module to automatically grade your submission.
  You may test your implementation of the functions on your own before the submission, but do not print anything to standard output in your submission.
  (e.g. do not use the print() function)

### Preliminaries
#### [Order]
The system will be given an order in the form of a Python dictionary. It stores a sandwich name as a key and the number of sandwiches as its item as follows.
You may assume that every key consists of alphabet characters(‘A-Za-z’) and spaces(‘ ‘).

Example: `order = {‘Chicken’: 2, ‘CheeseBacon’: 1, ‘Giant’: 2}`

#### [Variables]
We define the variable, `stock`, and import three variables from constant.py at the skeleton code:
`ingredients_info`, `recipes_info`, and `allergy_types`. `stock` is an abstraction of the warehouse.
Its value is an empty dictionary at the beginning.
During the execution, you should maintain the dictionary with its key being the ingredient and its value being the amount thereof.
The amount of each ingredient must always be a positive integer.

Example: `stock = {‘whitebread’: 7, ‘croissant’: 1, ...}.`

`ingredients_info` is a predefined nested dictionary representing all information about the ingredients of sandwiches.
Do not modify this variable. A key is the name of an ingredient and the corresponding item is a Python dictionary with three keys: `‘price’`, `'calories'`, and `‘allergy’`.
The `price` and the `calories` of every ingredient are given as positive integers.
The item of `‘allergy’` must be one of a string element in the globally defined set, `allergy_types`.
See 4 for details. In this project, you may assume that an ingredient causes at most one allergy.
If an ingredient does not cause any allergy, the corresponding value is None.

Example:
```py
ingredients_info = {
	‘whitebread’: {‘price’: 800, 'calories': 380, ‘allergy’: ‘Wheat’}, 
	‘croissant’: {‘price’: 1000, 'calories': 250, ‘allergy’: ‘Egg’},
	...
}
```

`recipes_info` is a predefined nested dictionary that describes all recipes of sandwiches the store sells.
There are five sandwiches in total. Do not modify this variable.
A key is the name of a sandwich, and the corresponding item is a Python dictionary that stores an ingredient name as a key and its amount (a positive integer) as the corresponding item.

Example:
```py
recipes_info = {
	‘Vegan’: {‘whitebread’: 1, ‘lettuce’: 10, ‘tomato’: 5}, 
	...
}
```

#### [Error messages]
We have five predefined error messages (string) in this project as below. Do not modify these error messages.

* `ERR_WRONG_INGREDIENTS` = ‘There is an ingredient we never use’
* `ERR_LACK_INGREDIENTS` = ‘One or more ingredients are not prepared’
* `ERR_EMPTY_ORDER` = ‘Sandwich is missing in your order’
* `ERR_UNKNOWN_SANDWICH` = ‘Your order includes a sandwich we do not serve’
* `ERR_ALLERGY_FOOD_INCLUDED` = ‘We found your order includes an ingredient conflicting with the allergy type(s) you’d notified’

----

### Task 3.1
> Stock Initialization

Complete the function `initStock(initial_status)`.

#### [Description]
This function initializes the value of `stock` according to the input string `initial_status`.

#### [Input]
The argument `initial_status` is a string that demonstrates the amount of each ingredient to be filled in the stock. It is written in the following format:

Example: `initial_status = ‘(amount) (ingredient), …, (amount) (ingredient)’`

Here, every (amount) is an integer. Each (ingredient) is the name of an ingredient.

The name of each ingredient is given in a singular form, not a plural form.
Every amount and comma in the string are followed by a single space.
You can assume that an ingredient appears at most once in the string.
Note that an empty string can also be given as an input.
The name of each ingredient consists only of alphabet characters(‘A-za-z’) and does not contain any whitespace in between.
There is always no comma at the end of the string.

#### [Output]
This function returns a tuple `(is_success, error_code)`

1. If initial_status includes an ingredient which does not appear in `ingredients_info`,
   this function should not change the value of stock at all and return `(False, ERR_WRONG_INGREDIENTS)`.

2. Otherwise, the update was successful, return `(True, None)`.

#### [Examples]
```py
>>> initStock(‘’)
(True, None)
>>> stock
{}
>>> initStock(‘100 whitebread, 3 lemon’)
(False, ERR_WRONG_INGREDIENTS)
>>> stock
{}
>>> initStock(‘100 whitebread, 40 tomato, 30 egg, 57 lettuce’)
(True, None)
>>> stock
{‘whitebread’: 100, ‘tomato’: 40, ‘egg’: 30, ‘lettuce’: 57} 
```

----

### Task 3.2
> Stock Management

Complete the function `updateStock(command, dict_ingredient_amount)`.

#### [Description]
This function updates the value of the `stock` according to the given `command` and `dict_ingredient_amount`.

* [Store] If the `command` is `‘STORE’` (a Python string), this function adds ingredients to the stock according to the second argument, `dict_ingredient_amount`.
  If new ingredients are given and no error arises, you should add new keys to the stock accordingly.
  You may assume that the name of each ingredient consists of only alphabets (‘A-Za-z’) without any whitespace.

* [Consume] If the `command` is `‘CONSUME’` and no error arises, this function subtracts the amount of each ingredient in
  `dict_ingredient_amount` from the `stock`.
  In case the amount of an ingredient becomes exactly 0, this function deletes the key from the stock, rather than keeping its amount as 0.

#### [Input]
The first argument `command` is one of the following two strings: `‘STORE’` and `‘CONSUME’`.
The second argument `dict_ingredient_amount` is a dictionary that stores an ingredient name as a key and its amount (a positive integer) as the corresponding item.
Note that `dict_ingredient_amount` might be an empty dictionary.

Example: `dict_ingredient_amount = {‘bacon’: 1, ‘tomato’: 2}`

#### [Output]
This function returns a tuple `(is_success, error_code)`

1. Regardless of the type of the command, if `dict_ingredient_amount` includes an ingredient which does not appear in `ingredients_info`,
   this function should not change the value of `stock` at all and return `(False, ERR_WRONG_INGREDIENTS)`.

2. If all the ingredients in `dict_ingredient_amount` appear in `ingredients_info` but there is not sufficient amount of an ingredient to be “consume”d
   (including the case where there is no corresponding ingredient key in the `stock`)–for even one kind,
   the function `updateStock` does not modify the value of stock, and returns `(False, ERR_LACK_INGREDIENTS)`.

3. Otherwise, the update was successful, it returns `(True, None)`.

#### [Example]
```py
>>> stock
{‘tomato’: 40, ‘egg’: 30, ‘lettuce’: 57}
>>> updateStock(‘STORE’, {‘lettuce’: 3, ‘bacon’: 50})
(True, None)
>>> stock
{‘tomato’: 40, ‘egg’: 30, ‘lettuce’: 60, ‘bacon’: 50}
>>> updateStock(‘CONSUME’, {‘lettuce’: 10})
(True, None)
>>> stock
{‘tomato’: 40, ‘egg’: 30, ‘lettuce’: 50, ‘bacon’: 50}
>>> updateStock(‘CONSUME’, {‘lemon’: 3, ‘lettuce’: 100})
(False, ERR_WRONG_INGREDIENTS)
( Note that even though we do not have enough amount of lettuce, the error code should be ERR_WRONG_INGREDIENTS, as the lemon does not appear in the ingredients_info. )
>>> updateStock(‘CONSUME’, {‘tomato’: 10, ‘cheese’: 1})
(False, ERR_LACK_INGREDIENTS)
>>> stock
{‘tomato’: 40, ‘egg’: 30, ‘lettuce’: 50, ‘bacon’: 50}
>>> updateStock(‘CONSUME’, {‘tomato’: 10, ‘egg’: 30})
(True, None)
>>> stock
{‘tomato’: 30, ‘lettuce’: 50, ‘bacon’: 50}
```

----

### Task 3.3
> Order Validation

Complete the function `validate(order, allergy_info)`. To implement this function, you need to reference both `recipes_info` and `ingredients_info`.
Note that this function does not modify any states at all and that it does not even check the value of `stock`.

#### [Description]
This function receives and checks the validity of the order along with the allergic restriction of the customer.

#### [Input]
The first argument `order` is a Python dictionary representing a customer’s order as described in preliminaries.
The second argument `allergy_info` is given as a subset of the globally defined set, `allergy_types`.
It is a set of allergy types that the customer must avoid.

Example: `order = {‘Chicken’: 2, ‘CheeseBacon’: 1, ‘Giant’: 2}`

Example: `allergy_types = {‘Egg’, ‘Fish’, ‘Milk’, ‘Soybeans’, ‘Wheat’}`

#### [Output]
This function returns a tuple `(is_valid, order_info, error_code)` where `is_valid` is a boolean that indicates whether the order is valid or not.
`order_info` is a dictionary of the form `{‘price’: price, 'calories': calories, ‘ingredients’: ingredients}`.
`price` and `calories` are the total price and calories of all the sandwiches in the order, respectively.
Here, `ingredients` is again a Python dictionary whose keys are all kinds of the ingredients we need to make all the sandwiches in the order.
Each item is the exact amount of the corresponding ingredient we should consume.
`error_code` is one of the predefined error messages.

Example: `order_info = {‘price’: 5000, 'calories': 660, ‘ingredients’: {‘whitebread’: 2, ‘bacon’: 2, ‘lettuce’: 4, ‘tomato’: 2}}`

1. If the `order` is an empty dictionary, return `(False, None, ERR_EMPTY_ORDER)`.
2. If the `order` is not empty and includes the name of a sandwich that does not appear in `recipes_info`, return `(False, None, ERR_UNKNOWN_SANDWICH)`.
3. When the `order` is not an empty dictionary and all the sandwiches in the `order` are known,
   if any of the required ingredients has an allergy type included in the `allergy_info`, return `(False, None, ERR_ALLERGY_FOOD_INCLUDED)`.

4. Otherwise, the order is valid, return `(True, order_info, None)`.

#### [Example]
```py
>>> validate({}, {‘Egg’, ‘Milk’})
(False, None, ERR_EMPTY_ORDER)
>>> validate({‘Turkey’: 1}, set())
(False, None, ERR_UNKNOWN_SANDWICH)
>>> validate({‘Croissant’: 1, ‘Turkey’: 1}, {‘Egg’, ‘Milk’})
(False, None, ERR_UNKNOWN_SANDWICH)
( Note that even though the order is containing an allergy conflict, the error code should be ERR_UNKNOWN_SANDWICH, as we do not have ‘Turkey Sandwich’ in recipes_info.)
>>> validate({‘Croissant’: 1, ‘Pescatarian’: 2}, {‘Egg’, ‘Milk’})
(False, None, ERR_ALLERGY_FOOD_INCLUDED)
>>> validate({‘Pescatarian’: 2}, {‘Egg’, ‘Milk’})
(True, {‘price’: 12000, 'calories': 3040, ‘ingredients’: {‘whitebread’: 2, ‘lettuce’: 6, ‘tomato’: 4, ‘tuna’: 4}}, None)
```

----

### Task 3.4
> Order Management

Complete the function `takeOrder(order, allergy_info)`.

#### [Description]
This function receives an order and allergic restriction of the customer. If the order is valid, make sandwiches by consuming ingredients from the stock.

#### [Input]
The input arguments (`order`, `allergy_info`) meet the same condition as validate. (See 3.3).

#### [Output]
This function returns a tuple `(is_success, error_code)` where `is_success` is a boolean value that indicates whether the order has been served successfully or not.
`error_code` is one of the predefined error messages described in preliminaries.

1. Check the validity of the `order` by using the function `validate` of task 3.3.
2. If `is_success` in the return value of the function `validate` is False, return with one of the error_code below.
  * `(False, ERR_EMPTY_ORDER)`
  * `(False, ERR_UNKNOWN_SANDWICH)`
  * `(False, ERR_ALLERGY_FOOD_INCLUDED)`

3. If the `order` is valid, update the `stock` by using the function `updateStock` of task 3.2.
   And if `is_success` in the return value from the function `updateStock` is False, return the `error_code` of the function `updateStock`.

4. Otherwise, i.e. the `order` has been served successfully, return `(True, None)`

#### [Example]
```py
>>> stock
{‘whitebread’: 100, ‘tomato’: 40, ‘cheese’: 30, ‘lettuce’: 50, ‘bacon’: 50}
>>> takeOrder({}, {‘Egg’, ‘Milk’})
(False, ERR_EMPTY_ORDER)
>>> takeOrder({‘CheeseBacon’: 1, ‘Turkey’: 1}, {‘Egg’, ‘Milk’})
(False, ERR_UNKNOWN_SANDWICH)
( Note that even though the order is containing an allergy conflict, the error code should be ERR_UNKNOWN_SANDWICH, as we do not have ‘Turkey Sandwich’ in recipes_info.)
>>> takeOrder({‘CheeseBacon’: 100}, {‘Egg’, ‘Milk’})
(False, ERR_ALLERGY_FOOD_INCLUDED)
>>> takeOrder({‘CheeseBacon’: 100}, {‘Egg’})
(False, ERR_LACK_INGREDIENTS)
>>> stock
{‘whitebread’: 100, ‘tomato’: 40, ‘cheese’: 30, ‘lettuce’: 50, ‘bacon’: 50}
>>> takeOrder({‘CheeseBacon’: 15}, {‘Egg’})
(True, None)
>>> stock
{‘whitebread’: 85, ‘tomato’: 25, ‘lettuce’: 20, ‘bacon’: 20}
```

----

Do not modify `constants.py`.

Please follow the instuction in PDF.

### Testcases
Testcase 1-19 are allotted 2 points each.
Testcase 1-4 are for Task 3.1.
Testcase 5-10 are for Task 3.2.
Testcase 11-15 are for Task 3.3.
Testcase 16-19 are for Task 3.4.

Testcase 20-31 are allotted 1 point each and for the entire program. You may not get any points for these cases if any of the Testcase 1-19 has failed.
