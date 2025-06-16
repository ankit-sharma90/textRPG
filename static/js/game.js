// Game state
let gameState = {
    event: null,
    enemy: null,
    options: []
};

// DOM elements
const messageBox = document.getElementById('message-box');
const actionButtons = document.getElementById('action-buttons');
const startButton = document.getElementById('start-button');
const healthDisplay = document.getElementById('health');
const goldDisplay = document.getElementById('gold');
const timeDisplay = document.getElementById('time');
const vampireStatus = document.getElementById('vampire-status');
const enemyInfo = document.getElementById('enemy-info');
const enemyName = document.getElementById('enemy-name');
const enemyHealthBar = document.getElementById('enemy-health-bar');
const enemyHealthText = document.getElementById('enemy-health-text');

// Initialize the game
document.addEventListener('DOMContentLoaded', () => {
    startButton.addEventListener('click', startGame);
    
    // Add keyboard shortcuts
    document.addEventListener('keydown', handleKeyPress);
});

// Handle keyboard shortcuts
function handleKeyPress(event) {
    // Number keys 1-9
    if (event.key >= '1' && event.key <= '9') {
        const buttonIndex = parseInt(event.key) - 1;
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
        addMessage('Error starting game. Please try again.');
    });
}

// Update the game state based on server response
function updateGameState(data) {
    // Update player status
    updatePlayerStatus(data.player);
    
    // Update time
    updateTime(data.time);
    
    // Update message
    if (data.message) {
        addMessage(data.message);
    }
    
    // Update game state
    gameState.event = data.event;
    gameState.options = data.options || [];
    
    // Handle enemy if in battle
    if (data.event === 'battle' && data.enemy) {
        gameState.enemy = data.enemy;
        showEnemyInfo(data.enemy);
    } else {
        hideEnemyInfo();
    }
    
    // Update action buttons
    updateActionButtons();
}

// Update the player status display
function updatePlayerStatus(player) {
    healthDisplay.textContent = `${player.health}/${player.max_health}`;
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
    if (time === 'Night') {
        body.classList.remove('earth-theme');
        body.classList.add('night-theme');
    } else {
        body.classList.remove('night-theme');
        body.classList.add('earth-theme');
    }
}

// Add a message to the message box
function addMessage(message) {
    const paragraphs = message.split('\n');
    
    // Clear message box if it's getting too long
    if (messageBox.children.length > 10) {
        messageBox.innerHTML = '';
    }
    
    paragraphs.forEach(paragraph => {
        if (paragraph.trim()) {
            const p = document.createElement('p');
            p.textContent = paragraph;
            messageBox.appendChild(p);
        }
    });
    
    // Scroll to bottom
    messageBox.scrollTop = messageBox.scrollHeight;
}

// Show enemy information
function showEnemyInfo(enemy) {
    enemyInfo.style.display = 'block';
    enemyName.textContent = enemy.name;
    enemyHealthBar.style.width = `${(enemy.health / 5) * 100}%`;
    enemyHealthText.textContent = `${enemy.health} HP`;
}

// Hide enemy information
function hideEnemyInfo() {
    enemyInfo.style.display = 'none';
}

// Update action buttons based on current options
function updateActionButtons() {
    // Clear existing buttons except start button
    while (actionButtons.firstChild) {
        actionButtons.removeChild(actionButtons.firstChild);
    }
    
    // Add new buttons for each option
    gameState.options.forEach((option, index) => {
        const button = document.createElement('button');
        button.classList.add('action-button');
        button.textContent = option;
        
        // Add keyboard shortcut hint
        button.title = `Press ${index + 1} to select`;
        
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
        addMessage('Error processing action. Please try again.');
    });
}