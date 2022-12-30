"""
This is a simple implementation of a random Agent in a Room that moves randomly until it capture the flag. 
"""
import random
import time

class Room:
    
    def __init__(self, size):
        self.size = size
        self.flag_position = None
        self.agent_position = None
        self.grid = [['.' for _ in range(size)] for _ in range(size)]

    def place_flag(self, x, y):
        self.flag_position = (x, y)
        self.grid[y][x] = 'F'
        
    def place_agent(self, x, y):
        self.agent_position = (x, y)
        self.grid[y][x] = 'A'

    def move_agent_broken(self, dx, dy):
        x, y = self.agent_position
        self.grid[y][x] = '.'
        self.agent_position = (x + dx, y + dy)
        self.grid[y+dy][x+dx] = 'A'
    
    def move_agent(self, dx, dy):
        x, y = self.agent_position
        self.grid[y][x] = '.'
        new_x, new_y = x + dx, y + dy
       
        # This is a flag for checking if the position is out of bounds 
        if 0 <= new_x < self.size and 0 <= new_y < self.size:
            self.agent_position = (new_x, new_y)
            self.grid[new_y][new_x] = 'A'
             
    def is_flag_captured(self):
        return self.flag_position == self.agent_position
    
    def print_room(self):
        
        for row in self.grid:
            print(' '.join(row))
                 

class Agent:
    
    def __init__(self, room):
        self.room = room
        self.directions = {"up":(0,-1), "down":(0,1), "left":(-1,0), "right":(1,0)}
  
    def move(self, direction):
        dy,dx = self.directions[direction]
        self.room.move_agent(dx, dy)
        
    def capture_flag(self):
        return self.room.is_flag_captured()


room = Room(15)
room.place_flag(7, 7)
room.place_agent(0, 0)

agent = Agent(room)
num_moves = 0

start_time = time.time()

while not agent.capture_flag():
    
    # Move the agent in a random direction
    room.print_room()
    print()
  
    direction = random.choice(list(agent.directions.keys()))
    agent.move(direction)
    print("Moving", direction)
  
    time.sleep(0.05)
    num_moves += 1
    
print("Flag captured!")

elapsed_time = time.time() - start_time

#Print time taken to capture the flag and number of moves
print("Time taken:", elapsed_time, "seconds")
print("Number of moves before capture:", num_moves)
