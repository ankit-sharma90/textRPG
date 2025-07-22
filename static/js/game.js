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

// Map elements
const mapContainer = document.getElementById('map-container');
const mapViewport = document.getElementById('map-viewport');
const worldNameDisplay = document.getElementById('world-name');
const coordinatesDisplay = document.getElementById('coordinates');

// Map elements

// Animation speed toggle elements
const animationSpeedToggle = document.getElementById('animation-speed-toggle');
const speedIndicator = document.getElementById('speed-indicator');

// Compass buttons
const compassNorth = document.getElementById('compass-north');
const compassEast = document.getElementById('compass-east');
const compassSouth = document.getElementById('compass-south');
const compassWest = document.getElementById('compass-west');

// Animation speed settings
let currentAnimationSpeed = 1; // Default to Fast (index 1)
const ANIMATION_SPEEDS = [
    { name: '🚀 Super Fast', damageTime: '0.8s', iconTime: '0.5s' },
    { name: '⚡ Fast', damageTime: '1.2s', iconTime: '0.8s' },
    { name: '🎯 Normal', damageTime: '1.8s', iconTime: '1.2s' },
    { name: '🐌 Slow', damageTime: '2.5s', iconTime: '1.8s' },
    { name: '🐢 Extra Slow', damageTime: '3.2s', iconTime: '2.2s' }
];

// Icon variations for different action types
const ICON_VARIATIONS = {
    attack: ['💢'],  // Impact symbol - clear and universal
    defend: ['🛡', '🚧', '⛨'],  // Shield, barrier, guard
    heal: ['💚', '💖', '✨']     // Heart, sparkle heart, stars
};

// Initialize the game
document.addEventListener('DOMContentLoaded', () => {
    startButton.addEventListener('click', startGame);
    
    // Add compass button event listeners
    compassNorth.addEventListener('click', () => takeAction(1));
    compassEast.addEventListener('click', () => takeAction(2));
    compassSouth.addEventListener('click', () => takeAction(3));
    compassWest.addEventListener('click', () => takeAction(4));
    
    // Add animation speed toggle listener
    if (animationSpeedToggle) {
        animationSpeedToggle.addEventListener('click', toggleAnimationSpeed);
    }
    
    // Add keyboard shortcuts
    document.addEventListener('keydown', handleKeyPress);
    
    // Initialize animation speed display and apply default speed
    updateSpeedIndicator();
    applyAnimationSpeed();
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

// Battle animation state
let battleAnimating = false;

// Add message to battle log (only one message at a time)
function addBattleLogMessage(message, isPlayerMessage = true) {
    // Clear existing messages
    while (battleLog.firstChild) {
        battleLog.removeChild(battleLog.firstChild);
    }
    
    // Add new message
    const p = document.createElement('p');
    p.textContent = message;
    
    // Add appropriate class for alignment
    if (isPlayerMessage) {
        p.classList.add('player-message');
    } else {
        p.classList.add('enemy-message');
    }
    
    battleLog.appendChild(p);
    battleLog.scrollTop = battleLog.scrollHeight;
}

// Animate button click
function animateButtonClick(button) {
    button.classList.add('button-clicked');
    setTimeout(() => {
        button.classList.remove('button-clicked');
    }, 300);
}

// Execute player turn with precise timing
function executePlayerTurn(data, choice) {
    const lines = data.message ? data.message.split('\n').filter(line => line.trim()) : [];
    const playerActionLine = lines.find(line => {
        const lower = line.toLowerCase();
        return lower.includes('you ') && (
            lower.includes('attack') || lower.includes('hit') || lower.includes('strike') ||
            lower.includes('defend') || lower.includes('block') || lower.includes('guard') ||
            lower.includes('heal') || lower.includes('restore') || lower.includes('damage') ||
            lower.includes('stance') || lower.includes('ready') || lower.includes('prepare')
        );
    }) || lines.find(line => line.trim().length > 0); // Fallback to any non-empty line
    
    updateTime(data.time);
    
    // 0.25s delay, then show battle log
    setTimeout(() => {
        if (playerActionLine) {
            addBattleLogMessage(playerActionLine, true);
        }
        
        // 0.25s delay, then play attack animation
        setTimeout(() => {
            let animationDuration = 250; // Default fallback
            if (choice <= gameState.options.length) {
                animationDuration = triggerSkillAnimation(gameState.options[choice - 1], true, playerActionLine);
            }
            
            // 4. Update health bar value when damage number is halfway through
            const currentSpeed = ANIMATION_SPEEDS[currentAnimationSpeed];
            const iconDuration = parseFloat(currentSpeed.iconTime) * 1000;
            const damageDuration = parseFloat(currentSpeed.damageTime) * 1000;
            const iconHalfway = iconDuration / 2;
            const damageHalfway = damageDuration / 2;
            const healthBarUpdateDelay = iconHalfway + damageHalfway;
            
            setTimeout(() => {
                if (data.enemy) {
                    gameState.enemy = data.enemy;
                    const maxEnemyHealth = data.enemy.name === 'Goblin' ? 3 : 5;
                    const healthPercentage = (data.enemy.health / maxEnemyHealth) * 100;
                    enemyHealthBar.style.width = `${healthPercentage}%`;
                    enemyHealthText.textContent = `${data.enemy.health} HP`;
                }
            }, healthBarUpdateDelay);
            
            // Wait for all animations to complete before continuing
            setTimeout(() => {
                
                // Check if battle continues
                if (data.event === 'battle' && data.enemy && data.enemy.health > 0) {
                    executeEnemyTurn(data);
                } else {
                    battleAnimating = false;
                    setBattleActionsEnabled(true);
                    updateGameState(data);
                }
            }, animationDuration);
        }, 250);
    }, 250);
}

// Execute enemy turn with precise timing
function executeEnemyTurn(data) {
    const lines = data.message ? data.message.split('\n').filter(line => line.trim()) : [];
    
    // Try multiple patterns to find enemy action
    let enemyActionLine = lines.find(line => {
        const lower = line.toLowerCase();
        return (lower.includes('goblin') || lower.includes('enemy')) && (
            lower.includes('attack') || lower.includes('hit') || lower.includes('strike') ||
            lower.includes('damage')
        ) && !lower.includes('you attack');
    });
    
    // If not found, look for any line that mentions damage to player
    if (!enemyActionLine) {
        enemyActionLine = lines.find(line => {
            const lower = line.toLowerCase();
            return lower.includes('damage') && !lower.includes('you attack') && !lower.includes('you hit');
        });
    }
    
    // If still not found, use a generic message
    if (!enemyActionLine && lines.length > 0) {
        enemyActionLine = lines[lines.length - 1]; // Use last line as fallback
    }
    
    // 0.5s delay before enemy turn starts
    setTimeout(() => {
        // 0.25s delay, then show enemy battle log
        setTimeout(() => {
            if (enemyActionLine) {
                addBattleLogMessage(enemyActionLine, false);
            }
            
            // 0.25s delay, then play enemy attack animation
            setTimeout(() => {
                const animationDuration = triggerSkillAnimation('attack', false, enemyActionLine);
                
                // 4. Update player health bar value when damage number is halfway through
                const currentSpeed = ANIMATION_SPEEDS[currentAnimationSpeed];
                const iconDuration = parseFloat(currentSpeed.iconTime) * 1000;
                const damageDuration = parseFloat(currentSpeed.damageTime) * 1000;
                const iconHalfway = iconDuration / 2;
                const damageHalfway = damageDuration / 2;
                const healthBarUpdateDelay = iconHalfway + damageHalfway;
                
                setTimeout(() => {
                    updatePlayerStatus(data.player);
                }, healthBarUpdateDelay);
                
                // Wait for all animations to complete before continuing
                setTimeout(() => {
                    battleAnimating = false;
                    setBattleActionsEnabled(true);
                }, animationDuration);
            }, 250);
        }, 250);
    }, 500);
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
        // In battle mode, DON'T show messages immediately - let battle actions show first
        // Only show battle messages during actual combat turns, not at battle start
        
        // Hide current message container during battle
        document.querySelector('.current-message-container').style.display = 'none';
    } else if (gameState.event === 'battle' && event !== 'battle') {
        // Battle just ended - show victory or defeat screen
        // Show current message container again
        document.querySelector('.current-message-container').style.display = 'block';
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
        // For non-battle events, ensure current message container is visible and add message
        document.querySelector('.current-message-container').style.display = 'block';
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
            p.style.textTransform = 'none'; // Ensure text is not transformed
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
    
    // Clear battle log when battle starts
    while (battleLog.firstChild) {
        battleLog.removeChild(battleLog.firstChild);
    }
    
    // Debug: Log that we're showing battle info
    console.log('Showing battle info, options:', gameState.options);
    
    // Ensure battle actions are created and shown immediately when battle starts
    updateBattleActions();
    
    // Use the same approach as setBattleActionsEnabled to ensure consistent centering
    setBattleActionsEnabled(true);
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
            animateButtonClick(button);
            takeAction(index + 1);
        });
        
        battleActions.appendChild(button);
    });
}

// Hide battle actions
function hideBattleActions() {
    const battleActions = document.getElementById('battle-actions');
    const battleLog = document.getElementById('battle-log');
    
    if (battleActions) {
        while (battleActions.firstChild) {
            battleActions.removeChild(battleActions.firstChild);
        }
        battleActions.classList.remove('show');
    }
    
    // Show battle log when hiding actions
    if (battleLog) {
        battleLog.style.display = 'block';
    }
}

// Trigger skill animation on specific health bar
function triggerSkillAnimation(actionText, isPlayerAction = true, battleMessage = '') {
    const lowerAction = actionText.toLowerCase();
    let animationClass = '';
    let hpAnimationClass = '';
    let targetElement = null;
    let actionType = '';
    
    // Get current animation speed
    const currentSpeed = ANIMATION_SPEEDS[currentAnimationSpeed];
    const healthBarDuration = parseFloat(currentSpeed.iconTime) * 1000;
    
    if (lowerAction.includes('attack') || lowerAction.includes('hit') || lowerAction.includes('strike')) {
        animationClass = 'skill-animation-attack';
        hpAnimationClass = 'hp-animation-attack';
        actionType = 'attack';
        // Attack animations target the opponent's health bar
        targetElement = isPlayerAction ? document.getElementById('enemy-info') : document.getElementById('player-battle-info');
        
        // Trigger screen shake for attacks
        triggerScreenShake();
        
        // Extract damage and determine max health for icon sizing
        const damage = extractDamageFromMessage(battleMessage);
        let maxHealth;
        
        if (isPlayerAction) {
            // Player attacking enemy - get enemy max health
            maxHealth = gameState.enemy && gameState.enemy.name === 'Goblin' ? 3 : 5;
        } else {
            // Enemy attacking player - get player max health from current game state
            maxHealth = document.getElementById('health').textContent.split('/')[1] || 10;
            maxHealth = parseInt(maxHealth);
        }
        
        // 1. Show action icon (starts immediately) with proportional sizing
        showActionIcon(targetElement, actionType, damage, maxHealth);
        
        // 3. Show damage number when icon is halfway through animation
        const iconDuration = parseFloat(currentSpeed.iconTime) * 1000;
        const iconHalfway = iconDuration / 2;
        setTimeout(() => {
            if (damage > 0) {
                showDamageNumber(targetElement, damage, false);
            }
        }, iconHalfway);
        
    } else if (lowerAction.includes('heal') || lowerAction.includes('restore') || lowerAction.includes('recover')) {
        animationClass = 'skill-animation-heal';
        hpAnimationClass = 'hp-animation-heal';
        actionType = 'heal';
        // Heal animations target the caster's health bar
        targetElement = isPlayerAction ? document.getElementById('player-battle-info') : document.getElementById('enemy-info');
        
        // Extract heal amount for icon sizing (heal actions don't scale with damage percentage)
        const healAmount = extractDamageFromMessage(battleMessage);
        
        // 1. Show action icon (starts immediately) - heal icons don't scale with damage
        showActionIcon(targetElement, actionType);
        
        // 3. Show heal number when icon is halfway through animation
        const iconDuration = parseFloat(currentSpeed.iconTime) * 1000;
        const iconHalfway = iconDuration / 2;
        setTimeout(() => {
            if (healAmount > 0) {
                showDamageNumber(targetElement, healAmount, true);
            }
        }, iconHalfway);
        
    } else if (lowerAction.includes('defend') || lowerAction.includes('block') || lowerAction.includes('guard')) {
        animationClass = 'skill-animation-defend';
        hpAnimationClass = 'hp-animation-defend';
        actionType = 'defend';
        // Defend animations target the caster's health bar
        targetElement = isPlayerAction ? document.getElementById('player-battle-info') : document.getElementById('enemy-info');
        
        // 1. Show action icon (starts immediately) - defend doesn't have damage numbers
        showActionIcon(targetElement, actionType);
    }
    
    if (animationClass && targetElement) {
        // 2. Start health bar flash animation immediately with icon
        const skillAnimationName = animationClass.replace('skill-animation-', '');
        const hpAnimationName = hpAnimationClass.replace('hp-animation-', '');
        
        // Apply animations with current speed
        targetElement.style.animation = `${skillAnimationName}-flash ${currentSpeed.iconTime} ease-in-out, ${hpAnimationName}-flash ${currentSpeed.iconTime} ease-in-out`;
        targetElement.classList.add(animationClass, hpAnimationClass);
        
        setTimeout(() => {
            targetElement.classList.remove(animationClass, hpAnimationClass);
            targetElement.style.animation = ''; // Clear inline animation
        }, healthBarDuration);
    }
    
    // Return the total animation duration for timing coordination
    return Math.max(parseFloat(currentSpeed.damageTime) * 1000, parseFloat(currentSpeed.iconTime) * 1000);
}

// Trigger screen shake effect
function triggerScreenShake() {
    const gameContainer = document.querySelector('.game-container');
    if (gameContainer) {
        gameContainer.classList.add('screen-shake');
        setTimeout(() => {
            gameContainer.classList.remove('screen-shake');
        }, 500);
    }
}

// Show damage number floating up from health bar
function showDamageNumber(targetElement, damage, isHealing = false) {
    if (!targetElement || !damage) return;
    
    const damageElement = document.createElement('div');
    damageElement.classList.add('damage-number');
    damageElement.classList.add(isHealing ? 'heal' : 'damage');
    damageElement.textContent = isHealing ? `+${damage}` : `-${damage}`;
    
    // Apply current animation speed directly to the element
    const currentSpeed = ANIMATION_SPEEDS[currentAnimationSpeed];
    const animationName = isHealing ? 'heal-float' : 'damage-float';
    damageElement.style.animation = `${animationName} ${currentSpeed.damageTime} ease-out forwards`;
    
    targetElement.appendChild(damageElement);
    
    // Remove the element after animation completes (use longer timeout for slower animations)
    const timeoutDuration = parseFloat(currentSpeed.damageTime) * 1000;
    setTimeout(() => {
        if (damageElement.parentNode) {
            damageElement.parentNode.removeChild(damageElement);
        }
    }, timeoutDuration);
}

// Show action icon next to battle info with size based on damage percentage
function showActionIcon(targetElement, actionType, damage = 0, maxHealth = 0) {
    if (!targetElement) return;
    
    // Remove any existing action icons
    const existingIcon = targetElement.querySelector('.action-icon');
    if (existingIcon) {
        existingIcon.remove();
    }
    
    const iconElement = document.createElement('div');
    iconElement.classList.add('action-icon', actionType);
    
    // Calculate damage percentage and add size class
    if (damage > 0 && maxHealth > 0 && actionType === 'attack') {
        const damagePercentage = (damage / maxHealth) * 100;
        let sizeClass = 'size-medium'; // Default
        
        // Debug logging
        console.log(`Icon sizing: damage=${damage}, maxHealth=${maxHealth}, percentage=${damagePercentage.toFixed(1)}%`);
        
        if (damagePercentage >= 50) {
            sizeClass = 'size-huge';
        } else if (damagePercentage >= 35) {
            sizeClass = 'size-large';
        } else if (damagePercentage >= 20) {
            sizeClass = 'size-medium';
        } else if (damagePercentage >= 10) {
            sizeClass = 'size-small';
        } else {
            sizeClass = 'size-tiny';
        }
        
        console.log(`Applied size class: ${sizeClass}`);
        iconElement.classList.add(sizeClass);
    }
    
    // Get random variation for the action type
    const variations = ICON_VARIATIONS[actionType] || ['⚡'];
    const randomIcon = variations[Math.floor(Math.random() * variations.length)];
    iconElement.textContent = randomIcon;
    
    // Apply current animation speed directly to the element
    const currentSpeed = ANIMATION_SPEEDS[currentAnimationSpeed];
    const animationName = `action-icon-${actionType}`;
    iconElement.style.animation = `${animationName} ${currentSpeed.iconTime} ease-out forwards`;
    
    targetElement.appendChild(iconElement);
    
    // Remove the icon after animation completes (use longer timeout for slower animations)
    const timeoutDuration = parseFloat(currentSpeed.iconTime) * 1000;
    setTimeout(() => {
        if (iconElement.parentNode) {
            iconElement.parentNode.removeChild(iconElement);
        }
    }, timeoutDuration);
}

// Extract damage amount from battle message
function extractDamageFromMessage(message) {
    if (!message) return 0;
    
    // Look for damage patterns like "2 damage", "takes 3 damage", "deals 1 damage"
    const damageMatch = message.match(/(?:deals?|takes?|suffers?)\s+(\d+)\s+damage/i) || 
                       message.match(/(\d+)\s+damage/i);
    
    if (damageMatch && damageMatch[1]) {
        return parseInt(damageMatch[1]);
    }
    
    // Look for healing patterns like "heals 2", "restores 3 health"
    const healMatch = message.match(/(?:heals?|restores?)\s+(\d+)/i);
    if (healMatch && healMatch[1]) {
        return parseInt(healMatch[1]);
    }
    
    return 1; // Default damage/heal amount if we can't parse it
}

// Toggle animation speed
function toggleAnimationSpeed() {
    currentAnimationSpeed = (currentAnimationSpeed + 1) % ANIMATION_SPEEDS.length;
    updateSpeedIndicator();
    applyAnimationSpeed();
}

// Update the speed indicator display
function updateSpeedIndicator() {
    if (speedIndicator) {
        speedIndicator.textContent = ANIMATION_SPEEDS[currentAnimationSpeed].name;
    }
}

// Apply the current animation speed to CSS
function applyAnimationSpeed() {
    const currentSpeed = ANIMATION_SPEEDS[currentAnimationSpeed];
    
    // Create or update the dynamic style element
    let styleElement = document.getElementById('dynamic-animation-speeds');
    if (!styleElement) {
        styleElement = document.createElement('style');
        styleElement.id = 'dynamic-animation-speeds';
        document.head.appendChild(styleElement);
    }
    
    // Update CSS with current animation speeds - using more specific selectors
    styleElement.textContent = `
        .battle-info .damage-number.damage {
            animation: damage-float ${currentSpeed.damageTime} ease-out forwards !important;
        }
        
        .battle-info .damage-number.heal {
            animation: heal-float ${currentSpeed.damageTime} ease-out forwards !important;
        }
        
        .battle-info .action-icon.attack {
            animation: action-icon-attack ${currentSpeed.iconTime} ease-out forwards !important;
        }
        
        .battle-info .action-icon.defend {
            animation: action-icon-defend ${currentSpeed.iconTime} ease-out forwards !important;
        }
        
        .battle-info .action-icon.heal {
            animation: action-icon-heal ${currentSpeed.iconTime} ease-out forwards !important;
        }
    `;
    
    console.log('Applied animation speed:', currentSpeed.name, 'Damage:', currentSpeed.damageTime, 'Icons:', currentSpeed.iconTime);
}

// Disable/enable battle actions
function setBattleActionsEnabled(enabled) {
    const battleActions = document.getElementById('battle-actions');
    const battleLog = document.getElementById('battle-log');
    
    console.log('setBattleActionsEnabled called with:', enabled);
    console.log('battleActions element:', battleActions);
    console.log('battleLog element:', battleLog);
    
    if (battleActions && battleLog) {
        if (enabled) {
            // Show battle actions using CSS class with !important rules
            battleActions.classList.add('centered');
            battleLog.style.display = 'none';
            console.log('Battle actions should now be visible and centered');
            console.log('Battle actions has centered class:', battleActions.classList.contains('centered'));
            console.log('Battle actions computed style:', window.getComputedStyle(battleActions).display);
            console.log('Battle actions children count:', battleActions.children.length);
        } else {
            // Show battle log, hide battle actions
            battleActions.classList.remove('centered');
            battleLog.style.display = 'block';
            console.log('Battle log should now be visible');
        }
    } else {
        console.log('Missing elements - battleActions:', !!battleActions, 'battleLog:', !!battleLog);
    }
}

// Take an action
function takeAction(choice) {
    // Prevent action if battle is animating
    if (battleAnimating) return;
    
    const requestData = {
        event: gameState.event,
        choice: choice
    };
    
    // Add enemy info if in battle
    if (gameState.event === 'battle' && gameState.enemy) {
        requestData.enemy_name = gameState.enemy.name;
        requestData.enemy_health = gameState.enemy.health;
        
        // Start battle animation sequence
        battleAnimating = true;
        setBattleActionsEnabled(false);
        
        // Send server request immediately
        fetch('/api/action', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestData)
        })
        .then(response => response.json())
        .then(data => {
            // Start player turn sequence with precise timing
            executePlayerTurn(data, choice);
        })
        .catch(error => {
            console.error('Error:', error);
            addCurrentMessage('Error processing action. Please try again.');
            battleAnimating = false;
            setBattleActionsEnabled(true);
        });
    } else {
        // Non-battle actions proceed normally
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
}