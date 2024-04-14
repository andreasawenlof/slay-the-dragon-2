# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high
"""
1. Import game.json
2. Select the starting room
3. Print the rooms description
4. Print the rooms exit-names and descriptions
"""

import json

with open('./assets/game.json') as f:
    game_data = json.load(f)


print('Starting Room', game_data['starting_room'])

rooms_data = game_data['rooms']
room1 = rooms_data['room1']

# Function for printing out a selected room
def print_room(room):
    print(room['description'])
    room_exits = room['exits']
    for exit in room_exits:
        print(exit['name'])
        print(exit['description'])

print_room(room1)

