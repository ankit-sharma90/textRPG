# Text RPG Game

A dark fantasy text-based RPG game with battles, loot collection, and a day/night cycle.

## Features (V1)

- Battle enemies
- Collect loot
- World map
- Actions
- Day & night cycle (every 3 actions)
- Web-based UI with keyboard shortcuts
- Dark fantasy theme

## UI Improvements

- Separate game log and battle log with different UI sections
- Visual distinction between game events and current actions
- Keyboard shortcuts displayed directly on action buttons
- Dark fantasy theme with appropriate color scheme
- Responsive design for different screen sizes

## How to Run

### Web Version (Recommended)

1. Make sure you have Python 3 installed
2. Create a virtual environment and install the required dependencies:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Run the web server:

```bash
python app.py
```

4. Open your browser and navigate to:

```
http://localhost:5000
```

### Terminal Version (Legacy)

1. Make sure you have Python 3 installed
2. Navigate to the game directory
3. Run the game with:

```bash
python main.py
```

## Gameplay

- You start with a first encounter with an NPC who offers you gold and a weapon
- You can choose to accept or reject the offering, or even fight the NPC
- After the first encounter, you can explore the world map
- You'll encounter enemies to battle
- Collect loot and gold from defeated enemies
- The game has a day/night cycle that changes every 3 actions
- If you die, you can choose to start over or become a vampire (with a daytime penalty)

## Game Controls

### Web Version
- Click on action buttons to make choices
- Use number keys (1-9) as keyboard shortcuts for actions (displayed on buttons)
- The UI theme adjusts based on the time of day (day/night)
- Game log shows important events
- Battle log shows combat results
- Current action shows immediate feedback

### Terminal Version
The game is controlled through text input. When prompted, enter the number corresponding to your choice.

## Technical Requirements

- Fast execution
- Browser playable
- Persistent sessions
- Dark fantasy theme