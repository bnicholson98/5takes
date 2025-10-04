"""Game table and row management for 5 Takes."""

from typing import List, Optional
from .card import Card


class Row:
    """Represents a single row of cards on the table."""
    
    MAX_CARDS = 5
    
    def __init__(self, starting_card: Card):
        """Initialize row with a starting card.
        
        Args:
            starting_card: The first card in the row
        """
        self._cards = [starting_card]
    
    @property
    def cards(self) -> List[Card]:
        """Get list of cards in this row.
        
        Returns:
            Copy of cards list in this row
        """
        return self._cards.copy()
    
    @property
    def last_card(self) -> Card:
        """Get the rightmost card in the row.
        
        Returns:
            The last card placed in this row
        """
        return self._cards[-1]
    
    @property
    def is_full(self) -> bool:
        """Check if row has maximum cards.
        
        Returns:
            True if row has 5 or more cards
        """
        return len(self._cards) >= self.MAX_CARDS
    
    @property
    def card_count(self) -> int:
        """Get number of cards in row.
        
        Returns:
            Current number of cards in this row
        """
        return len(self._cards)
    
    @property
    def total_points(self) -> int:
        """Calculate total penalty points for all cards in row.
        
        Returns:
            Sum of penalty points for all cards
        """
        return sum(card.points for card in self._cards)
    
    def can_place_card(self, card: Card) -> bool:
        """Check if card can be placed in this row.
        
        Args:
            card: Card to check placement for
            
        Returns:
            True if card can be legally placed
        """
        return card.value > self.last_card.value and not self.is_full
    
    def place_card(self, card: Card) -> Optional[List[Card]]:
        """Place card in row. Returns wiped cards if row becomes full.
        
        Args:
            card: Card to place in row
            
        Returns:
            List of wiped cards if row became full, None otherwise
            
        Raises:
            ValueError: If card cannot be placed in row
        """
        if not card.value > self.last_card.value:
            raise ValueError(f"Card {card.value} cannot be placed after {self.last_card.value}")
        
        if self.is_full:
            raise ValueError("Cannot place card in full row")
        
        self._cards.append(card)
        
        if self.is_full:
            wiped_cards = self._cards[:-1]  # All cards except the last one
            self._cards = [card]  # Keep only the card that was just placed
            return wiped_cards
        
        return None
    
    def wipe_and_replace(self, new_card: Card) -> List[Card]:
        """Replace all cards in row with new starting card.
        
        Args:
            new_card: Card to become new starting card
            
        Returns:
            List of all cards that were wiped
        """
        wiped_cards = self._cards.copy()
        self._cards = [new_card]
        return wiped_cards
    
    def __str__(self) -> str:
        """String representation of row.
        
        Returns:
            Space-separated string of cards in row
        """
        return " ".join(str(card) for card in self._cards)


class Table:
    """Manages the 4 rows of cards on the game table."""
    
    NUM_ROWS = 4
    
    def __init__(self, starting_cards: List[Card]):
        """Initialize table with 4 starting cards.
        
        Args:
            starting_cards: List of exactly 4 cards for row starts
            
        Raises:
            ValueError: If not exactly 4 starting cards provided
        """
        if len(starting_cards) != self.NUM_ROWS:
            raise ValueError(f"Table requires exactly {self.NUM_ROWS} starting cards")
        
        self._rows = [Row(card) for card in starting_cards]
    
    @property
    def rows(self) -> List[Row]:
        """Get list of all rows.
        
        Returns:
            Copy of all 4 rows on table
        """
        return self._rows.copy()
    
    def get_row(self, index: int) -> Row:
        """Get specific row by index.
        
        Args:
            index: Row index (0-3)
            
        Returns:
            The requested row
            
        Raises:
            IndexError: If index is not 0-3
        """
        if not 0 <= index < self.NUM_ROWS:
            raise IndexError(f"Row index must be 0-{self.NUM_ROWS-1}")
        return self._rows[index]
    
    def find_target_row(self, card: Card) -> Optional[int]:
        """Find the best row for placing a card.
        
        Args:
            card: Card to find placement for
            
        Returns:
            Row index (0-3) or None if no valid placement
        """
        best_row = None
        smallest_gap = float('inf')
        
        for i, row in enumerate(self._rows):
            if row.can_place_card(card):
                gap = card.value - row.last_card.value
                if gap < smallest_gap:
                    smallest_gap = gap
                    best_row = i
        
        return best_row
    
    def place_card(self, card: Card, forced_row: Optional[int] = None) -> tuple[int, Optional[List[Card]]]:
        """Place card on table.
        
        Args:
            card: Card to place
            forced_row: Specific row index to wipe and replace
            
        Returns:
            Tuple of (row_index, wiped_cards)
            
        Raises:
            ValueError: If card cannot be placed
            IndexError: If forced_row is invalid
        """
        if forced_row is not None:
            if not 0 <= forced_row < self.NUM_ROWS:
                raise IndexError(f"Row index must be 0-{self.NUM_ROWS-1}")
            wiped_cards = self._rows[forced_row].wipe_and_replace(card)
            return forced_row, wiped_cards
        
        target_row = self.find_target_row(card)
        if target_row is None:
            raise ValueError(f"Card {card.value} cannot be placed on any row")
        
        wiped_cards = self._rows[target_row].place_card(card)
        return target_row, wiped_cards
    
    def must_wipe_row(self, card: Card) -> bool:
        """Check if card forces player to wipe a row.
        
        Args:
            card: Card to check
            
        Returns:
            True if card is too low for all rows
        """
        return self.find_target_row(card) is None
    
    def get_row_choices(self) -> List[int]:
        """Get list of available row indices for wiping.
        
        Returns:
            List of row indices (0-3)
        """
        return list(range(self.NUM_ROWS))
    
    def __str__(self) -> str:
        """String representation of table.
        
        Returns:
            Multi-line string showing all rows
        """
        lines = []
        for i, row in enumerate(self._rows):
            lines.append(f"Row {i+1}: {row}")
        return "\n".join(lines)
