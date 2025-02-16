import json
import random
from prompt_toolkit import prompt

# Load game data
with open("./assets/game.json") as f:
    game_data = json.load(f)

print("Starting Room", game_data["starting_room"])


def run_game():
    rooms_data = game_data["rooms"]
    starting_room_key = game_data["starting_room"]
    previous_room = None
    current_room = rooms_data[starting_room_key]
    player = game_data["player"]
    items = game_data["items"]
    static_items = game_data["static_items"]

    print_room(current_room)
    print_static_items_from_room(current_room, static_items)
    print_item(current_room)

    while True:
        answer = prompt("What to do?:\n").strip().lower()
        action = answer.split(maxsplit=1)

        if not action:
            print("Invalid input.")
            continue

        command = action[0]
        target = action[1] if len(action) > 1 else None

        if command == "exit":
            print("Quitting the game..... byeeeeee!")
            break

        elif command in ["inventory", "inv"]:
            print_inventory(player, items)

        elif command == "walk" and target:
            exit = select_exit(target, current_room)
            if exit["locked"]:
                print(exit["locked_description"])
            else:
                previous_room = current_room
                current_room = room_from_exit(exit, rooms_data)
                print("You enter...")
                print_entire_room(current_room, static_items)

        elif command == "take" and target:
            take_item(target, current_room, items, player)

        elif command == "attack" and target:
            attack_static_item(target, static_items)

        elif command == "use" and target:
            (item_key, item) = get_item_from_inventory(items, target, player)
            if not item:
                print("You don't have that item!")
                continue
            use_on = prompt("What do you want to use the item with? \n")
            process_item_use(item_key, item, use_on,
                             current_room, static_items, player)

        elif command == "look_around":
            print("You look around and see...")
            print_entire_room(current_room, static_items)

        elif command == "go_back":
            if previous_room is None:
                print("I can't go back!")
            else:
                current_room = previous_room
                print_entire_room(current_room, static_items)
                previous_room = None

        else:
            print(f"I don't know how to do {command}")
            show_available_commands()

# Function for printing out a selected room


def print_entire_room(room, static_items):
    print_room(room)
    print_static_items_from_room(room, static_items)
    print_item(room)


def print_inventory(player, items):
    print("Checking the inventory...")
    inventory_print_str = ", ".join(
        [items[item_key]["name"] for item_key in player["inventory"]])
    print(inventory_print_str if inventory_print_str else "Your inventory is empty.")


def take_item(item_name, room, items, player):
    item_key = get_item_key_from_item_name(item_name, items)
    if item_key and item_key in room["items"]:
        room["items"].remove(item_key)
        player["inventory"].append(item_key)
        print(f"You take the {item_name}.")
    else:
        print("There is no such item here.")


def attack_static_item(static_item_name, static_items):
    static_item_key, static_item = get_static_item_from_static_item_name(
        static_item_name, static_items)
    if static_item_key:
        if "attack" in static_item.get("allowed_action", {}):
            print(static_item["allowed_action"]["attack"]["message"])
            if "effects" in static_item["allowed_action"]["attack"]:
                process_effects(
                    static_item["allowed_action"]["attack"]["effects"])
        else:
            print(static_item.get("not_allowed_actions", {}).get(
                "attack", {}).get("message", "You can't attack that!"))
    else:
        print("There's nothing to attack here.")


def process_item_use(item_key, item, use_on, current_room, static_items, player):
    static_item_key, static_item = get_static_item_from_static_item_name(
        use_on, static_items)
    if static_item_key and item_key in item.get("use_on", {}):
        effects = item["use_on"][static_item_key]["effects"]
        process_effects(effects)
    else:
        print("That item can't be used here.")


def process_effects(effects):
    for effect in effects:
        if effect["type"] == "die":
            print(effect["message"])
            exit()
        elif effect["type"] == "add_item":
            print(effect["message"])


def get_item_key_from_item_name(item_name, items):
    return next((key for key, item in items.items() if item["name"].lower() == item_name.lower()), None)


def get_static_item_from_static_item_name(static_item_name, static_items):
    for key, item in static_items.items():
        if item["name"].lower() == static_item_name.lower():
            return key, item
    return None, None


def select_exit(exit_name, current_room):
    return next((exit for exit in current_room["exits"] if exit_name.lower() == exit["name"].lower()), None)


def room_from_exit(exit, rooms_data):
    return rooms_data[exit["destination"]]


def show_available_commands():
    print("""
    I know how to: 
        walk [room name]
        take [item name]
        attack [name of something in the room]
        open [name of something in the room]
        look_around
        go_back
        inventory
        exit << to quit the game >> 
    """)


run_game()
