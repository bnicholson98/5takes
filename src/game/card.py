"""Card and deck management for 5 Takes game."""

from typing import List
import random


class Card:
    """Represents a single card with value and point calculation."""
    
    def __init__(self, value: int):
        """Initialize card with given value.
        
        Args:
            value: Card value between 1 and 104
            
        Raises:
            ValueError: If value is not between 1 and 104
        """
        if not 1 <= value <= 104:
            raise ValueError("Card value must be between 1 and 104")
        self._value = value
    
    @property
    def value(self) -> int:
        """Get the card's numeric value.
        
        Returns:
            The card's numeric value (1-104)
        """
        return self._value
    
    @property
    def points(self) -> int:
        """Calculate penalty points for this card.
        
        Returns:
            Penalty points (1-7) based on card value
        """
        if self._value == 55:
            return 7
        elif self._value % 11 == 0:
            return 5
        elif self._value % 10 == 0:
            return 3
        elif self._value % 5 == 0:
            return 2
        else:
            return 1
    
    def __str__(self) -> str:
        """String representation of card.
        
        Returns:
            Formatted card string like '[42]'
        """
        return f"[{self._value}]"
    
    def __repr__(self) -> str:
        """Debug representation of card.
        
        Returns:
            Debug string like 'Card(42)'
        """
        return f"Card({self._value})"
    
    def __eq__(self, other) -> bool:
        """Check equality based on card value.
        
        Args:
            other: Object to compare with
            
        Returns:
            True if other is a Card with same value
        """
        if isinstance(other, Card):
            return self._value == other._value
        return False
    
    def __lt__(self, other) -> bool:
        """Compare cards by value.
        
        Args:
            other: Card to compare with
            
        Returns:
            True if this card's value is less than other's
        """
        if isinstance(other, Card):
            return self._value < other._value
        return NotImplemented
    
    def __hash__(self) -> int:
        """Hash based on card value.
        
        Returns:
            Hash value for use in sets and dicts
        """
        return hash(self._value)


class Deck:
    """Manages the deck of 104 cards."""
    
    def __init__(self):
        """Initialize deck with all 104 cards."""
        self._cards = [Card(i) for i in range(1, 105)]
        self.shuffle()
    
    def shuffle(self) -> None:
        """Shuffle the deck randomly."""
        random.shuffle(self._cards)
    
    def deal_card(self) -> Card:
        """Deal one card from the deck.
        
        Returns:
            The dealt card
            
        Raises:
            IndexError: If deck is empty
        """
        if not self._cards:
            raise IndexError("Cannot deal from empty deck")
        return self._cards.pop()
    
    def deal_cards(self, count: int) -> List[Card]:
        """Deal multiple cards from the deck.
        
        Args:
            count: Number of cards to deal
            
        Returns:
            List of dealt cards
            
        Raises:
            IndexError: If not enough cards remaining
        """
        if count > len(self._cards):
            raise IndexError(f"Cannot deal {count} cards, only {len(self._cards)} remaining")
        return [self.deal_card() for _ in range(count)]
    
    @property
    def remaining_cards(self) -> int:
        """Get number of cards remaining in deck.
        
        Returns:
            Number of cards left in deck
        """
        return len(self._cards)
    
    def reset(self) -> None:
        """Reset deck with all 104 cards and shuffle."""
        self._cards = [Card(i) for i in range(1, 105)]
        self.shuffle()
