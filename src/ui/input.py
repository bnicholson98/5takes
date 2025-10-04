"""User input handling for 5 Takes game."""

from typing import List, Optional, Tuple
import sys
import os

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from game.player import Player
from game.card import Card
from game.table import Table
from .display import GameDisplay
from .colors import colors


class InputHandler:
    """Handles all user input with validation."""
    
    @staticmethod
    def get_player_names() -> List[str]:
        """Get player names from user input.
        
        Returns:
            List of unique player names (3-10 players)
        """
        GameDisplay.show_title()
        
        while True:
            try:
                count_input = GameDisplay.prompt_for_input(
                    "Enter number of players (3-10): "
                )
                player_count = int(count_input.strip())
                
                if not 3 <= player_count <= 10:
                    GameDisplay.show_message("Number of players must be between 3 and 10", "error")
                    continue
                    
                break
                
            except ValueError:
                GameDisplay.show_message("Please enter a valid number", "error")
        
        print()
        names = []
        for i in range(player_count):
            while True:
                name = GameDisplay.prompt_for_input(f"Enter name for Player {i+1}: ").strip()
                
                if not name:
                    GameDisplay.show_message("Name cannot be empty", "error")
                    continue
                
                if name in names:
                    GameDisplay.show_message("Name already taken", "error")
                    continue
                
                names.append(name)
                break
        
        return names
    
    @staticmethod
    def get_card_selection(player: Player, table: Table) -> Card:
        """Get card selection from player.
        
        Args:
            player: Player making selection
            table: Current table state for display
            
        Returns:
            Selected card from player's hand
        """
        colors.clear_screen()
        GameDisplay.show_round_header(0)  # Will be updated by caller
        GameDisplay.show_table(table)
        GameDisplay.show_player_hand(player, show_indices=True)
        
        while True:
            try:
                selection = GameDisplay.prompt_for_input(
                    f"Select a card (1-{player.hand_size}): "
                )
                
                index = int(selection.strip()) - 1
                
                if not 0 <= index < player.hand_size:
                    GameDisplay.show_message(
                        f"Please enter a number between 1 and {player.hand_size}", 
                        "error"
                    )
                    continue
                
                selected_card = player.get_card_by_index(index)
                
                confirm = GameDisplay.prompt_for_input(
                    f"Play {colors.colored_card(selected_card.value, selected_card.points)}? (y/n): "
                ).strip().lower()
                
                if confirm in ['y', 'yes']:
                    return selected_card
                
            except ValueError:
                GameDisplay.show_message("Please enter a valid number", "error")
            except (IndexError, KeyError):
                GameDisplay.show_message("Invalid selection", "error")
    
    @staticmethod
    def get_row_choice(player: Player, table: Table) -> int:
        """Get row choice when player must wipe a row.
        
        Args:
            player: Player who must choose
            table: Table with rows to choose from
            
        Returns:
            Zero-based row index (0-3)
        """
        colors.clear_screen()
        GameDisplay.show_message(
            f"{player.name}: Your card is too low for all rows!", 
            "warning"
        )
        GameDisplay.show_table(table)
        GameDisplay.show_row_choices(table)
        
        while True:
            try:
                choice = GameDisplay.prompt_for_input("Choose row to take (1-4): ")
                row_index = int(choice.strip()) - 1
                
                if not 0 <= row_index < 4:
                    GameDisplay.show_message("Please enter 1, 2, 3, or 4", "error")
                    continue
                
                return row_index
                
            except ValueError:
                GameDisplay.show_message("Please enter a valid number", "error")
    
    @staticmethod
    def confirm_play_again() -> bool:
        """Ask if players want to play another game.
        
        Returns:
            True if players want another game
        """
        while True:
            choice = GameDisplay.prompt_for_input("Play another game? (y/n): ").strip().lower()
            
            if choice in ['y', 'yes']:
                return True
            elif choice in ['n', 'no']:
                return False
            else:
                GameDisplay.show_message("Please enter 'y' for yes or 'n' for no", "error")
    
    @staticmethod
    def show_round_start(round_num: int) -> None:
        """Show round start screen.
        
        Args:
            round_num: Round number starting
        """
        colors.clear_screen()
        GameDisplay.show_title()
        GameDisplay.show_message(f"Starting Round {round_num}...", "info")
        GameDisplay.wait_for_enter()
    
    @staticmethod
    def show_turn_start(round_num: int, turn_num: int) -> None:
        """Show turn start information.
        
        Args:
            round_num: Current round number
            turn_num: Current turn number
        """
        colors.clear_screen()
        GameDisplay.show_round_header(round_num, turn_num)
    
    @staticmethod
    def show_turn_results(results: List[Tuple[Player, Card, int, Optional[List[Card]]]], table: Table) -> None:
        """Display turn results and wait for confirmation.
        
        Args:
            results: List of (player, card, row_index, wiped_cards) tuples
            table: Updated table state
        """
        colors.clear_screen()
        GameDisplay.show_turn_results(results)
        GameDisplay.show_table(table)
        GameDisplay.wait_for_enter()
    
    @staticmethod
    def show_round_end(players: List[Player], round_num: int) -> None:
        """Show round end scores.
        
        Args:
            players: List of players with updated scores
            round_num: Round number that just ended
        """
        colors.clear_screen()
        GameDisplay.show_message(f"Round {round_num} Complete!", "success")
        GameDisplay.show_scores(players, show_round_scores=True)
        GameDisplay.wait_for_enter()
