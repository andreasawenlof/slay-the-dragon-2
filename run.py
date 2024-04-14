# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high
"""
Spelaren ska kunna byta rum:
1. Ta emot input från spelaren
2. Tolka användarens input
3. Kod för att byta rum
"""

import json
from prompt_toolkit import prompt

with open('./assets/game.json') as f:
    game_data = json.load(f)


print('Starting Room', game_data['starting_room'])

rooms_data = game_data['rooms']
room_key = game_data['starting_room']
current_room = rooms_data[room_key]

# Function for printing out a selected room
def print_room(room):
    print(room['description'])
    room_exits = room['exits']
    for exit in room_exits:
        print(exit['name'])
        print(exit['description'])

print_room(current_room)

answer = prompt('Where do you want to go?: ')

for exit in current_room['exits']:
    if(answer == exit['name']):
        chosen_exit = exit
        print(chosen_exit)

# print('You said: %s' % answer)

    #else:
    #    print(f"Your input is invalid, please chooose between the following exits {exit['name']}")