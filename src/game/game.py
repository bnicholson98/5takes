"""Main game logic and round management for 5 Takes."""

from typing import List, Tuple, Optional
from .card import Card, Deck
from .player import Player
from .table import Table
from .rules import GameRules


class GameState:
    """Tracks current game state."""
    
    def __init__(self):
        """Initialize empty game state."""
        self.round_number = 0
        self.turn_number = 0
        self.is_game_over = False
        self.winner: Optional[Player] = None


class Game:
    """Main game controller managing rounds and turns."""
    
    def __init__(self, player_names: List[str]):
        """Initialize game with list of player names.
        
        Args:
            player_names: List of unique player names (3-10 players)
            
        Raises:
            ValueError: If player count or names are invalid
        """
        GameRules.validate_player_count(len(player_names))
        GameRules.validate_player_names(player_names)
        
        self._players = [Player(name) for name in player_names]
        self._deck = Deck()
        self._table: Optional[Table] = None
        self._state = GameState()
        self._turn_results: List[Tuple[Player, Card, int, Optional[List[Card]]]] = []
    
    @property
    def players(self) -> List[Player]:
        """Get list of all players.
        
        Returns:
            Copy of players list
        """
        return self._players.copy()
    
    @property
    def table(self) -> Optional[Table]:
        """Get current table state.
        
        Returns:
            Current table or None if no round started
        """
        return self._table
    
    @property
    def state(self) -> GameState:
        """Get current game state.
        
        Returns:
            Current game state object
        """
        return self._state
    
    @property
    def turn_results(self) -> List[Tuple[Player, Card, int, Optional[List[Card]]]]:
        """Get results from the last turn.
        
        Returns:
            List of (player, card, row_index, wiped_cards) tuples
        """
        return self._turn_results.copy()
    
    def start_new_round(self) -> None:
        """Start a new round of the game."""
        self._state.round_number += 1
        self._state.turn_number = 0
        self._turn_results = []
        
        for player in self._players:
            player.reset_round_score()
            player.clear_selection()
        
        self._deck.reset()
        
        starting_cards = self._deck.deal_cards(GameRules.STARTING_ROWS)
        starting_cards.sort()
        self._table = Table(starting_cards)
        
        for player in self._players:
            cards = self._deck.deal_cards(GameRules.CARDS_PER_PLAYER)
            player.deal_cards(cards)
    
    def select_card_for_player(self, player: Player, card: Card) -> None:
        """Select a card for a specific player.
        
        Args:
            player: Player making selection
            card: Card to select
            
        Raises:
            ValueError: If selection is invalid
        """
        GameRules.validate_card_selection(player, card)
        player.select_card(card)
    
    def all_players_selected(self) -> bool:
        """Check if all players have selected cards.
        
        Returns:
            True if all players have selected cards
        """
        return GameRules.all_players_selected(self._players)
    
    def process_turn(self) -> List[Tuple[Player, Card, int, Optional[List[Card]]]]:
        """Process a complete turn with all player selections.
        
        Returns:
            List of (player, card, row_index, wiped_cards) results
            
        Raises:
            ValueError: If not all players have selected cards
        """
        if not self.all_players_selected():
            raise ValueError("Not all players have selected cards")
        
        self._state.turn_number += 1
        self._turn_results = []
        
        sorted_players = GameRules.sort_players_by_card_value(self._players)
        
        for player in sorted_players:
            played_card = player.play_selected_card()
            
            if self._table.must_wipe_row(played_card):
                row_index, wiped_cards = self._process_forced_wipe(player, played_card)
            else:
                row_index, wiped_cards = self._table.place_card(played_card)
            
            penalty_points = 0
            if wiped_cards:
                penalty_points = GameRules.calculate_penalty_points(wiped_cards)
                player.add_penalty_points(penalty_points)
            
            self._turn_results.append((player, played_card, row_index, wiped_cards))
        
        return self._turn_results.copy()
    
    def _process_forced_wipe(self, player: Player, card: Card) -> Tuple[int, List[Card]]:
        """Handle when player must choose a row to wipe.
        
        Args:
            player: Player forced to wipe
            card: Card being played
            
        Returns:
            Tuple of (row_index, wiped_cards)
        """
        row_choices = self._table.get_row_choices()
        
        if hasattr(player, '_forced_row_choice'):
            row_choice = getattr(player, '_forced_row_choice')
            delattr(player, '_forced_row_choice')
        else:
            row_choice = self._get_row_choice_for_player(player, row_choices)
        
        return self._table.place_card(card, forced_row=row_choice)
    
    def _get_row_choice_for_player(self, player: Player, choices: List[int]) -> int:
        """Get row choice from player (to be overridden by UI layer).
        
        Args:
            player: Player making choice
            choices: Available row indices
            
        Returns:
            Selected row index
        """
        return min(choices)
    
    def set_forced_row_choice(self, player: Player, row_index: int) -> None:
        """Set the row choice for a player who must wipe a row.
        
        Args:
            player: Player making choice
            row_index: Row index (0-3) to wipe
            
        Raises:
            ValueError: If row index is invalid
        """
        if not 0 <= row_index < GameRules.STARTING_ROWS:
            raise ValueError(f"Row index must be 0-{GameRules.STARTING_ROWS-1}")
        setattr(player, '_forced_row_choice', row_index)
    
    def is_round_over(self) -> bool:
        """Check if current round is finished.
        
        Returns:
            True if all players have empty hands
        """
        return GameRules.is_round_over(self._players)
    
    def check_game_end(self) -> bool:
        """Check if game should end and set winner.
        
        Returns:
            True if game has ended
        """
        if GameRules.is_game_over(self._players):
            self._state.is_game_over = True
            self._state.winner = GameRules.find_winner(self._players)
            return True
        return False
    
    def get_scores(self) -> List[Tuple[str, int, int]]:
        """Get current scores for all players.
        
        Returns:
            List of (name, round_score, total_score) tuples
        """
        return [(p.name, p.round_score, p.total_score) for p in self._players]
    
    def get_player_by_name(self, name: str) -> Optional[Player]:
        """Find player by name.
        
        Args:
            name: Player name to search for
            
        Returns:
            Player with matching name or None
        """
        for player in self._players:
            if player.name == name:
                return player
        return None
    
    def clear_all_selections(self) -> None:
        """Clear all player card selections."""
        for player in self._players:
            player.clear_selection()
    
    def get_players_needing_row_choice(self) -> List[Tuple[Player, Card]]:
        """Get players who need to choose a row to wipe.
        
        Returns:
            List of (player, card) tuples for players who must wipe
        """
        needing_choice = []
        sorted_players = GameRules.sort_players_by_card_value(self._players)
        
        temp_table = Table([row.cards[0] for row in self._table.rows])
        for row_idx, row in enumerate(self._table.rows):
            for card in row.cards[1:]:
                temp_table.get_row(row_idx)._cards.append(card)
        
        for player in sorted_players:
            if player.has_selected_card:
                if temp_table.must_wipe_row(player.selected_card):
                    needing_choice.append((player, player.selected_card))
                    # Player wipes a row, so update temp table for next check
                    # For simplicity, we'll just use row 0 as placeholder
                    temp_table.get_row(0)._cards = [player.selected_card]
                else:
                    # Place card normally on temp table
                    temp_table.place_card(player.selected_card)
        
        return needing_choice
