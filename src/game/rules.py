"""Game rules and validation for 5 Takes."""

from typing import List
from .card import Card
from .player import Player


class GameRules:
    """Encapsulates all game rules and validation."""
    
    MIN_PLAYERS = 3
    MAX_PLAYERS = 10
    CARDS_PER_PLAYER = 10
    STARTING_ROWS = 4
    TOTAL_CARDS = 104
    GAME_END_SCORE = 50
    
    @classmethod
    def validate_player_count(cls, count: int) -> None:
        """Validate number of players.
        
        Args:
            count: Number of players
            
        Raises:
            ValueError: If count is not between 3 and 10
        """
        if not cls.MIN_PLAYERS <= count <= cls.MAX_PLAYERS:
            raise ValueError(f"Game requires {cls.MIN_PLAYERS}-{cls.MAX_PLAYERS} players")
    
    @classmethod
    def validate_player_names(cls, names: List[str]) -> None:
        """Validate player names are unique and non-empty.
        
        Args:
            names: List of player names to validate
            
        Raises:
            ValueError: If names are empty, non-unique, or contain empty strings
        """
        if not names:
            raise ValueError("No player names provided")
        
        cleaned_names = [name.strip() for name in names]
        
        if any(not name for name in cleaned_names):
            raise ValueError("Player names cannot be empty")
        
        if len(set(cleaned_names)) != len(cleaned_names):
            raise ValueError("Player names must be unique")
    
    @classmethod
    def calculate_cards_needed(cls, player_count: int) -> int:
        """Calculate total cards needed for game setup.
        
        Args:
            player_count: Number of players
            
        Returns:
            Total cards needed (players * 10 + 4)
        """
        return (player_count * cls.CARDS_PER_PLAYER) + cls.STARTING_ROWS
    
    @classmethod
    def is_game_over(cls, players: List[Player]) -> bool:
        """Check if any player has exceeded the game end threshold.
        
        Args:
            players: List of players to check
            
        Returns:
            True if any player has more than 50 points
        """
        return any(player.total_score > cls.GAME_END_SCORE for player in players)
    
    @classmethod
    def find_winner(cls, players: List[Player]) -> Player:
        """Find the player with the lowest total score.
        
        Args:
            players: List of players to check
            
        Returns:
            Player with lowest total score
            
        Raises:
            ValueError: If no players provided
        """
        if not players:
            raise ValueError("No players to determine winner")
        return min(players, key=lambda p: p.total_score)
    
    @classmethod
    def is_round_over(cls, players: List[Player]) -> bool:
        """Check if all players have empty hands.
        
        Args:
            players: List of players to check
            
        Returns:
            True if all players have no cards
        """
        return all(player.hand_size == 0 for player in players)
    
    @classmethod
    def all_players_selected(cls, players: List[Player]) -> bool:
        """Check if all players have selected cards.
        
        Args:
            players: List of players to check
            
        Returns:
            True if all players have selected cards
        """
        return all(player.has_selected_card for player in players)
    
    @classmethod
    def calculate_penalty_points(cls, cards: List[Card]) -> int:
        """Calculate total penalty points for a list of cards.
        
        Args:
            cards: List of cards to calculate points for
            
        Returns:
            Sum of penalty points for all cards
        """
        return sum(card.points for card in cards)
    
    @classmethod
    def sort_players_by_card_value(cls, players: List[Player]) -> List[Player]:
        """Sort players by their selected card values.
        
        Args:
            players: List of players with selected cards
            
        Returns:
            Players sorted by card value (ascending)
        """
        return sorted(
            [p for p in players if p.has_selected_card],
            key=lambda p: p.selected_card.value
        )
    
    @classmethod
    def validate_card_selection(cls, player: Player, card: Card) -> None:
        """Validate that a player can select a specific card.
        
        Args:
            player: Player attempting selection
            card: Card to select
            
        Raises:
            ValueError: If selection is invalid
        """
        if not player.has_card(card):
            raise ValueError(f"Player {player.name} does not have card {card.value}")
        
        if player.has_selected_card:
            raise ValueError(f"Player {player.name} has already selected a card")
