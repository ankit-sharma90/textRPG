# Key features V1
- battle enemies
- collect loot
- world map
- actions
- day & night cycle (every 3 actions)

# Key features (full release)
- battle enemies
- collect loot
- build your character
    - equipment can grant special skills
- create account & save progress
- exciting encoutners
    - randomization means interesting enemies, special quests, and NPCs can popup
- death is not permanent
    - roguelite mechanics
- dynamic enemy system
  - nemesis system (enemies that kill you are marked as nemeses, get stronger, and give better rewards)
  - high level enemies can run away from you & target your weaknesses
  - clever enemies can steal items from you
- mystery
    - world map is hidden by default, you can unlock portions of it via quests & beating certain enemies
    - multiple worlds or realms, and each has a diff visual treament for the UI

## Technical requirements V1
- It must be very fast
- Users must be able to play in the browser
- Sessions do not timeout, so the game can be played asyncronously

## User journey: first event V1
- NPC greets player and gives them 10 gold, a stick (weapon)
- Stick does 1 damage
- Player can take 3 actions
    - Reject offering and move on
    - Take the goods and move on
    - Take the goods and fight the NPC

## User journey: first battle V1
- If fights NPC, this is the first battle
- Otherwise, the first action screen after the player moves on is a battle with a Goblin

## User journey: first death V1
- Player dies when health reaches zero
- Player has two options
    1. Lose everything (items, character level, gold) and start new
    2. Resurrect as a vampire with everything before they died, but now take 5% health damage per day during daytime

## Feature requirements V1
**Actions** 
- User must take one of 3 actions on each screen
  1. Interact with event/object
  2. Movement on world map
- Scenarios:
    1. NPC - character with dialogue that has a quest for the player
    2. Merchant - character that will buy and sell items from the player in return for gold
    3. Enemy - enemy that will battle the player

**World maps**
- Start on Earth world map
- Map is not visible to user, only through special & temporary mechanics
- Worlds are as follows
    1. Earth (modern day)
    2. Heavenly mountains
    3. Stone caverns
    4. Future city
    5. Prehistoric jungle
    6. Atlantis

**Battles**
- Battles are like Pokemon: player vs. enemy until one reaches zero health
- Player goes first
- Player & Enemy can play one skill on their turn
- Attacks reduce enemy HP, while defensive skills heal player or reduce attack damage
- Enemies reward the player with loot (see loot table)

**Enemies**
- Goblin: 3 hp, 1 attack points, has only one attack (hit, which does 1 damage)

**Loot table**
- Gold (90%)
- Equipment (10%)

## User journey: signup V2
* Play as guest
* Create account to save progress
* Enter email
* Get confirmation
* Create password
* Start playing
