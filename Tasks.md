Initial setup
- [x] create the initial setup for this game specified in requirements.md as V1

Implement basic UI
- [x] game should not run in the terminal, but instead render output & take inputs via browser
- [x] each action should have a button
- [x] user can click or use keyboard shortcut to invoke each action
- [x] theme the page after the current "world"

UI improvements
- [x] separate the game log from the battle log with a diffrent UI
    - example: You defeated the Goblin should have a separate UI box from "You moved on the world map"
- [x] separate the game log from the current message with some UI treatment
    - example: You defeated the Goblin should be visually separate from the current action "You attack the Goblin for 1 damage"
- [x] show action shortcuts in the UI itself
- [x] theme colors overall should not be very bright, this is a dark fantasy RPG

Battle UI improvements
- [x] show a health bar for the player in addition to the enemy
- [x] player actions should not be in their own separate section, they should be combined with the latest action in the general "current UI" section
- [x] dont give titles to each section, this clutters the UI
- [x] replace "Quit game" with "Flee" option during battles
- [x] remove the battle log container that shows "Battle with Goblin has begun!"
- [x] remove the game log box to simplify the UI
- [x] add a dedicated battle log between enemy health bar and player actions for battle-specific messages
- [x] ensure battle messages like "You attack the Goblin for 1 damage!" only appear in the battle log
- [x] limit battle log to only show the latest 2 messages

Navigation improvements
- [x] replace "Move on the map" with directional movement options (North, East, South, West)
- [x] remove "Check inventory" and "Quit game" options from the main UI for V1
- [x] implement compass-style directional controls (North at top, East at right, etc.)
- [x] display all actions vertically for better readability