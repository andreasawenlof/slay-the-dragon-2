Slay the Dragon - A Text-Based RPG

Overview

Slay the Dragon is a text-based role-playing game where players navigate through multiple rooms, collecting items and solving challenges to ultimately defeat a mighty dragon. The game structure is inspired by classic adventure games, particularly The Legend of Zelda on the NES, incorporating elements like locked doors requiring keys, strategic item collection, and an epic boss battle.

UX

The Idea

The game revolves around exploration and puzzle-solving within a dungeon-like environment. Players must carefully choose their actions, gather necessary items, and strategically plan their approach to reach the final challenge: slaying the dragon.

The inspiration comes from classic adventure games, incorporating logical problem-solving with simple but engaging mechanics. The challenge lies in finding the correct path, gathering useful tools, and making the right choices at critical moments.

Structure

The game consists of interconnected rooms, each with unique descriptions, interactive objects, and potential obstacles. Players must:

Navigate through different rooms using directional movement commands.

Collect items like swords and keys to unlock doors and prepare for the final encounter.

Interact with the environment by examining objects, opening chests, and making strategic decisions.

Battle the dragon using acquired weapons, where using the wrong weapon results in failure.

Features

Existing Features

Room Exploration - Players can move between rooms, discovering new areas and obstacles.

Item Collection & Inventory Management - Items like swords and keys are required for progression.

Puzzle Solving - Certain doors are locked and require specific keys or actions to open.

Combat System - A simple battle mechanic where using the correct weapon is necessary to win.

Future Features

Expanded Room System - Adding more rooms with unique challenges and hidden items.

More Complex Enemy Interactions - Introducing additional creatures with different strengths and weaknesses.

Multiple Endings - Varying outcomes based on player choices and item usage.

Technologies Used

Python - Core programming language used for the game's logic.

JSON - Used for storing game data, including rooms, items, and interactions.

Prompt Toolkit - Enhances the command-line interface for a better player experience.

Testing

Manual Testing - The game was tested by:

Navigating through all available rooms.

Collecting and using items.

Attempting invalid commands to check error handling.

Ensuring the win/loss conditions trigger correctly.

Validator Testing

Code was checked using PEP8 to ensure compliance with Python best practices.

Bugs & Fixes

Solved Bugs

Index Errors - Fixed an issue where room navigation caused crashes due to missing keys.

Incorrect Item Handling - Ensured that item use correctly affects the game state.

Combat Logic Issues - Addressed a problem where using the incorrect weapon against the dragon did not trigger a failure message properly.

Remaining Bugs

No known remaining issues.

Deployment

This project was deployed using Code Institute's mock terminal on Heroku.

Steps for Deployment

Fork or clone this repository.

Create a new Heroku app.

Set the buildpacks to:

heroku/python

heroku/nodejs

Create a Config Var called PORT and set it to 8000.

Connect the GitHub repository to Heroku.

Deploy the application.

Credits

Game Concept & Development: [Your Name]

Code Institute: For the deployment template and educational resources.

Zelda NES: Inspiration for the dungeon-like gameplay mechanics.

Acknowledgments

Special thanks to Code Institute for providing the framework for this project and to all playtesters for their valuable feedback!
