# Provides advanced interactive command-line prompts
from prompt_toolkit import prompt
import time
import json


# Load initial game data from the JSON file at startup
with open("./assets/game.json") as f:
    game_data = json.load(f)


def reset_game():
    """Reloads game data to fully reset the game state."""
    global game_data, rooms_data, starting_room_key, previous_room, current_room, player, items, static_items

    # Read the latest game state from the JSON file to reset all variables
    with open("./assets/game.json") as f:  # Reload from JSON
        game_data = json.load(f)

    # Reassign game data to local/global variables for use throughout the game
    rooms_data = game_data["rooms"]
    starting_room_key = game_data["starting_room"]
    previous_room = None
    current_room = rooms_data[starting_room_key]
    player = game_data["player"]
    items = game_data["items"]
    static_items = game_data["static_items"]

    print("\n New game started!\n")


def show_menu():
    """Displays the main menu and handles user menu choices."""
    while True:
        print("\n=== Main Menu ===")
        print("1. New Game")
        print("2. Instructions")
        print("3. Credits")
        print("4. Exit")

        choice = input("Enter your choice (1-4): ")

        # Routes user input to the correct game function or exits
        if choice == "1":
            reset_game()
            run_game()
        elif choice == "2":
            show_instructions()
        elif choice == "3":
            show_credits()
        elif choice == "4":
            print("Thanks for playing! Goodbye!")
            return
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")


def show_instructions():
    """Displays the game instructions from the loaded JSON data."""
    print("\n=== Instructions ===")
    print(game_data["instructions"])
    input("Press Enter to return to the menu...")


def show_credits():
    """Displays the game credits from the loaded JSON data."""
    print("\n=== Credits ===")
    print(game_data["credits"])
    input("Press Enter to return to the menu...")


def run_game():
    """Main game loop where player input is processed and the game state updates accordingly."""
    rooms_data = game_data["rooms"]
    starting_room_key = game_data["starting_room"]
    previous_room = None
    current_room = rooms_data[starting_room_key]
    player = game_data["player"]
    items = game_data["items"]
    static_items = game_data["static_items"]
    start_time = time.time()  # Records the starting time for the session

    # Provide initial room details to the player
    print_room(current_room)
    print_static_items_from_room(current_room, static_items)
    print_item(current_room)

    while True:
        answer = prompt("What to do?:\n")  # Prompt for user input

        # Process the user’s input by splitting into action and target
        action = answer.split(maxsplit=1)

        if len(action) > 0:
            action[0] = action[0].lower()
        else:
            action = [" "]

        if len(action) > 1:
            action[1] = action[1].lower()

        # Handle various user commands

        # Exit the game
        if action[0] == "exit":
            print("Quitting the game..... byeeeeee!")
            break

        elif action[0] == "inventory" or action[0] == "inv":
            # Display the player's current inventory
            if len(player["inventory"]) == 0:
                print("You have nothing in your inventory.")
            else:
                print_inventory(player, items)

        elif action[0] == "walk":
            # Allows player to move to another room if they specify a valid exit
            if len(action) == 1:  # No destination provided
                print(
                    "Walk where?\nYou need to specify where to walk. Try: walk [exit]"
                )
            else:
                exit = select_exit(action[1], current_room)
                if exit is None:  # Exit doesn't exist
                    print(
                        f"There is no exit named " +
                        action[1] + " in this room."
                    )
                elif exit["locked"]:
                    print(exit["locked_description"])
                else:
                    previous_room = current_room
                    current_room = room_from_exit(exit, rooms_data)
                    print("You enter... ")
                    print_entire_room(current_room, static_items)

        elif action[0] == "take":
            # Allows player to pick up an item if it exists and is not a static item
            if len(action) == 1:  # No item provided
                print(
                    "Take what? \nYou need to specify what to take. Try: take [item]"
                )
            else:
                item_key = get_item_key_from_item_name(action[1], items)
                static_item_key = get_static_item_key_from_static_item_name(
                    action[1], static_items
                )
                if static_item_key in current_room["static_items"]:
                    print(
                        f"I can't put {action[1].title()} in my pocket, it doesn't fit."
                    )
                elif item_key not in current_room["items"]:
                    print(f"I can't take {action[1].title()}.")
                else:
                    take_item(action[1], current_room, items, player)
                    print(f"You take the.... {action[1].title()}")

        elif action[0] == "attack" or action[0] == "open":
            # Allows player to interact with static items using attack/open
            if len(action) == 1:  # No target provided
                print(
                    f"{action[0].capitalize()} what? \nYou need to specify what to {action[0]}. Try: {action[0]} [item]"
                )
            else:
                static_item_data = get_static_item_from_static_item_name(
                    action[1], static_items
                )

                if static_item_data is None:
                    print(f"You can't {action[0]} '{action[1].title()}'.")
                else:
                    static_item_key, static_item = static_item_data

                    # Check if action is allowed on the static item
                    if action[0] in static_item.get("allowed_action", {}):
                        print(
                            static_item["allowed_action"][action[0]]["message"]
                        )  # Print success message
                        if action[0] == "open":
                            # If opening, move items inside to the player's inventory
                            for item_key in static_item.get("items", []):
                                add_item_key_to_player_inventory(
                                    item_key, player
                                )
                            static_item["items"] = []

                    # If action is not allowed, print the relevant message
                    elif action[0] in static_item.get("not_allowed_actions", {}):
                        print(
                            static_item["not_allowed_actions"][action[0]][
                                "message"
                            ]
                        )
                    else:
                        print(f"You can't {action[0]} '{action[1].title()}'.")
        elif action[0] == "use":
            # Allows the player to use an item in their inventory on something
            if len(action) == 1:  # No item provided
                print(
                    "Use what? \nYou need to specify an item to use. Try: use [item]"
                )
            else:
                (item_key, item) = get_item_from_inventory(
                    items, action[1], player
                )

                if item_key is None:  # Item not found in inventory
                    print(f"You don’t have '{action[1]}' in your inventory!")
                else:
                    use_on = prompt(
                        "What do you want to use " + action[1] + " with? \n"
                    )
                    if item["category"] == "exit_opener":
                        # If item is intended to unlock exits
                        exit = select_exit(use_on, current_room)
                        if exit is None:
                            print(f"There is no exit called '{use_on}'.")
                        else:
                            exit_event = exit.get("exit_openers", {}).get(
                                item_key
                            )
                            if exit_event:
                                exit["locked"] = False
                                print(exit_event["open_description"])
                            else:
                                print(
                                    f"You can't use '{action[1]}' on '{use_on}'."
                                )
                    elif item["category"] == "static_item_effect":
                        # If item is intended to affect static items in the room
                        static_item_data = get_static_item_from_static_item_name(
                            use_on, static_items
                        )

                        if static_item_data is None:
                            print(
                                f"You can't use '{action[1].title()}' on '{use_on.title()}'."
                            )
                        else:
                            static_item_key, static_item = static_item_data
                            item_effects = (
                                item["use_on"]
                                .get(static_item_key, {})
                                .get("effects", [])
                            )
                            # Handle the possible effects of using the item
                            for effect in item_effects:
                                if effect["type"] == "die":
                                    print(effect["message"])
                                    end = time.time()
                                    length = end - start_time
                                    print(
                                        f"Your game took {length:.2f} seconds."
                                    )
                                    # Return to main menu after a short pause
                                    input(
                                        "Press Enter to return to the main menu..."
                                    )
                                    return "RETURN_TO_MENU"
                                elif effect["type"] == "add_item":
                                    print(effect["message"])
                                    add_item_key_to_player_inventory(
                                        effect["item_key"], player
                                    )
                                elif effect["type"] == "win_game":
                                    print(effect["message"])
                                    end = time.time()
                                    length = end - start_time
                                    print(
                                        f"Your game took {length:.2f} seconds."
                                    )
                                    input(
                                        "Press Enter to return to the main menu..."
                                    )
                                    return "RETURN_TO_MENU"
        elif action[0] == "look_around":
            # Refreshes the room description and its items
            print_entire_room(current_room, static_items)
        elif action[0] == "go_back":
            # Allows returning to the previously visited room if it exists
            if previous_room is None:
                print("I can't go back!")
            else:
                current_room = previous_room
                print_entire_room(current_room, static_items)
                previous_room = None
        else:
            # Fallback for unrecognized commands
            print("I don't know how to... " + action[0])
            print(
                """I know how to:
                    walk [room name]
                    take [item name]
                    attack [name of something in the room]
                    open [name of something in the room]
                    look_around
                    go_back
                    inventory
                    exit << to quit the game >>
                  """
            )


def print_entire_room(room, static_items):
    """Displays the room description, its static items, and any items present."""
    print_room(room)
    print_static_items_from_room(room, static_items)
    print_item(room)


def print_inventory(player, items):
    """Lists all items currently in the player’s inventory."""
    print("Checking the inventory...")
    if not player["inventory"]:
        print("You have nothing in your inventory.")
        return

    inventory_items = [
        items[item_key]["name"].title() for item_key in player["inventory"]
    ]
    print(", ".join(inventory_items))  # Make it look nice


def print_static_items_from_room(room, static_items):
    """Displays static items found in the current room."""
    for static_item_key in room["static_items"]:
        print(static_items[static_item_key]["name"])
        print(static_items[static_item_key]["description"])


def print_room(room):
    """Prints the current room's description and outlines all exits."""
    print(room["description"])
    print("------------------------------------------------------")
    print("You look around and see...")
    room_exits = room["exits"]
    for exit in room_exits:
        print("===========================================================")
        print(exit["name"] + " - " + exit["description"])
        print("===========================================================")


def print_item(room):
    """Prints the names and descriptions of any items located in the current room."""
    room_items = room["items"]
    items = game_data["items"]
    for item in room_items:
        item_name = items[item]["name"]
        item_desc = items[item]["description"]
        print(item_name)
        print(item_desc)


def take_item(item_name, room, items, player):
    """Moves a specified item from the current room to the player's inventory."""
    item_key = get_item_key_from_item_name(item_name, items)
    remove_item_key_from_room_items(item_key, room)
    add_item_key_to_player_inventory(item_key, player)


def get_item_from_inventory(items, item_name, player):
    """
    Searches the player's inventory for an item matching the given name.
    Returns a tuple (item_key, item_dict) or (None, None) if not found.
    """
    item_name = item_name.lower()
    for item_key, item in items.items():
        if item["name"].lower() == item_name:
            if item_key in player["inventory"]:
                return (item_key, item)
    return None, None


def get_item_key_from_item_name(item_name, items):
    """Returns the item key from the 'items' dict if the name matches, else None."""
    item_name = item_name.lower()  # Normalize input to lowercase
    for key, item in items.items():
        if item["name"].lower() == item_name:  # Compare in lowercase
            return key
    return None  # If no match is found


def remove_item_key_from_room_items(item_key, room):
    """Removes an item key from the room's item list."""
    room_items = room["items"]
    room_items.remove(item_key)


def remove_item_key_from_static_item(item_key, static_item):
    """Removes an item key from a static item's 'items' list."""
    items_in_static_item = static_item["items"]
    items_in_static_item.remove(item_key)


def add_item_key_to_player_inventory(item_key, player):
    """Adds an item key to the player's inventory."""
    inventory = player["inventory"]
    inventory.append(item_key)


def attack_static_item(action, static_item_name, static_items):
    """
    Attempts to attack a static item if the corresponding
    action is listed in the static item's properties.
    """
    (static_item_key, static_item) = get_static_item_from_static_item_name(
        static_item_name, static_items
    )

    if action in static_item["not_allowed_actions"].keys():
        print_not_allowed_message_from_static_item(static_item, action)


def get_static_item_from_static_item_name(static_item_name, static_items):
    """
    Retrieves a static item's dictionary from its name.
    Returns (static_item_key, static_item) or None if not found.
    """
    static_item_name = static_item_name.lower()  # Normalize input
    for static_item_key in static_items:
        current_static_item_name = static_items[static_item_key]["name"].lower(
        )
        if current_static_item_name == static_item_name:
            return (static_item_key, static_items[static_item_key])
    return None  # Ensure it always returns a value


def print_not_allowed_message_from_static_item(static_item, action):
    """Prints the 'not allowed' message for a given static item action."""
    message = static_item["not_allowed_actions"][action]["message"]
    print(message)


def open_static_item(action, static_item_name, static_items, player):
    """Handles opening static items if the 'open' action is allowed."""
    static_item_key = get_static_item_key_from_static_item_name(
        static_item_name, static_items
    )

    static_item = static_items[static_item_key]

    if "open" in static_item.get("allowed_action", {}):
        print_allowed_message_from_static_item(static_item, action)
        for item_key in static_item["items"]:
            add_item_key_to_player_inventory(item_key, player)
        static_item["items"] = []


def get_static_item_key_from_static_item_name(static_item_name, static_items):
    """Returns the key of a static item if its name matches the provided argument."""
    static_item_name = static_item_name.lower()  # Normalize input to lowercase
    for static_item_key, static_item in static_items.items():
        if static_item["name"].lower() == static_item_name:
            return static_item_key
    return None  # Prevents KeyError if no match is found


def print_allowed_message_from_static_item(static_item, action):
    """Prints the allowed action message for a given static item."""
    message = static_item["allowed_action"][action]["message"]
    print(message)


"""

"""


def select_exit(exit_name, current_room):
    """Finds and returns an exit within the current_room by matching the exit's name."""
    exit_name = exit_name.lower()  # Normalize input
    for exit in current_room["exits"]:
        if exit_name == exit["name"].lower():  # Normalize comparison
            return exit  # ✅ Returns the correct exit immediately
    return None  # ✅ Always returns a value (prevents crash)


def room_from_exit(exit, rooms_data):
    """Retrieves the destination room data based on the exit's destination key."""
    exit_destination = exit["destination"]
    room = rooms_data[exit_destination]
    return room


if __name__ == "__main__":
    show_menu()  # Start with menu instead of running the game immediately
