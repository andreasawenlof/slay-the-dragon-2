# Testing Documentation

## Overview

This document outlines the testing process for the **Slay the Dragon** text-based adventure game. Each test case includes the expected behavior, the actual outcome, and whether the test passed or failed.

## Test Cases

| **Test Case**                             | **Expected Behavior**                                                              | **Actual Outcome**                                                                 | **Pass/Fail** |
| ----------------------------------------- | ---------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------- | ------------- |
| **Game Starts Successfully**              | The game initializes, prints the starting room description, and prompts for input. | ✅ TBD                                                                             | ✅            |
| **Check Inventory (Empty)**               | `inventory` or `inv` command shows an empty inventory.                             | ✅ (Should have a message saying no items)                                         | ✅            |
| **Pick Up an Item**                       | `take [item]` adds the item to inventory and removes it from the room.             | ✅ TBD                                                                             | ✅            |
| **Check Inventory (With Items)**          | `inventory` lists collected items.                                                 | ✅ TBD                                                                             | ✅            |
| **Move to Another Room**                  | `walk [exit name]` transitions to the specified room.                              | ✅ TBD                                                                             | ✅            |
| **Walk Into Locked Door**                 | `walk [locked exit]` prints a message that the door is locked.                     | ✅ TBD                                                                             | ✅            |
| **Use Key on Locked Door**                | `use key` unlocks the door, allowing movement.                                     | ✅ Prob should display a description of it being open when using look_around again | ✅            |
| **Walk Through Unlocked Door**            | `walk [exit name]` moves the player to the next room.                              | ✅ TBD                                                                             | ✅            |
| **Look Around the Room**                  | `look_around` prints all exits, static items, and descriptions.                    | ✅ TBD                                                                             | ✅            |
| **Interact With a Static Object (Chest)** | `open chest` prints the message and gives the player an item.                      | ✅ TBD                                                                             | ✅            |
| **Attack Static Object (Chest)**          | `attack chest` prints a failure message.                                           | ✅ TBD                                                                             | ✅            |
| **Use Wooden Sword on Dragon**            | `use wooden_sword` prints the death message and ends the game.                     | ✅ TBD                                                                             | ✅            |
| **Use Mighty Sword on Dragon**            | `use mighty_sword` prints the victory message and ends the game.                   | ✅ TBD                                                                             | ✅            |
| **Go Back to Previous Room**              | `go_back` moves the player back to the last room they were in.                     | ✅ TBD                                                                             | ✅            |
| **Enter Invalid Command**                 | Entering an unknown command prints a list of valid commands.                       | ✅ TBD                                                                             | ✅            |
| **Exit the Game**                         | `exit` quits the game.                                                             | ✅ TBD                                                                             | ✅            |

## Additional Notes

-   If a test fails, document the **bug or unexpected behavior** under **Issues Found** below.
-   Any additional edge cases should be noted and tested separately.

## Issues Found

-   When using an item and it asks you what you want to use it on, if you write "inv" etc you crash
-   Obviously, not using the exact correct names crashes
-   Attack doesn't work on dragon and maybe it should be an "what do you want to attack the dragon with?"
-   open only works on the chest nothing else could work on exists but not sure, it might become a future feature.
-   Winning the game does not quit the game or take you to a menu also needed to be implemented.
-   Prob should be able to just write, walk, open, take etc and ask "command what?"

# Additional Testing - Error Handling & Edge Cases

## Overview

This document outlines additional test cases focusing on **error handling, invalid inputs, and edge cases** for the **Slay the Dragon** text-based adventure.

## Test Cases

| **Test Case**                                                                            | **Expected Behavior**                                                          | **Actual Outcome**                               | **Pass/Fail** | **Fix Documentation**                                                                                                                                                                               |
| ---------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ | ------------------------------------------------ | ------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **1a. Input action and item with mixed casing (`TAKE sword`, `wAlK door`)**              | Commands should be case-insensitive (converted to lowercase)                   | Tells me that it doesn't understand the command. | ✅ (fixed)    | Added `.lower()` to `action[0]` before processing the command.                                                                                                                                      |
| **1b. Input only item with mixed casing (`take sWoRd`, `walk DoOr`)**                    | Commands should be case-insensitive (converted to lowercase)                   | Game Crashes                                     | ❌            | -                                                                                                                                                                                                   |
| **2a. Entering a command without arguments (`walk`, `use`)**                             | Should ask the player **"Walk where?"** or **"Use what?"** instead of crashing | Game Crashes                                     | ❌            | -                                                                                                                                                                                                   |
| **2b. Entering a command without arguments with mixed casing (`wAlK`, `uSe`)**           | Should give the same outcome as above **"Walk where?"** or **"Use what?"**     | Tells me that it doesn't understand the command. | ❌            | -                                                                                                                                                                                                   |
| **3a. Entering completely invalid command (`fly dragon`, `eat sword`)**                  | Should print **"I don't know how to [command]"**                               | Tells me that it doesn't understand the command. | ✅            | -                                                                                                                                                                                                   |
| **3b. Entering correct command but invalid item/exit (`take dragon`, `walk pony`)**      | Should print **"I don't know how to [command]"** instead of crashing           | ✅ Game Crashes                                  | ❌            | Checked if the exit/item exists in the current room. If not, prints a message telling the player it doesn't exist.                                                                                  |
| **4. Trying to use an item that is NOT in inventory (`use sword` before picking it up)** | Should print **"You don’t have that item!"** instead of crashing               | Game Crashes                                     | ✅ (fixed)    | Fixed by checking if the item exists in the player's inventory before proceeding. If the item is not found, the game now prints `"You don’t have '[item]' in your inventory!"` instead of crashing. |
| **5. Trying to take an item that doesn’t exist (`take banana`)**                         | Should print **"There is no banana here."** instead of crashing                | Game Crashes                                     | ✅ (fixed)    | Fixed by checking if the item exists before calling `take_item()`. If it doesn’t exist, the game now prints `"There is no '[item]' here."` instead of crashing.                                     |
| **6. Using `use` but entering an invalid target (`use key on chair`)**                   | Should print **"You can’t use that here."**                                    | Game Crashes                                     | ❌            | -                                                                                                                                                                                                   |
| **7. Entering `inventory` when inventory is empty**                                      | Should print **"You have nothing in your inventory."**                         | Prints out empty array, nothing.                 | ✅ (fixed)    | Fixed by checking if inventory is empty and printing a message instead of showing an empty list.                                                                                                    |
| **8. Trying to `open` something that isn't openable (`open dragon`)**                    | Should print **"You can't open that."** instead of crashing                    | Game Crashes                                     | ❌            | -                                                                                                                                                                                                   |
| **9. Trying to `attack` a non-attackable object (`attack door`)**                        | Should print **"You can’t attack that."**                                      | Game Crashes                                     | ❌            | -                                                                                                                                                                                                   |
| **10. Winning the game (`use mighty_sword on dragon`)**                                  | Should **quit the game or return to menu** instead of continuing               | Goes back to prompt "What to do?"                | ❌            | -                                                                                                                                                                                                   |

---

## Next Steps

1️⃣ **Test all cases** and document outcomes.  
2️⃣ **Fix any crashes or incorrect behavior** (write fixes under "Fix Documentation").  
3️⃣ **Retest after fixing** to confirm everything works properly.

---

🚀 **Once all tests pass, we’ll be golden!** Now go break things, babe! 💪😏

## Conclusion

All major functionalities should be tested before final submission. ✅
