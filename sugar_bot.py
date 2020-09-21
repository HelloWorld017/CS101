# A bot with sugars

class SugarBot(Robot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.repeat = lambda fn: lambda *args: [fn(*args[1:]) for _ in range(args[0])] and None
        self.set_trace('blue')
    
    def move_until(self):
        while self.front_is_clear():
            self.move()

    def move_safe():
        if self.front_is_clear():
            self.move()
    
    def pick_safe():
        if self.on_beeper():
            self.pick_beeper()
    
    def pick_until():
        while self.on_beeper():
            self.pick_beeper()
    
    def drop_safe():
        if self.carries_beepers():
            self.drop_beeper()
    
    def drop_until():
        while self.carries_beepers():
            self.drop_beeper()
    
    def move_pick():
        self.move()
        self.pick_safe()
    
    def ensure_north(self):
        while not self.facing_north():
            self.turn_left()
    
    def __getattr__(self, name):
        if not name.endswith("_n"):
            return None
        
        repeat_fn = getattr(self, name[:-2], lambda: None)
        return self.repeat(repeat_fn)
