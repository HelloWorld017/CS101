from cs1robots import *
from cs1media import *
from elice_utils import EliceUtils
from time import sleep

# You can change the target ".wld" file for test here.
load_world('worlds/test_1.wld')

hubo = Robot()

image_width = 16
image_height = 16

# Set colors of pixels in this "image" object.
image = create_picture(image_width, image_height, (255, 255, 255))

########################################
# --- Your code starts from here ---

# [The regular way to do this things]

# Let's define some sugartic functions
hubo.set_trace('blue')
hubo.turn = lambda n = 1: [hubo.turn_left() for i in range(n)]

def pick_get():
    count = 0
    
    while hubo.on_beeper():
        hubo.pick_beeper()
        count += 1

    b = 255 - max(count * 16 - 1, 0)
    return (b, b, b)

# Right-side-turn
is_rhs = False
def traverse(callback):
    global is_rhs;
    
    for y in range(image_height):
        for x in range(image_width):
            callback(x, y)
            
            if hubo.front_is_clear():
                hubo.move()
        
        turn_size = 3 if is_rhs else 1
        hubo.turn(turn_size)

        if hubo.front_is_clear():
            hubo.move()

        hubo.turn(turn_size)

        is_rhs = not is_rhs


traverse(lambda x, y:
    image.set(
        image_width - x - 1 if is_rhs else x,
        image_height - y - 1,
        pick_get()
    )
)


"""
# [An easier way to do these things]
# 1-Line Coding is so nice!!
# Aw, I didn't know that this doesn't work on test case.

[(lambda k, b: image._pixels.__setitem__((k[0] - 1, image_height - k[1]), (b, b, b)))(key, 255 - max(count * 16 - 1, 0)) for (key, count) in getattr(__import__('cs1robots'), '_world').beepers.items()]


# Descriptions:
    # 1. There is a hidden variable _world in cs1robots.
    #    It has beeper property, which allows user for accessing world's beeper data.
    
    # 2. Using this, supply the key and brightness (which is calculated from beeper's count) to the lambda (IIFE)
    #    The lambda function sets pixel's (key[0] - 1, image_height - key[1]) to (b, b, b)
    #    I subtracted 1 from X Coordinate as beeper's index is one-based.
    #    I intentionally inverted Y Coordinate
    
    # 3. Simple?

# I am very sorry for
    # * not obeying PEP8,
    # * abusing & spamming array comprehension instead of for-loop,
    # * using dynamic import although it is not dynamic,
    # * using __setitem__ to avoid variable-assignment limit in lambda,
        # (:= operator was possible, but that is implemented in Python 3.8)
    # * creating useless lambda function for each loop,
    # * finally, last but not least, using not-documented properties (in cs1 libraries)

# But I hope you TA guys enjoy this one-lined code.
# If you enjoyed this, please push 'Like' and 'Subscribe' button in git.nenw.dev (GitHub @HelloWorld017)
"""

# --- Your code ends here ---
########################################

download_message = '⬇ Download the result image file from the link below ⬇'
print('#' * len(download_message))
print(download_message)
sleep(0.1)

# Save your image object as a file.
image.save_as('./result.png')
# Show a download link for your result image file.
utils = EliceUtils()
utils.send_file('./result.png')

sleep(0.1)
print('#' * len(download_message))
