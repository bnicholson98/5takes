"""Terminal display formatting for 5 Takes game."""

from typing import List, Optional, Tuple
import sys
import os

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from game.player import Player
from game.table import Table
from game.card import Card
from .colors import colors


class GameDisplay:
    """Handles all game display formatting."""
    
    @staticmethod
    def show_title() -> None:
        """Display game title."""
        colors.clear_screen()
        colors.print_separator()
        colors.print_centered(colors.colored_text("5 TAKES", colors.HEADER))
        colors.print_separator()
        print()
    
    @staticmethod
    def show_round_header(round_num: int, turn_num: int = 0) -> None:
        """Display round and turn information."""
        if turn_num > 0:
            header = f"Round {round_num} - Turn {turn_num}"
        else:
            header = f"Round {round_num}"
        colors.print_centered(colors.colored_text(header, colors.INFO))
        colors.print_separator()
        print()
    
    @staticmethod
    def show_table(table: Table) -> None:
        """Display current table state."""
        print(colors.colored_text("Table:", colors.HEADER))
        for i, row in enumerate(table.rows):
            row_text = f"Row {i+1}: "
            card_texts = []
            for card in row.cards:
                card_texts.append(colors.colored_card(card.value, card.points))
            print(f"{colors.colored_text(row_text, colors.TABLE_ROW)}{' '.join(card_texts)}")
        print()
    
    @staticmethod
    def show_player_hand(player: Player, show_indices: bool = True) -> None:
        """Display player's hand with optional indices."""
        print(colors.colored_text(f"{player.name}'s Hand:", colors.PLAYER_NAME))
        
        hand = player.hand
        if not hand:
            print("No cards in hand")
            return
        
        cards_per_line = 5
        for i in range(0, len(hand), cards_per_line):
            line_cards = hand[i:i + cards_per_line]
            
            if show_indices:
                indices = [f"{j+1:2d}." for j in range(i, i + len(line_cards))]
                print("  " + "     ".join(indices))
            
            card_displays = []
            for card in line_cards:
                card_displays.append(colors.colored_card(card.value, card.points))
            print("  " + "  ".join(card_displays))
            
            if show_indices:
                points = [f"({card.points} pt{'s' if card.points != 1 else ''})" for card in line_cards]
                print("  " + "  ".join(f"{p:>6s}" for p in points))
            
            if i + cards_per_line < len(hand):
                print()
        print()
    
    @staticmethod
    def show_scores(players: List[Player], show_round_scores: bool = False) -> None:
        """Display player scores."""
        print(colors.colored_text("Scores:", colors.HEADER))
        
        for player in players:
            name_part = colors.colored_text(f"{player.name:15s}", colors.PLAYER_NAME)
            
            if show_round_scores and player.round_score > 0:
                score_part = colors.colored_text(
                    f"Round: {player.round_score:2d} | Total: {player.total_score:2d}",
                    colors.SCORE
                )
            else:
                score_part = colors.colored_text(f"Total: {player.total_score:2d}", colors.SCORE)
            
            print(f"  {name_part} {score_part}")
        print()
    
    @staticmethod
    def show_turn_results(results: List[Tuple[Player, Card, int, Optional[List[Card]]]]) -> None:
        """Display results of a turn."""
        print(colors.colored_text("Turn Results:", colors.HEADER))
        
        for player, card, row_index, wiped_cards in results:
            card_text = colors.colored_card(card.value, card.points)
            row_text = f"Row {row_index + 1}"
            
            if wiped_cards:
                penalty_points = sum(c.points for c in wiped_cards)
                penalty_text = colors.colored_text(f"(+{penalty_points} points)", colors.ERROR)
                print(f"  {colors.colored_text(player.name, colors.PLAYER_NAME)}: "
                      f"{card_text} → {row_text} {penalty_text}")
            else:
                print(f"  {colors.colored_text(player.name, colors.PLAYER_NAME)}: "
                      f"{card_text} → {row_text}")
        print()
    
    @staticmethod
    def show_card_selections(players: List[Player]) -> None:
        """Display all players' selected cards."""
        print(colors.colored_text("Selected Cards:", colors.HEADER))
        
        selected_players = [(p, p.selected_card) for p in players if p.has_selected_card]
        selected_players.sort(key=lambda x: x[1].value)
        
        for player, card in selected_players:
            card_text = colors.colored_card(card.value, card.points)
            print(f"  {colors.colored_text(player.name, colors.PLAYER_NAME)}: {card_text}")
        print()
    
    @staticmethod
    def show_row_choices(table: Table) -> None:
        """Display rows for selection when wiping."""
        print(colors.colored_text("Choose a row to take:", colors.WARNING))
        
        for i, row in enumerate(table.rows):
            points = row.total_points
            cards_text = " ".join(colors.colored_card(card.value, card.points) for card in row.cards)
            point_text = colors.colored_text(f"({points} point{'s' if points != 1 else ''})", colors.ERROR)
            print(f"  {i+1}. {cards_text} {point_text}")
        print()
    
    @staticmethod
    def show_game_over(winner: Player, final_scores: List[Tuple[str, int, int]]) -> None:
        """Display game over screen with winner and final scores."""
        colors.clear_screen()
        colors.print_separator()
        colors.print_centered(colors.colored_text("GAME OVER", colors.HEADER))
        colors.print_separator()
        print()
        
        print(colors.colored_text(f"🎉 {winner.name} wins with {winner.total_score} points! 🎉", colors.SUCCESS))
        print()
        
        print(colors.colored_text("Final Scores:", colors.HEADER))
        sorted_scores = sorted(final_scores, key=lambda x: x[2])
        
        for i, (name, round_score, total_score) in enumerate(sorted_scores):
            position = f"{i+1}."
            name_part = colors.colored_text(f"{name:15s}", colors.PLAYER_NAME)
            score_part = colors.colored_text(f"{total_score:2d} points", colors.SCORE)
            print(f"  {position:3s} {name_part} {score_part}")
    
    @staticmethod
    def prompt_for_input(message: str) -> str:
        """Display input prompt with consistent formatting."""
        return input(colors.colored_text(message, colors.PROMPT))
    
    @staticmethod
    def show_message(message: str, message_type: str = "info") -> None:
        """Display a message with appropriate color."""
        color_map = {
            "info": colors.INFO,
            "success": colors.SUCCESS,
            "warning": colors.WARNING,
            "error": colors.ERROR
        }
        color = color_map.get(message_type, colors.INFO)
        print(colors.colored_text(message, color))
        print()
    
    @staticmethod
    def wait_for_enter(message: str = "Press Enter to continue...") -> None:
        """Wait for user to press Enter."""
        input(colors.colored_text(message, colors.PROMPT))
        print()
    
    @staticmethod
    def show_pass_device_prompt(player_name: str) -> None:
        """Display prompt to pass device to next player."""
        colors.clear_screen()
        colors.print_separator()
        colors.print_centered(f"Pass device to {player_name}")
        colors.print_separator()
        print()
        GameDisplay.wait_for_enter("Press Enter when ready...")
