from cs1robots import *
import math

#################################################
############## DO NOT MODIFY ABOVE ##############
#################################################


## Do not call 'calculate_distance_with_obstacles' function in this section.
## Instead, modifly the variables below to test your code.
city_name_to_load = 'sample_cities/towns_obs1.wld'
function_arguments = ['quad', 0.05, -1, 7]

debug = lambda *args: None

class DijkstraBot:
    directions = {
        0: (0, 1),
        1: (-1, 0),
        2: (0, -1),
        3: (1, 0)
    }
    
    def __init__(self, bot, position):
        self.start_position = position
        self.current_node = position
        self.direction = 0
        self.bot = bot
        self.graph = {}
        
        for x in range(1, 11):
            for y in range(1, 12):
                self.graph[(x, y)] = {
                    'visited': False,
                    'queue': None,
                    'connected': [],
                    'beeper': False
                }
        
        self.reverse_direction = {
            v: k for k, v in self.directions.items()
        }

        self.graph[self.current_node]['queue'] = []
        
        self.ensure_north()
    
    def ensure_north(self):
        while not self.bot.facing_north():
            self.bot.turn_left()
        
        self.direction = 0

    def get_connected_nodes(self):
        self.ensure_north()
        connected_nodes = []
        
        for i in range(4):
            if not self.bot.front_is_clear():
                self.bot.turn_left()
                continue

            conn = self.directions[i]
            connected_nodes.append(
                (self.current_node[0] + conn[0], self.current_node[1] + conn[1])
            )
            
            self.bot.turn_left()

        return connected_nodes

    def move_to(self, next_node):
        if self.current_node == next_node:
            return
        
        queue = self.graph[self.current_node]['queue']
        next_queue = self.graph[next_node]['queue']
        movement_queue = []
        
        start = 0
        for movement in reversed([self.start_position] + queue):
            if movement in next_queue:
                start = next_queue.index(movement)
                break
            
            movement_queue.append(movement)
        
        movement_queue = movement_queue + next_queue[start:]
        self.move_for_queue(movement_queue)
    
    def move_for_queue(self, queue):
        debug('move_for', queue)
        for movement in queue:
            if movement == self.current_node:
                continue
            
            movement_direction = self.reverse_direction[
                (
                    movement[0] - self.current_node[0],
                    movement[1] - self.current_node[1]
                )
            ]
            self.turn_to(movement_direction)
            self.bot.move()
            
            self.current_node = movement
    
    def turn(self, n = 1):
        for x in range(n):
            self.bot.turn_left()
        
        self.direction = ((self.direction + n) % 4 + 4) % 4
    
    def turn_to(self, target):
        turn_count = (((target - self.direction) % 4) + 4) % 4
        self.turn(turn_count)
    
    def distance(self, node):
        if self.graph[node]['queue'] is None:
            d = float('inf')
        
        else:
            d = len(self.graph[node]['queue'])
        
        return d

    def build_graph(self):
        next_node = self.current_node
        
        while next_node is not None:
            debug('visit', next_node)
            if self.graph[next_node]['queue'] is None:
                # Unreachable graph
                break
            
            self.move_to(next_node)
            
            if self.bot.on_beeper():
                self.graph[next_node]['beeper'] = True
            
            connected_nodes = self.get_connected_nodes()
            debug('connected', connected_nodes)
            
            for node in connected_nodes:
                distance = self.distance(node)
                if distance > self.distance(next_node) + 1:
                    self.graph[node]['queue'] = self.graph[next_node]['queue'] + [node]
            
            self.graph[next_node]['visited'] = True
            min_distance = float('inf')
            next_node = None

            for node, descriptor in self.graph.items():
                if descriptor['visited']:
                    continue
                
                distance = self.distance(node)
                if min_distance > distance:
                    min_distance = distance
                    next_node = node

func_list = {
    'quad': lambda a, b, c: lambda x: a * x ** 2 + b * x + c,
    'trig': lambda a, b, c: lambda x: a * math.sin(b * x) + c
}

def calculate_distance_with_obstacles(function_type, a, b, c):
    func = func_list[function_type](a, b, c)
    
    dijkstra = DijkstraBot(hubo, (1, 1))
    dijkstra.build_graph()
    
    town_positions = [None for i in range(10)]
    
    for node, descriptor in dijkstra.graph.items():
        if descriptor['beeper']:
            town_positions[node[0] - 1] = node[1]

    train_positions = [round(func(x)) for x in range(1, 11)]
    
    distances = [
        abs(town_positions[i] - fx) if town_positions[i] is not None else 10
        for (i, fx) in enumerate(train_positions)
    ]
    
    dijkstra.move_to((1, 11))
    dijkstra.turn_to(3)
    
    for i in range(10):
        for j in range(distances[i]):
            hubo.drop_beeper()
        
        if hubo.front_is_clear():
            hubo.move()

#################################################
############## DO NOT MODIFY BELOW ##############
#################################################

load_world(city_name_to_load)
hubo = Robot(beepers=100)

if __name__ == "__main__":
    calculate_distance_with_obstacles(function_arguments[0], function_arguments[1], function_arguments[2], function_arguments[3])