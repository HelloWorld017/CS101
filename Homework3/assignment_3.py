"""
Author - Jaeseok Huh (jaeseok.h@kaist.ac.kr), KAIST School of Computing
Date - Oct 19, 2019
"""


#################### BEGIN of DO NOT MODIFY ####################
## Do NOT MODIFY anything in this area

from constants import ingredients_info, recipes_info, allergy_types
from constants import ERR_WRONG_INGREDIENTS, ERR_LACK_INGREDIENTS, ERR_EMPTY_ORDER, ERR_UNKNOWN_SANDWICH, ERR_ALLERGY_FOOD_INCLUDED

## We maintain this variable throughout the entire execution.
stock = {}

"""
@return stock
"""
def getStock():
    global stock
    return stock
#################### END of DO NOT MODIFY ####################

import re

stock_regex = re.compile(r'^\s*(\d+) ([A-Za-z]+)\s*$')

"""
Task 3.1
@return is_success : Boolean
@return error_code : string (defined in `constants`)
"""
def initStock(initial_status):
    stocks_split = [stock for stock in initial_status.split(',') if stock.strip() != '']

    stocks_parsed = [
        stock_regex.match(stock_str) for stock_str in stocks_split
    ]
    
    stock_update = {}
    for stock_match in stocks_parsed:
        if not stock_match or stock_match.group(2) not in ingredients_info:
            return (False, ERR_WRONG_INGREDIENTS)
        
        stock_update[stock_match.group(2)] = int(stock_match.group(1))
    
    stock.clear()
    stock.update(stock_update)
    return (True, None)

"""
Task 3.2
@return is_success : Boolean
@return error_code : string (defined in `constants`)
"""
def updateStock(command, dict_ingredient_amount):
    multiplier = 1 if command == 'STORE' else -1
    update_items = {}
    
    for k, v in dict_ingredient_amount.items():
        if k not in ingredients_info:
            return (False, ERR_WRONG_INGREDIENTS)
    
    for k, v in dict_ingredient_amount.items():
        stock_value = stock[k] if k in stock else 0
        
        new_value = stock_value + v * multiplier
        
        if new_value < 0:
            return (False, ERR_LACK_INGREDIENTS)
        
        update_items[k] = new_value
    
    stock.update(update_items)
    
    for k in list(stock):
        if stock[k] == 0:
            del stock[k]
    
    return (True, None)

"""
Task 3.3
@return is_valid : Boolean
@return order_info : Dictionary (see the description regarding the details)
@return error_code : string (defined in `constants`)
"""
def validate(order, allergy_info):
    if not order:
        return (False, None, ERR_EMPTY_ORDER)
    
    if any([key not in recipes_info for key in order.keys()]):
        return (False, None, ERR_UNKNOWN_SANDWICH)
    
    ingredients = {}
    allergic_maps = set()
    
    for sandwich, count in order.items():
        for ingredient, ingredient_count in recipes_info[sandwich].items():
            if ingredient not in ingredients:
                ingredients[ingredient] = 0
            
            ingredients[ingredient] += count * ingredient_count
            
            allergy = ingredients_info[ingredient]['allergy']
            if allergy is not None:
                allergic_maps.add(allergy)
    
    for allergic in allergy_info:
        if allergic in allergic_maps:
            return (False, None, ERR_ALLERGY_FOOD_INCLUDED)

    prices, calories = zip(*[
        [
            ingredients_info[ingredient]['price'] * count,
            ingredients_info[ingredient]['calories'] * count
        ]
        for ingredient, count in ingredients.items()
    ])
	
	    
    """
	order_list = [
        key
        for key, value in order.items()
        for i in range(value)
    ]
	
    ingredients = [
        ingredient
        for sandwich in order_list
        for ingredient, count in recipes_info[sandwich].items()
        for i in range(count)
    ]
    
    food_allergics = set([
        ingredients_info[ingredient]['allergy']
        for ingredient in ingredients
    ])
    
    if any([
        allergic in food_allergics
        for allergic in allergy_info
    ]):
        return (False, None, ERR_ALLERGY_FOOD_INCLUDED)
    """
    
    return (True, {
        'price': sum(prices),
        'calories': sum(calories),
        'ingredients':ingredients
    }, None)

"""
Task 3.4
@return order_info : Boolean
@return error_code : string (defined in `constants`)
"""
def takeOrder(order, allergy_info):
    (valid, order_info, err_code) = validate(order, allergy_info)
    
    if not valid:
        return (False, err_code)
    
    (avail, err_code) = updateStock('CONSUME', order_info['ingredients'])
    
    if not avail:
        return (False, err_code)
    
    return (True, None)