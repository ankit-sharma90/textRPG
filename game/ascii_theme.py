"""
ASCII Art Theme Module - Contains all ASCII art elements for the game
"""

class ASCIITheme:
    """ASCII art theme for the text RPG"""
    
    # Game title
    TITLE = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║  ████████╗███████╗██╗  ██╗████████╗    ██████╗ ██████╗  ██████╗             ║
║  ╚══██╔══╝██╔════╝╚██╗██╔╝╚══██╔══╝    ██╔══██╗██╔══██╗██╔════╝             ║
║     ██║   █████╗   ╚███╔╝    ██║       ██████╔╝██████╔╝██║  ███╗            ║
║     ██║   ██╔══╝   ██╔██╗    ██║       ██╔══██╗██╔═══╝ ██║   ██║            ║
║     ██║   ███████╗██╔╝ ██╗   ██║       ██║  ██║██║     ╚██████╔╝            ║
║     ╚═╝   ╚══════╝╚═╝  ╚═╝   ╚═╝       ╚═╝  ╚═╝╚═╝      ╚═════╝             ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

    # Status borders
    STATUS_TOP = "╔═══════════════════════════════════════════════════════════════════════════════╗"
    STATUS_MID = "╠═══════════════════════════════════════════════════════════════════════════════╣"
    STATUS_BOT = "╚═══════════════════════════════════════════════════════════════════════════════╝"
    STATUS_SIDE = "║"
    
    # Battle frames
    BATTLE_FRAME = """
┌─────────────────────────────────────────────────────────────────────────────┐
│                              ⚔️  BATTLE  ⚔️                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  {player_art}                                    {enemy_art}                │
│                                                                             │
│  {player_name:<20}                      {enemy_name:>20}                   │
│  HP: {player_hp:<15}                      HP: {enemy_hp:>15}               │
│                                                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│ {battle_log:<75} │
└─────────────────────────────────────────────────────────────────────────────┘
"""

    # Character sprites
    PLAYER_SPRITE = """
    ⚔️
   /|\\
   / \\
"""

    GOBLIN_SPRITE = """
   👹
  /|\\
  / \\
"""

    OLD_MAN_SPRITE = """
   👴
  /|\\
  / \\
"""

    DRAGON_SPRITE = """
   🐲
  /█\\
 /███\\
"""

    # Health bar components
    HEALTH_FULL = "█"
    HEALTH_EMPTY = "░"
    HEALTH_FRAME_L = "["
    HEALTH_FRAME_R = "]"
    
    # Menu borders
    MENU_TOP = "┌─────────────────────────────────────────────────────────────────────────────┐"
    MENU_MID = "├─────────────────────────────────────────────────────────────────────────────┤"
    MENU_BOT = "└─────────────────────────────────────────────────────────────────────────────┘"
    MENU_SIDE = "│"
    
    # Direction arrows
    ARROWS = {
        'north': '↑',
        'south': '↓', 
        'east': '→',
        'west': '←'
    }
    
    # Location symbols
    LOCATIONS = {
        'forest': '🌲',
        'mountain': '⛰️',
        'cave': '🕳️',
        'village': '🏘️',
        'castle': '🏰',
        'dungeon': '⚱️'
    }
    
    @staticmethod
    def create_health_bar(current_hp, max_hp, width=20):
        """Create an ASCII health bar"""
        if max_hp == 0:
            filled = 0
        else:
            filled = int((current_hp / max_hp) * width)
        empty = width - filled
        
        bar = ASCIITheme.HEALTH_FRAME_L
        bar += ASCIITheme.HEALTH_FULL * filled
        bar += ASCIITheme.HEALTH_EMPTY * empty
        bar += ASCIITheme.HEALTH_FRAME_R
        
        return f"{bar} {current_hp}/{max_hp}"
    
    @staticmethod
    def create_bordered_text(text, width=75):
        """Create bordered text box"""
        lines = text.split('\n')
        result = [ASCIITheme.MENU_TOP]
        
        for line in lines:
            # Pad line to width
            padded_line = f"{line:<{width-4}}"
            result.append(f"{ASCIITheme.MENU_SIDE} {padded_line} {ASCIITheme.MENU_SIDE}")
        
        result.append(ASCIITheme.MENU_BOT)
        return '\n'.join(result)
    
    @staticmethod
    def create_status_display(player, time_system):
        """Create ASCII status display"""
        health_bar = ASCIITheme.create_health_bar(player.health, player.max_health)
        vampire_status = " 🧛 VAMPIRE" if player.is_vampire else ""
        
        status_text = f"""
{ASCIITheme.STATUS_TOP}
{ASCIITheme.STATUS_SIDE} ❤️  Health: {health_bar:<30} 💰 Gold: {player.gold:<10} 🕐 {time_system.get_time_of_day():<10}{vampire_status:<15} {ASCIITheme.STATUS_SIDE}
{ASCIITheme.STATUS_BOT}
"""
        return status_text.strip()
    
    @staticmethod
    def create_battle_display(player_name, player_hp, player_max_hp, enemy_name, enemy_hp, enemy_max_hp, battle_log=""):
        """Create ASCII battle display"""
        player_art = ASCIITheme.PLAYER_SPRITE.strip()
        
        # Choose enemy sprite based on name
        if "goblin" in enemy_name.lower():
            enemy_art = ASCIITheme.GOBLIN_SPRITE.strip()
        elif "dragon" in enemy_name.lower():
            enemy_art = ASCIITheme.DRAGON_SPRITE.strip()
        elif "old man" in enemy_name.lower():
            enemy_art = ASCIITheme.OLD_MAN_SPRITE.strip()
        else:
            enemy_art = ASCIITheme.GOBLIN_SPRITE.strip()
        
        player_hp_bar = ASCIITheme.create_health_bar(player_hp, player_max_hp, 15)
        enemy_hp_bar = ASCIITheme.create_health_bar(enemy_hp, enemy_max_hp, 15)
        
        return ASCIITheme.BATTLE_FRAME.format(
            player_art=player_art,
            enemy_art=enemy_art,
            player_name=player_name,
            enemy_name=enemy_name,
            player_hp=player_hp_bar,
            enemy_hp=enemy_hp_bar,
            battle_log=battle_log[:75]
        )
    
    @staticmethod
    def create_menu_options(options):
        """Create ASCII menu with options"""
        result = [ASCIITheme.MENU_TOP]
        
        for i, option in enumerate(options, 1):
            option_text = f"[{i}] {option}"
            padded_option = f"{option_text:<73}"
            result.append(f"{ASCIITheme.MENU_SIDE} {padded_option} {ASCIITheme.MENU_SIDE}")
        
        result.append(ASCIITheme.MENU_BOT)
        return '\n'.join(result)
    
    # Death screen
    DEATH_SCREEN = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║    ██████╗ ███████╗ █████╗ ████████╗██╗  ██╗                                ║
║    ██╔══██╗██╔════╝██╔══██╗╚══██╔══╝██║  ██║                                ║
║    ██║  ██║█████╗  ███████║   ██║   ███████║                                ║
║    ██║  ██║██╔══╝  ██╔══██║   ██║   ██╔══██║                                ║
║    ██████╔╝███████╗██║  ██║   ██║   ██║  ██║                                ║
║    ╚═════╝ ╚══════╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝                                ║
║                                                                              ║
║                           💀 YOU HAVE DIED 💀                               ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

    # Victory screen
    VICTORY_SCREEN = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║  ██╗   ██╗██╗ ██████╗████████╗ ██████╗ ██████╗ ██╗   ██╗                   ║
║  ██║   ██║██║██╔════╝╚══██╔══╝██╔═══██╗██╔══██╗╚██╗ ██╔╝                   ║
║  ██║   ██║██║██║        ██║   ██║   ██║██████╔╝ ╚████╔╝                    ║
║  ╚██╗ ██╔╝██║██║        ██║   ██║   ██║██╔══██╗  ╚██╔╝                     ║
║   ╚████╔╝ ██║╚██████╗   ██║   ╚██████╔╝██║  ██║   ██║                      ║
║    ╚═══╝  ╚═╝ ╚═════╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝   ╚═╝                      ║
║                                                                              ║
║                          🏆 ENEMY DEFEATED! 🏆                              ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""