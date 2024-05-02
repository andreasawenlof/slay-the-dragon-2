# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high
"""

Static Items:
    Stationary in the room (cannot be moved) CHECK
        - print static items
    
    Interaction with static items
        Define what actions are allowed with respective static items
            - if action is allowed do action
                - call the appropriate action function (we start with open)

            - if action not allowed shame user
                - get static item key from static item name
                - get static item object from static item key
                - get message from not allowed in static item object
                - print message


        User write to open openable static items (COMPLETE LATER just add an empty function)
            - get item key from item name
            - action with item key
    
    
    State of item to change when interaction has been done
    
    
    static item kunna ha items i sig: CHECKED
        - ändra i json så att items kan vara i static items 
    
    
    vid interaction ska items flyttas till spelaren
        -

"""
import json
from prompt_toolkit import prompt

with open("./assets/game.json") as f:
    game_data = json.load(f)


print("Starting Room", game_data["starting_room"])


def run_game():
    rooms_data = game_data["rooms"]
    room_key = game_data["starting_room"]
    current_room = rooms_data[room_key]
    player = game_data["player"]
    items = game_data["items"]
    static_items = game_data["static_items"]

    print_room(current_room)
    print_static_items_from_room(current_room, static_items)
    print_item(current_room)
    
    while True:
        
        answer = prompt("What to do?: ")

        # Got this solution by stackflow, see readme
        action = answer.split(maxsplit=1)

        # Exit the game
        if action[0] == "exit":
            print("Quitting the game..... byeeeeee!")
            break

        elif action[0] == "inventory" or action[0] == "inv":
            print_inventory(player, items)

        elif action[0] == "walk":
            exit = select_exit(action[1], current_room)
            current_room = room_from_exit(exit, rooms_data)
            print('You enter... ')
            print_room(current_room)
            print_static_items_from_room(current_room, static_items)
            print_item(current_room)

        elif action[0] == "take":
            take_item(action[1], current_room, player, items)
            print(f"You take the.... {action[1]}")

        elif action[0] == "attack":
            attack_static_item(action[0], action[1], static_items)



def print_inventory(player, items):
    print("Checking the inventory...")
    inventory_print_str = ""
    for item_key in player["inventory"]:
        item_name = items[item_key]["name"]
        inventory_print_str += f"{item_name}, "
    inventory_print_str = inventory_print_str.rstrip(", ")
    print(inventory_print_str)

def print_static_items_from_room(room, static_items):
    for static_item_key in room['static_items']:
        print(static_items[static_item_key]['name'])
        print(static_items[static_item_key]['description'])



# Function for printing out a selected room
def print_room(room):
    print(room["description"])
    room_exits = room["exits"]
    for exit in room_exits:
        print(exit["name"])
        print(exit["description"])


def print_item(room):
    room_items = room["items"]
    items = game_data["items"]
    for item in room_items:
        item_name = items[item]["name"]
        item_desc = items[item]["description"]
        print(item_name)
        print(item_desc)


def take_item(item_name, room, player, items):
    item_key = get_item_key_from_item_name(item_name, items)
    remove_item_key_from_room_items(item_key, room)
    add_item_key_to_player_inventory(item_key, player)

    """
    room_item_list = game_data['rooms'][room]['items']
    room_items = game_data['items']
    player_inventory = game_data['player']['inventory']
    for key in game_data['items']:
        room_item_name = room_items[key]['name']
        if room_item_name == item_name:
            room_item_list.remove(key)
            player_inventory.append(key)
    return item_name;
    """


def get_item_key_from_item_name(item_name, items):
    for key in items:
        if item_name == items[key]["name"]:
            return key


def remove_item_key_from_room_items(item_key, room):
    room_items = room["items"]
    room_items.remove(item_key)


def add_item_key_to_player_inventory(item_key, player):
    inventory = player["inventory"]
    inventory.append(item_key)

def attack_static_item(action, static_item_name, static_items):
    static_item = get_static_item_from_static_item_name(static_item_name, static_items)
    
    if (action in static_item["not_allowed_actions"].keys()):
        print_not_allowed_message_from_static_item(static_item, action) 

def get_static_item_from_static_item_name(static_item_name, static_items):
    for static_item_key in static_items:
        current_static_item_name = static_items[static_item_key]['name']
        if(current_static_item_name == static_item_name):
            return static_items[static_item_key]

def print_not_allowed_message_from_static_item(static_item, action):
    message = static_item["not_allowed_actions"][action]["message"]
    print(message)



"""

"""


def select_exit(exit_name, current_room):
    for exit in current_room["exits"]:
        if exit_name == exit["name"]:
            chosen_exit = exit
    return chosen_exit


def room_from_exit(exit, rooms_data):
    exit_destination = exit["destination"]
    room = rooms_data[exit_destination]
    return room


run_game()


# print('You said: %s' % answer)

# else:
#    print(f"Your input is invalid, please chooose between the following exits {exit['name']}")
