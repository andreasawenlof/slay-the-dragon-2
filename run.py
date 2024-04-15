# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high
"""
Add exit action to close the game
"""

import json
from prompt_toolkit import prompt

with open('./assets/game.json') as f:
    game_data = json.load(f)


print('Starting Room', game_data['starting_room'])

def run_game():
    rooms_data = game_data['rooms']
    room_key = game_data['starting_room']
    current_room = rooms_data[room_key]
    while True:
      print_room(current_room)
      answer = prompt('What to do?: ')
      
      #Exit the game
      if(answer == 'exit'):
          break
      
      exit = select_exit(answer, current_room)
      current_room = room_from_exit(exit, rooms_data)

# Function for printing out a selected room
def print_room(room):
    print(room['description'])
    room_exits = room['exits']
    for exit in room_exits:
        print(exit['name'])
        print(exit['description'])


def select_exit(exit_name, current_room):
    for exit in current_room['exits']:
        if(exit_name == exit['name']):
            chosen_exit = exit
    return chosen_exit

def room_from_exit(exit, rooms_data):
    exit_destination = exit['destination']
    room = rooms_data[exit_destination]
    return room

run_game()


# print('You said: %s' % answer)

    #else:
    #    print(f"Your input is invalid, please chooose between the following exits {exit['name']}")