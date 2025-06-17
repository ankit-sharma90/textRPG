#!/usr/bin/env python3
"""
Web application for Text RPG Game
"""
from flask import Flask, render_template, request, jsonify, session
from flask_socketio import SocketIO
import json
import uuid
from game.game_manager import GameManager
from game.items import STICK

app = Flask(__name__)
app.secret_key = 'text_rpg_secret_key'
socketio = SocketIO(app)

# Store active games
games = {}

@app.route('/')
def index():
    """Render the main game page"""
    # Create a unique session ID if not exists
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    
    # Create a new game for this session if not exists
    if session['session_id'] not in games:
        games[session['session_id']] = GameManager()
    
    return render_template('index.html')

@app.route('/api/start_game', methods=['POST'])
def start_game():
    """Start a new game"""
    session_id = session['session_id']
    game = games[session_id]
    
    # Reset game if needed
    games[session_id] = GameManager()
    game = games[session_id]
    
    # Return initial game state
    return jsonify({
        'message': 'Welcome to Text RPG!',
        'player': {
            'health': game.player.health,
            'max_health': game.player.max_health,
            'gold': game.player.gold,
            'is_vampire': game.player.is_vampire
        },
        'time': game.time_system.get_time_of_day(),
        'event': 'first_encounter',
        'options': [
            'Reject the offering and move on',
            'Take the goods and move on',
            'Take the goods and fight the NPC'
        ]
    })

@app.route('/api/action', methods=['POST'])
def take_action():
    """Process a player action"""
    data = request.json
    action = data.get('action')
    event = data.get('event')
    choice = data.get('choice')
    
    session_id = session['session_id']
    game = games[session_id]
    
    response = {}
    
    # Handle first encounter
    if event == 'first_encounter':
        if choice == 1:  # Reject
            response = {
                'message': 'You reject the offering and move on. The old man looks disappointed as you walk away.',
                'event': 'map',
                'options': ['Move North', 'Move East', 'Move South', 'Move West']
            }
        elif choice == 2:  # Take and move on
            game.player.add_gold(10)
            game.player.add_item(STICK)
            game.player.equip_weapon(STICK)
            response = {
                'message': 'You accept the offering and thank the old man. The old man smiles and wishes you good luck on your journey.',
                'event': 'map',
                'options': ['Move North', 'Move East', 'Move South', 'Move West']
            }
        elif choice == 3:  # Take and fight
            game.player.add_gold(10)
            game.player.add_item(STICK)
            game.player.equip_weapon(STICK)
            response = {
                'message': 'You take the offering and then attack the old man!',
                'event': 'battle',
                'enemy': {
                    'name': 'Old Man',
                    'health': 5
                },
                'options': ['Attack', 'Defend', 'Flee']
            }
    
    # Handle map actions
    elif event == 'map':
        # All directional movements (1-4) are handled the same way
        if choice >= 1 and choice <= 4:
            directions = ['North', 'East', 'South', 'West']
            direction = directions[choice - 1]
            
            game.action_taken()
            # 70% chance of battle
            import random
            if random.random() < 0.7:
                response = {
                    'message': f'You move {direction} and encounter a Goblin!',
                    'event': 'battle',
                    'enemy': {
                        'name': 'Goblin',
                        'health': 3
                    },
                    'options': ['Attack', 'Defend', 'Flee']
                }
            else:
                response = {
                    'message': f'You move {direction} but find nothing of interest.',
                    'event': 'map',
                    'options': ['Move North', 'Move East', 'Move South', 'Move West']
                }
    
    # Handle battle actions
    elif event == 'battle':
        enemy_name = data.get('enemy_name')
        enemy_health = data.get('enemy_health')
        
        if choice == 1:  # Attack
            damage = game.player.get_attack_damage()
            enemy_health -= damage
            
            message = f"You attack the {enemy_name} for {damage} damage!"
            
            if enemy_health <= 0:
                # Enemy defeated
                import random
                gold_reward = random.randint(1, 5)
                game.player.add_gold(gold_reward)
                
                response = {
                    'message': f"{message}\nYou defeated the {enemy_name}!\nYou found {gold_reward} gold!",
                    'event': 'map',
                    'options': ['Move North', 'Move East', 'Move South', 'Move West']
                }
            else:
                # Enemy attacks back
                enemy_damage = 1
                game.player.take_damage(enemy_damage)
                
                if game.player.health <= 0:
                    # Player died
                    response = {
                        'message': f"{message}\nThe {enemy_name} attacks you for {enemy_damage} damage!\nYou have been defeated!",
                        'event': 'death',
                        'options': [
                            'Lose everything and start new',
                            'Resurrect as a vampire (keep items but take 5% damage during day)'
                        ]
                    }
                else:
                    response = {
                        'message': f"{message}\nThe {enemy_name} attacks you for {enemy_damage} damage!",
                        'event': 'battle',
                        'enemy': {
                            'name': enemy_name,
                            'health': enemy_health
                        },
                        'options': ['Attack', 'Defend', 'Flee']
                    }
        
        elif choice == 2:  # Defend
            enemy_damage = 0
            message = "You take a defensive stance.\nThe enemy's attack does no damage!"
            
            response = {
                'message': message,
                'event': 'battle',
                'enemy': {
                    'name': enemy_name,
                    'health': enemy_health
                },
                'options': ['Attack', 'Defend', 'Flee']
            }
        
        elif choice == 3:  # Flee
            # 50% chance to successfully flee
            import random
            if random.random() < 0.5:
                response = {
                    'message': f"You successfully flee from the {enemy_name}!",
                    'event': 'map',
                    'options': ['Move North', 'Move East', 'Move South', 'Move West']
                }
            else:
                # Failed to flee, enemy attacks
                enemy_damage = 1
                game.player.take_damage(enemy_damage)
                
                if game.player.health <= 0:
                    # Player died
                    response = {
                        'message': f"You failed to flee!\nThe {enemy_name} attacks you for {enemy_damage} damage!\nYou have been defeated!",
                        'event': 'death',
                        'options': [
                            'Lose everything and start new',
                            'Resurrect as a vampire (keep items but take 5% damage during day)'
                        ]
                    }
                else:
                    response = {
                        'message': f"You failed to flee!\nThe {enemy_name} attacks you for {enemy_damage} damage!",
                        'event': 'battle',
                        'enemy': {
                            'name': enemy_name,
                            'health': enemy_health
                        },
                        'options': ['Attack', 'Defend', 'Flee']
                    }
    
    # Handle death
    elif event == 'death':
        if choice == 1:  # Lose everything
            game.player = GameManager().player
            response = {
                'message': "You've been reborn. All progress lost.",
                'event': 'map',
                'options': ['Move North', 'Move East', 'Move South', 'Move West']
            }
        elif choice == 2:  # Vampire
            game.player.resurrect_as_vampire()
            response = {
                'message': "You've been resurrected as a vampire! You'll take damage during daytime.",
                'event': 'map',
                'options': ['Move North', 'Move East', 'Move South', 'Move West']
            }
    
    # Add player status to all responses
    response['player'] = {
        'health': game.player.health,
        'max_health': game.player.max_health,
        'gold': game.player.gold,
        'is_vampire': game.player.is_vampire
    }
    response['time'] = game.time_system.get_time_of_day()
    
    return jsonify(response)

if __name__ == '__main__':
    socketio.run(app, debug=True)