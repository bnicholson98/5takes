"""Player management for 5 Takes game."""

from typing import List, Optional
from .card import Card


class Player:
    """Represents a player in the game."""
    
    def __init__(self, name: str):
        """Initialize player with name.
        
        Args:
            name: Player's name
            
        Raises:
            ValueError: If name is empty or whitespace
        """
        if not name.strip():
            raise ValueError("Player name cannot be empty")
        self._name = name.strip()
        self._hand: List[Card] = []
        self._total_score = 0
        self._round_score = 0
        self._selected_card: Optional[Card] = None
    
    @property
    def name(self) -> str:
        """Get player's name.
        
        Returns:
            The player's name
        """
        return self._name
    
    @property
    def hand(self) -> List[Card]:
        """Get player's current hand.
        
        Returns:
            Sorted list of cards in hand
        """
        return sorted(self._hand)
    
    @property
    def hand_size(self) -> int:
        """Get number of cards in hand.
        
        Returns:
            Current number of cards in hand
        """
        return len(self._hand)
    
    @property
    def total_score(self) -> int:
        """Get player's total score across all rounds.
        
        Returns:
            Cumulative penalty points
        """
        return self._total_score
    
    @property
    def round_score(self) -> int:
        """Get player's score for current round.
        
        Returns:
            Penalty points gained this round
        """
        return self._round_score
    
    @property
    def selected_card(self) -> Optional[Card]:
        """Get the card selected for current turn.
        
        Returns:
            Selected card or None if no selection
        """
        return self._selected_card
    
    @property
    def has_selected_card(self) -> bool:
        """Check if player has selected a card for current turn.
        
        Returns:
            True if card is selected for this turn
        """
        return self._selected_card is not None
    
    def deal_cards(self, cards: List[Card]) -> None:
        """Add cards to player's hand.
        
        Args:
            cards: Cards to add to hand
        """
        self._hand.extend(cards)
        self._hand.sort()
    
    def has_card(self, card: Card) -> bool:
        """Check if player has specific card in hand.
        
        Args:
            card: Card to check for
            
        Returns:
            True if card is in hand
        """
        return card in self._hand
    
    def select_card(self, card: Card) -> None:
        """Select a card from hand for current turn.
        
        Args:
            card: Card to select
            
        Raises:
            ValueError: If card not in hand or already selected
        """
        if card not in self._hand:
            raise ValueError(f"Card {card.value} not in player's hand")
        if self._selected_card is not None:
            raise ValueError("Player has already selected a card this turn")
        
        self._selected_card = card
    
    def play_selected_card(self) -> Card:
        """Remove and return the selected card.
        
        Returns:
            The selected card
            
        Raises:
            ValueError: If no card is selected
        """
        if self._selected_card is None:
            raise ValueError("No card selected")
        
        played_card = self._selected_card
        self._hand.remove(played_card)
        self._selected_card = None
        return played_card
    
    def add_penalty_points(self, points: int) -> None:
        """Add penalty points to player's scores.
        
        Args:
            points: Penalty points to add
            
        Raises:
            ValueError: If points is negative
        """
        if points < 0:
            raise ValueError("Penalty points cannot be negative")
        self._round_score += points
        self._total_score += points
    
    def reset_round_score(self) -> None:
        """Reset round score to 0 (for new round)."""
        self._round_score = 0
    
    def clear_selection(self) -> None:
        """Clear current card selection."""
        self._selected_card = None
    
    def get_card_by_index(self, index: int) -> Card:
        """Get card from hand by index.
        
        Args:
            index: Zero-based index into hand
            
        Returns:
            Card at that position in hand
            
        Raises:
            IndexError: If index is out of range
        """
        if not 0 <= index < len(self._hand):
            raise IndexError(f"Hand index must be 0-{len(self._hand)-1}")
        return self._hand[index]
    
    def __str__(self) -> str:
        """String representation of player.
        
        Returns:
            Player name and total score
        """
        return f"{self._name} (Score: {self._total_score})"
    
    def __repr__(self) -> str:
        """Debug representation of player.
        
        Returns:
            Debug string with name, score, and hand size
        """
        return f"Player('{self._name}', score={self._total_score}, hand_size={len(self._hand)})"
