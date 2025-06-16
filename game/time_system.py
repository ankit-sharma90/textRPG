"""
Time System module - Manages the day/night cycle
"""

class TimeSystem:
    """Manages the day/night cycle"""
    
    def __init__(self):
        self.time = 0  # 0 = day, 1 = night
        
    def advance_time(self):
        """Advance time to next day/night cycle"""
        self.time = (self.time + 1) % 2
        print(f"Time has changed to {self.get_time_of_day()}")
        
    def get_time_of_day(self):
        """Get the current time of day"""
        return "Day" if self.time == 0 else "Night"
    
    def is_daytime(self):
        """Check if it's currently daytime"""
        return self.time == 0