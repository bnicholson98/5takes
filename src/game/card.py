"""Card and deck management for 5 Takes game."""

from typing import List
import random


class Card:
    """Represents a single card with value and point calculation."""
    
    def __init__(self, value: int):
        """Initialize card with given value (1-104)."""
        if not 1 <= value <= 104:
            raise ValueError("Card value must be between 1 and 104")
        self._value = value
    
    @property
    def value(self) -> int:
        """Get the card's numeric value."""
        return self._value
    
    @property
    def points(self) -> int:
        """Calculate penalty points for this card."""
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
        """String representation of card."""
        return f"[{self._value}]"
    
    def __repr__(self) -> str:
        """Debug representation of card."""
        return f"Card({self._value})"
    
    def __eq__(self, other) -> bool:
        """Check equality based on card value."""
        if isinstance(other, Card):
            return self._value == other._value
        return False
    
    def __lt__(self, other) -> bool:
        """Compare cards by value."""
        if isinstance(other, Card):
            return self._value < other._value
        return NotImplemented
    
    def __hash__(self) -> int:
        """Hash based on card value."""
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
        """Deal one card from the deck."""
        if not self._cards:
            raise IndexError("Cannot deal from empty deck")
        return self._cards.pop()
    
    def deal_cards(self, count: int) -> List[Card]:
        """Deal multiple cards from the deck."""
        if count > len(self._cards):
            raise IndexError(f"Cannot deal {count} cards, only {len(self._cards)} remaining")
        return [self.deal_card() for _ in range(count)]
    
    @property
    def remaining_cards(self) -> int:
        """Get number of cards remaining in deck."""
        return len(self._cards)
    
    def reset(self) -> None:
        """Reset deck with all 104 cards and shuffle."""
        self._cards = [Card(i) for i in range(1, 105)]
        self.shuffle()
