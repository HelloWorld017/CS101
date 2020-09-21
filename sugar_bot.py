# A bot with sugars
# ====
# Originally developed for doing lab when I was in the class
# Updated for TA works

class SugarBot(Robot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.repeat = lambda fn: lambda *args: [fn(*args[1:]) for _ in range(args[0])] and None
        self.set_trace('blue')
    
    def move_until(self):
        while self.front_is_clear():
            self.move()

    def move_safe(self):
        if self.front_is_clear():
            self.move()
    
    def pick_safe(self):
        if self.on_beeper():
            self.pick_beeper()
    
    def pick_until(self):
        while self.on_beeper():
            self.pick_beeper()
    
    def drop_safe(self):
        if self.carries_beepers():
            self.drop_beeper()
    
    def drop_until(self):
        while self.carries_beepers():
            self.drop_beeper()
    
    def move_pick(self):
        self.move_safe()
        self.pick_until()
    
    def move_pick_until(self):
        self.pick_until()
        while self.front_is_clear():
            self.move_pick()
        
    def ensure_north(self):
        while not self.facing_north():
            self.turn_left()
    
    def direction_oddeven(self, direction = 0):
        return 1 if direction == 0 else 3
    
    def uturn(self, direction = 0):
        self.turn_left_n(self.direction_oddeven(direction))
        if not self.front_is_clear():
            return False
        
        self.move()
        self.turn_left_n(self.direction_oddeven(direction))
        return True
    
    def turn_right(self):
        self.turn_left_n(3)
    
    def turn_backward(self):
        self.turn_left_n(2)
    
    def __getattr__(self, name):
        if not name.endswith("_n"):
            return None
        
        repeat_fn = getattr(self, name[:-2], lambda: None)
        return self.repeat(repeat_fn)
