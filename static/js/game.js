// Game state
let gameState = {
    event: null,
    enemy: null,
    options: []
};

// DOM elements
const currentMessage = document.getElementById('current-message');
const battleContainer = document.getElementById('battle-container');
const battleLog = document.getElementById('battle-log');
const actionButtons = document.getElementById('action-buttons');
const compassContainer = document.getElementById('compass-container');
const startButton = document.getElementById('start-button');
const healthDisplay = document.getElementById('health');
const playerHealthBar = document.getElementById('player-health-bar');
const goldDisplay = document.getElementById('gold');
const timeDisplay = document.getElementById('time');
const vampireStatus = document.getElementById('vampire-status');
const enemyInfo = document.getElementById('enemy-info');
const enemyName = document.getElementById('enemy-name');
const enemyHealthBar = document.getElementById('enemy-health-bar');
const enemyHealthText = document.getElementById('enemy-health-text');

// Compass buttons
const compassNorth = document.getElementById('compass-north');
const compassEast = document.getElementById('compass-east');
const compassSouth = document.getElementById('compass-south');
const compassWest = document.getElementById('compass-west');

// Initialize the game
document.addEventListener('DOMContentLoaded', () => {
    startButton.addEventListener('click', startGame);
    
    // Add compass button event listeners
    compassNorth.addEventListener('click', () => takeAction(1));
    compassEast.addEventListener('click', () => takeAction(2));
    compassSouth.addEventListener('click', () => takeAction(3));
    compassWest.addEventListener('click', () => takeAction(4));
    
    // Add keyboard shortcuts
    document.addEventListener('keydown', handleKeyPress);
});

// Handle keyboard shortcuts
function handleKeyPress(event) {
    // Number keys 1-9
    if (event.key >= '1' && event.key <= '9') {
        const buttonIndex = parseInt(event.key) - 1;
        
        // If we're in map mode and compass is visible
        if (gameState.event === 'map' && compassContainer.style.display !== 'none') {
            if (buttonIndex === 0) compassNorth.click();
            else if (buttonIndex === 1) compassEast.click();
            else if (buttonIndex === 2) compassSouth.click();
            else if (buttonIndex === 3) compassWest.click();
            return;
        }
        
        // Otherwise use regular action buttons
        const buttons = document.querySelectorAll('.action-button');
        if (buttonIndex < buttons.length) {
            buttons[buttonIndex].click();
        }
    }
}

// Start a new game
function startGame() {
    fetch('/api/start_game', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        updateGameState(data);
    })
    .catch(error => {
        console.error('Error:', error);
        addCurrentMessage('Error starting game. Please try again.');
    });
}

// Update the game state based on server response
function updateGameState(data) {
    // Update player status
    updatePlayerStatus(data.player);
    
    // Update time
    updateTime(data.time);
    
    // Update message based on event type
    if (data.message) {
        processMessage(data.message, data.event);
    }
    
    // Update game state
    gameState.event = data.event;
    gameState.options = data.options || [];
    
    // Handle enemy if in battle
    if (data.event === 'battle' && data.enemy) {
        gameState.enemy = data.enemy;
        showBattleInfo(data.enemy);
    } else {
        hideBattleInfo();
    }
    
    // Update action buttons or compass based on event
    if (data.event === 'map' && data.options && 
        data.options.includes('Move North') && 
        data.options.includes('Move East') && 
        data.options.includes('Move South') && 
        data.options.includes('Move West')) {
        // Show compass for map navigation
        showCompass();
        hideActionButtons();
    } else {
        // Show regular action buttons for other events
        hideCompass();
        updateActionButtons();
    }
}

// Process message based on event type
function processMessage(message, event) {
    const lines = message.split('\n');
    
    // Clear current message
    clearCurrentMessage();
    
    if (event === 'battle') {
        // In battle mode, we want to show all battle-related messages in the battle log
        // and only show non-battle messages in the current message area
        
        // For battle events, we'll put battle messages in the battle log
        // and only non-battle messages in the current message area
        let nonBattleMessages = [];
        let battleMessages = [];
        
        lines.forEach(line => {
            if (line.trim()) {
                // Check if this is a battle message
                if (isBattleMessage(line)) {
                    battleMessages.push(line);
                } else {
                    nonBattleMessages.push(line);
                }
            }
        });
        
        // Add battle messages to battle log
        if (battleMessages.length > 0) {
            // Add each battle message as a new paragraph
            battleMessages.forEach(line => {
                const p = document.createElement('p');
                p.textContent = line;
                battleLog.appendChild(p);
            });
            
            // Limit battle log size
            while (battleLog.children.length > 10) {
                battleLog.removeChild(battleLog.firstChild);
            }
            
            // Scroll battle log to bottom
            battleLog.scrollTop = battleLog.scrollHeight;
        }
        
        // Add non-battle messages to current message
        if (nonBattleMessages.length > 0) {
            addCurrentMessage(nonBattleMessages.join('\n'));
        } else {
            // If no non-battle messages, add a generic message
            addCurrentMessage("Battle in progress...");
        }
    } else {
        // For non-battle events, just add to current message
        addCurrentMessage(message);
    }
}

// Helper function to determine if a message is battle-related
function isBattleMessage(message) {
    const battleKeywords = [
        'attack', 'damage', 'defeated', 'flee', 'stance', 'defensive',
        'goblin', 'enemy', 'health', 'hp', 'battle', 'old man',
        'for 1 damage', 'attacks you'
    ];
    
    message = message.toLowerCase();
    return battleKeywords.some(keyword => message.includes(keyword));
}

// Update the player status display
function updatePlayerStatus(player) {
    // Update health text
    healthDisplay.textContent = `${player.health}/${player.max_health}`;
    
    // Update health bar
    const healthPercentage = (player.health / player.max_health) * 100;
    playerHealthBar.style.width = `${healthPercentage}%`;
    
    // Change color based on health percentage
    if (healthPercentage <= 25) {
        playerHealthBar.style.backgroundColor = '#c04040'; // Red for low health
    } else if (healthPercentage <= 50) {
        playerHealthBar.style.backgroundColor = '#c0a040'; // Yellow for medium health
    } else {
        playerHealthBar.style.backgroundColor = '#60a060'; // Green for good health
    }
    
    // Update gold
    goldDisplay.textContent = player.gold;
    
    // Show vampire status if applicable
    if (player.is_vampire) {
        vampireStatus.style.display = 'block';
    } else {
        vampireStatus.style.display = 'none';
    }
}

// Update the time display and theme
function updateTime(time) {
    timeDisplay.textContent = time;
    
    // Update theme based on time
    const body = document.body;
    body.classList.remove('day', 'night');
    
    if (time === 'Night') {
        body.classList.add('night');
    } else {
        body.classList.add('day');
    }
}

// Add a message to the current message box
function addCurrentMessage(message) {
    if (!message.trim()) return;
    
    clearCurrentMessage();
    
    const lines = message.split('\n');
    lines.forEach(line => {
        if (line.trim()) {
            const p = document.createElement('p');
            p.textContent = line;
            currentMessage.appendChild(p);
        }
    });
    
    // Scroll to bottom
    currentMessage.scrollTop = currentMessage.scrollHeight;
}

// Clear the current message box
function clearCurrentMessage() {
    while (currentMessage.firstChild) {
        currentMessage.removeChild(currentMessage.firstChild);
    }
}

// Show battle information
function showBattleInfo(enemy) {
    battleContainer.style.display = 'block';
    enemyName.textContent = enemy.name;
    
    // Update enemy health bar
    const maxEnemyHealth = enemy.name === 'Goblin' ? 3 : 5; // Approximate max health
    const healthPercentage = (enemy.health / maxEnemyHealth) * 100;
    enemyHealthBar.style.width = `${healthPercentage}%`;
    
    enemyHealthText.textContent = `${enemy.health} HP`;
    
    // Add initial battle message
    const p = document.createElement('p');
    p.textContent = `Battle with ${enemy.name} begins!`;
    battleLog.appendChild(p);
}

// Hide battle information
function hideBattleInfo() {
    battleContainer.style.display = 'none';
}

// Show compass navigation
function showCompass() {
    compassContainer.style.display = 'block';
}

// Hide compass navigation
function hideCompass() {
    compassContainer.style.display = 'none';
}

// Hide action buttons
function hideActionButtons() {
    while (actionButtons.firstChild) {
        actionButtons.removeChild(actionButtons.firstChild);
    }
}

// Update action buttons based on current options
function updateActionButtons() {
    // Clear existing buttons
    hideActionButtons();
    
    // Add new buttons for each option
    gameState.options.forEach((option, index) => {
        const button = document.createElement('button');
        button.classList.add('action-button');
        
        // Create key span
        const keySpan = document.createElement('span');
        keySpan.classList.add('action-key');
        keySpan.textContent = index + 1;
        
        // Create text span
        const textSpan = document.createElement('span');
        textSpan.classList.add('action-text');
        textSpan.textContent = option;
        
        // Add spans to button
        button.appendChild(keySpan);
        button.appendChild(textSpan);
        
        button.addEventListener('click', () => {
            takeAction(index + 1);
        });
        
        actionButtons.appendChild(button);
    });
}

// Take an action
function takeAction(choice) {
    const requestData = {
        event: gameState.event,
        choice: choice
    };
    
    // Add enemy info if in battle
    if (gameState.event === 'battle' && gameState.enemy) {
        requestData.enemy_name = gameState.enemy.name;
        requestData.enemy_health = gameState.enemy.health;
    }
    
    fetch('/api/action', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestData)
    })
    .then(response => response.json())
    .then(data => {
        updateGameState(data);
    })
    .catch(error => {
        console.error('Error:', error);
        addCurrentMessage('Error processing action. Please try again.');
    });
}