from cs1robots import *
import math

#################################################
############## DO NOT MODIFY ABOVE ##############
#################################################

## Do not call 'calculate_distance' function in this section.
## Instead, modifly the variables below to test your code.
city_name_to_load = 'sample_cities/towns1.wld'
function_arguments = ['quad', 0.05, -1, 7]

def safe(fn):
    def safe_fn():
        try:
            return fn()

        except:
            return None
    
    return safe_fn


repeat = lambda fn: lambda n = 1: [fn() for i in range(n)] or None

func_list = {
    'quad': lambda a, b, c: lambda x: a * x ** 2 + b * x + c,
    'trig': lambda a, b, c: lambda x: a * math.sin(b * x) + c
}

sugars = ()

def calculate_distance(function_type, a, b, c):
    global sugars
    
    func = func_list[function_type](a, b, c)
    sugars = (
        repeat(safe(hubo.turn_left)),
        repeat(safe(hubo.move)),
        repeat(safe(hubo.drop_beeper))
    )
    
    turn, move, beep = sugars
    town_positions = get_town_positions()
    train_positions = [round(func(x)) for x in range(1, 11)]
    
    distances = [
        abs(town_positions[i] - fx) for (i, fx) in enumerate(train_positions)
    ]
    
    turn()
    move(10)
    turn(3)
    
    for d in distances:
        beep(d)
        move()

def get_town_positions():
    turn, move, beep = sugars
    town_positions = []
    
    for x in range(10):
        turn()
        
        y = 1
        
        while not hubo.on_beeper():
            y += 1
            move()
        
        town_positions.append(y)
        turn(2)
        move(y)
        turn()
        move()
    
    turn(2)
    move(9)
    turn(2)
    
    return town_positions

#################################################
############## DO NOT MODIFY BELOW ##############
#################################################

load_world(city_name_to_load)
hubo = Robot(beepers=100)

if __name__ == "__main__":
    calculate_distance(function_arguments[0], function_arguments[1], function_arguments[2], function_arguments[3])