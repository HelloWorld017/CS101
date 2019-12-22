from cs1robots import *

#################################################
############## DO NOT MODIFY ABOVE ##############
#################################################

## Do not call 'detour_obstacle' function in this section.
## Instead, modifly the variable below to test your code.
city_name_to_load = 'sample_cities/detour2.wld'

debug = lambda *args: None
# debug = lambda *args: print(*args)

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
                    'connected': []
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


def detour_obstacle(hubo):
    # hubo.set_trace('blue')
    dijkstra = DijkstraBot(hubo, (5, 2))
    dijkstra.build_graph()
    
    min_y = 99
    target_node = None
    for node, descriptor in dijkstra.graph.items():
        if node[0] != 5:
            continue
        
        if node[1] <= 2:
            continue
        
        if descriptor['queue'] is None:
            continue
        
        if node[1] < min_y:
            min_y = node[1]
    
    if min_y == 99:
        return float('inf')
    
    dijkstra.move_to((5, min_y))
    return min_y - 2


#################################################
############## DO NOT MODIFY BELOW ##############
#################################################

load_world(city_name_to_load)
hubo = Robot(orientation='N', avenue=5, street=2)

if __name__ == "__main__":
    detour_obstacle(hubo)