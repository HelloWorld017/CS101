from cs1robots import *
import math

#################################################
############## DO NOT MODIFY ABOVE ##############
#################################################

## Do not call 'demo_route' function in this section.
## Instead, modifly the variable below to test your code.
function_arguments = ['quad', 0, 1, 2]

func_list = {
    'quad': lambda a, b, c: lambda x: a * x ** 2 + b * x + c,
    'trig': lambda a, b, c: lambda x: a * math.sin(b * x) + c
}


def safe(fn):
    def safe_fn():
        try:
            return fn()

        except:
            return None
    
    return safe_fn


repeat = lambda fn: lambda n = 1: [fn() for i in range(n)] or None

def demo_route(function_type, a, b, c):
    hubo.set_trace('blue')
    
    turn = repeat(safe(hubo.turn_left))
    move = repeat(safe(hubo.move))
    beep = repeat(safe(hubo.drop_beeper))

    def place_at(y, count = 1):
        turn()
        move(y - 1)
        beep(count)
        turn(2)
        move(y - 1)
        turn()

    func = func_list[function_type](a, b, c)
    
    for x in range(10):
        f_x = func(x + 1)
        
        if f_x < 0.5:
            beep(3)
            move()
            continue
        
        if f_x >= 10.5:
            place_at(10, 3)
            move()
            continue
        
        place_at(round(f_x))
        move()


#################################################
############## DO NOT MODIFY BELOW ##############
#################################################

create_world()
hubo = Robot(beepers=100)

if __name__ == "__main__":
    demo_route(function_arguments[0], function_arguments[1], function_arguments[2], function_arguments[3])