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
const battleActions = document.getElementById('battle-actions');
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
const playerBattleHealthBar = document.getElementById('player-battle-health-bar');
const playerBattleHealthText = document.getElementById('player-battle-health-text');

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
        
        // If we're in battle mode, use battle actions
        if (gameState.event === 'battle' && battleActions.children.length > 0) {
            if (buttonIndex < battleActions.children.length) {
                battleActions.children[buttonIndex].click();
            }
            return;
        }
        
        // If we're in map mode and compass is visible
        if (gameState.event === 'map' && compassContainer.style.display !== 'none') {
            if (buttonIndex === 0) compassNorth.click();
            else if (buttonIndex === 1) compassEast.click();
            else if (buttonIndex === 2) compassSouth.click();
            else if (buttonIndex === 3) compassWest.click();
            return;
        }
        
        // Otherwise use regular action buttons
        const buttons = document.querySelectorAll('#action-buttons .action-button');
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
    if (data.event === 'battle') {
        // Show battle actions in battle container
        hideCompass();
        hideActionButtons();
        updateBattleActions();
    } else if (data.event === 'map' && data.options && 
        data.options.includes('Move North') && 
        data.options.includes('Move East') && 
        data.options.includes('Move South') && 
        data.options.includes('Move West')) {
        // Show compass for map navigation
        showCompass();
        hideActionButtons();
        hideBattleActions();
    } else {
        // Show regular action buttons for other events
        hideCompass();
        hideBattleActions();
        updateActionButtons();
    }
}

// Process message based on event type
function processMessage(message, event) {
    if (event === 'battle') {
        // In battle mode, add all messages to the battle log
        // and clear the current message area
        
        const lines = message.split('\n');
        
        // Add each line to the battle log
        lines.forEach(line => {
            if (line.trim()) {
                const p = document.createElement('p');
                p.textContent = line;
                battleLog.appendChild(p);
            }
        });
        
        // Keep only the last 2 messages in battle log
        while (battleLog.children.length > 2) {
            battleLog.removeChild(battleLog.firstChild);
        }
        
        // Scroll battle log to bottom to show latest messages
        battleLog.scrollTop = battleLog.scrollHeight;
        
        // Clear current message during battle
        clearCurrentMessage();
        
        // Add a status message to current message area
        const p = document.createElement('p');
        p.textContent = "Battle in progress... Check the battle log above for details.";
        currentMessage.appendChild(p);
    } else if (gameState.event === 'battle' && event !== 'battle') {
        // Battle just ended - show victory or defeat screen
        clearCurrentMessage();
        
        // Extract non-battle messages
        const lines = message.split('\n');
        const nonBattleLines = [];
        let defeatedMonster = "";
        let killedBy = "";
        let goldGained = 0;
        let playerDefeated = false;
        
        lines.forEach(line => {
            const lowerLine = line.toLowerCase();
            // Skip battle-related messages but keep victory/defeat messages
            if (!lowerLine.includes('attack') && 
                !lowerLine.includes('damage') && 
                !lowerLine.includes('stance')) {
                if (line.trim()) {
                    nonBattleLines.push(line);
                    
                    // Check for player defeat
                    if (lowerLine.includes('you died') || 
                        lowerLine.includes('you were killed') || 
                        lowerLine.includes('you have been defeated')) {
                        playerDefeated = true;
                        
                        // Try to extract what killed the player
                        const killedByMatch = line.match(/by (?:the |a |an )?([^!.]+)/i);
                        if (killedByMatch && killedByMatch[1]) {
                            killedBy = killedByMatch[1].trim();
                        }
                    }
                    
                    // Check for victory
                    if (lowerLine.includes('defeated') || lowerLine.includes('victory')) {
                        const monsterMatch = line.match(/defeated the ([^!.]+)/i);
                        if (monsterMatch && monsterMatch[1]) {
                            defeatedMonster = monsterMatch[1].trim();
                        }
                    }
                    
                    // Check for gold gained
                    if (lowerLine.includes('gold')) {
                        const goldMatch = line.match(/(\d+) gold/i);
                        if (goldMatch && goldMatch[1]) {
                            goldGained = parseInt(goldMatch[1]);
                        }
                    }
                }
            }
        });
        
        // Show appropriate screen based on battle outcome
        if (playerDefeated) {
            showDefeatedScreen(`You were killed by ${killedBy || "your enemy"}`, killedBy);
        } else if (nonBattleLines.length > 0 && defeatedMonster) {
            showSuccessScreen(`Victory!`, `You defeated ${defeatedMonster}`, goldGained);
        } else {
            // Fallback to regular message display if we couldn't parse the details
            nonBattleLines.forEach(line => {
                const p = document.createElement('p');
                p.textContent = line;
                currentMessage.appendChild(p);
            });
        }
    } else {
        // For non-battle events, just add to current message
        clearCurrentMessage();
        addCurrentMessage(message);
    }
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
    
    // Update battle health display if in battle
    if (playerBattleHealthBar && playerBattleHealthText) {
        playerBattleHealthBar.style.width = `${healthPercentage}%`;
        playerBattleHealthText.textContent = `${player.health}/${player.max_health} HP`;
        
        // Apply same color logic to battle health bar
        if (healthPercentage <= 25) {
            playerBattleHealthBar.style.backgroundColor = '#c04040';
        } else if (healthPercentage <= 50) {
            playerBattleHealthBar.style.backgroundColor = '#c0a040';
        } else {
            playerBattleHealthBar.style.backgroundColor = '#60a060';
        }
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
    
    // Remove any special screen classes if present
    currentMessage.classList.remove('success-screen', 'defeated-screen');
}

// Show success screen with embellishments
function showSuccessScreen(title, message, goldAmount = 0) {
    clearCurrentMessage();
    
    // Add success screen class to the message container
    currentMessage.classList.add('success-screen');
    
    // Create title with stars
    const titleElement = document.createElement('div');
    titleElement.classList.add('success-title');
    titleElement.innerHTML = `★ ${title} ★`;
    currentMessage.appendChild(titleElement);
    
    // Create message
    const messageElement = document.createElement('div');
    messageElement.classList.add('success-message');
    messageElement.textContent = message;
    currentMessage.appendChild(messageElement);
    
    // Create gold reward display if gold was gained
    if (goldAmount > 0) {
        const goldElement = document.createElement('div');
        goldElement.classList.add('success-reward');
        goldElement.innerHTML = `<span class="gold-icon">⭐</span> ${goldAmount} gold gained!`;
        currentMessage.appendChild(goldElement);
    }
    
    // Add decorative border
    const borderElement = document.createElement('div');
    borderElement.classList.add('success-border');
    borderElement.innerHTML = '✧ ✦ ✧ ✦ ✧ ✦ ✧ ✦ ✧ ✦ ✧ ✦ ✧';
    currentMessage.appendChild(borderElement);
    
    // Scroll to bottom
    currentMessage.scrollTop = currentMessage.scrollHeight;
}

// Show defeated screen with embellishments
function showDefeatedScreen(message, killedBy) {
    clearCurrentMessage();
    
    // Add defeated screen class to the message container
    currentMessage.classList.add('defeated-screen');
    
    // Create title with skull symbols
    const titleElement = document.createElement('div');
    titleElement.classList.add('defeated-title');
    titleElement.innerHTML = `☠ Defeated ☠`;
    currentMessage.appendChild(titleElement);
    
    // Create message
    const messageElement = document.createElement('div');
    messageElement.classList.add('defeated-message');
    messageElement.textContent = message || `You were killed by ${killedBy}`;
    currentMessage.appendChild(messageElement);
    
    // Add decorative border
    const borderElement = document.createElement('div');
    borderElement.classList.add('defeated-border');
    borderElement.innerHTML = '✧ ✦ ✧ ✦ ✧ ✦ ✧ ✦ ✧ ✦ ✧ ✦ ✧';
    currentMessage.appendChild(borderElement);
    
    // Scroll to bottom
    currentMessage.scrollTop = currentMessage.scrollHeight;
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
    
    // Only clear battle log and add initial message if this is a new battle
    // Check if battle log is empty or only has the initial "begins" message
    if (battleLog.children.length === 0) {
        // Clear any existing content first
        while (battleLog.firstChild) {
            battleLog.removeChild(battleLog.firstChild);
        }
        
        // Add initial battle message for new battles
        const p = document.createElement('p');
        p.textContent = `⚔️ Battle with ${enemy.name} begins!`;
        battleLog.appendChild(p);
    }
}

// Hide battle information
function hideBattleInfo() {
    battleContainer.style.display = 'none';
    
    // Clear battle log when battle ends
    while (battleLog.firstChild) {
        battleLog.removeChild(battleLog.firstChild);
    }
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

// Update battle actions in battle container
function updateBattleActions() {
    // Clear existing battle actions
    hideBattleActions();
    
    // Add battle action buttons
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
        
        battleActions.appendChild(button);
    });
}

// Hide battle actions
function hideBattleActions() {
    while (battleActions.firstChild) {
        battleActions.removeChild(battleActions.firstChild);
    }
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
