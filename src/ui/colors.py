"""Terminal color schemes for 5 Takes game."""

import os
from colorama import Fore, Back, Style, init


class Colors:
    """Terminal color constants and utilities."""
    
    def __init__(self):
        """Initialize colorama for cross-platform support."""
        init(autoreset=True)
    
    HEADER = Fore.CYAN + Style.BRIGHT
    SUCCESS = Fore.GREEN + Style.BRIGHT
    WARNING = Fore.YELLOW + Style.BRIGHT
    ERROR = Fore.RED + Style.BRIGHT
    INFO = Fore.BLUE
    
    CARD = Fore.WHITE + Back.BLUE
    CARD_HIGH_POINTS = Fore.YELLOW + Back.RED + Style.BRIGHT
    CARD_MEDIUM_POINTS = Fore.BLACK + Back.YELLOW
    CARD_LOW_POINTS = Fore.BLACK + Back.GREEN
    
    PLAYER_NAME = Fore.MAGENTA + Style.BRIGHT
    SCORE = Fore.CYAN
    TABLE_ROW = Fore.WHITE + Style.BRIGHT
    
    PROMPT = Fore.GREEN + Style.BRIGHT
    INPUT = Fore.YELLOW
    
    RESET = Style.RESET_ALL
    
    @classmethod
    def card_color(cls, points: int) -> str:
        """Get color code for card based on point value."""
        if points >= 5:
            return cls.CARD_HIGH_POINTS
        elif points >= 3:
            return cls.CARD_MEDIUM_POINTS
        elif points >= 2:
            return cls.CARD_MEDIUM_POINTS
        else:
            return cls.CARD_LOW_POINTS
    
    @classmethod
    def colored_card(cls, value: int, points: int) -> str:
        """Get colored string representation of card."""
        color = cls.card_color(points)
        return f"{color}[{value:3d}]{cls.RESET}"
    
    @classmethod
    def colored_text(cls, text: str, color: str) -> str:
        """Apply color to text."""
        return f"{color}{text}{cls.RESET}"
    
    @staticmethod
    def clear_screen() -> None:
        """Clear terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    @staticmethod
    def print_separator(width: int = 60, char: str = "=") -> None:
        """Print a separator line."""
        print(char * width)
    
    @staticmethod
    def print_centered(text: str, width: int = 60) -> None:
        """Print text centered within given width."""
        print(text.center(width))


colors = Colors()
