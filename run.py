# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high
"""
1. Show items in the current room (check)
2. Pickup/Take the items in the current room
3. Action to print inventory
<<<<<<< HEAD
=======

2. Action to print inventory


User will write take item_name
Example: "take Mighty Sword"

Find item object from items that have the name that the user wanted
Match item object with found item key
Remove item_key from room item array
Add item_key to Player Inventory

>>>>>>> 6b16273 (Add inventory feature to check invetory)
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
      print_item(current_room)
      answer = prompt('What to do?: ')
      
      #Got this solution by stackflow, see readme
      action = answer.split(maxsplit=1)
      
      #Exit the game
      if(action[0] == 'exit'):
          print('Quitting the game..... byeeeeee!')
          break
      
      if action[0] == 'inventory' or action[0] == 'inv':
          print('checking the inventory...')
          print(game_data['player']['inventory'])
      
      if(action[0] == 'walk'):
        exit = select_exit(action[1], current_room)
        current_room = room_from_exit(exit, rooms_data)
      
      if(action[0] == 'take'):
          take_item = take_item()
          

      elif (action[0] == 'take'):
          

# Function for printing out a selected room
def print_room(room):sfaf
    print(room['description'])
    room_items = room['items']
    room_exits = room['exits']
    for exit in room_exits:
        print(exit['name'])
        print(exit['description'])
    
    items = game_data['items'] 
    for item_key in room_items:
        print(f'Item: {items[item_key]['name']}')
        print(f'Usage: {items[item_key]['description']}')
    
"""

"""

def print_item(room):
    room_items = room['items']
    items = game_data['items']
    for item in room_items:
        item_name = items[item]['name']
        item_desc = items[item]['description']
        print(item_name)
        print(item_desc)

def take_item(item_name, inventory, room):
    room_item_list = game_data['rooms'][room]['items']
    room_items = game_data['items']
    player_inventory = game_data['player']['inventory']
    for key in game_data['items']:
        room_item_name = room_items[key]['name']
        if room_item_name == 'item_name':
            room_item_list.remove(key)
            player_inventory.append(key)


    



        



    


"""

"""


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