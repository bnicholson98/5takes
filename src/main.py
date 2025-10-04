"""Main entry point for 5 Takes game."""

from typing import List, Optional
from game.game import Game
from game.player import Player
from ui.input import InputHandler
from ui.display import GameDisplay
from ui.colors import colors


class GameController:
    """Main game controller handling the game flow."""
    
    def __init__(self):
        """Initialize game controller."""
        self._game: Optional[Game] = None
    
    def run(self) -> None:
        """Main game loop."""
        GameDisplay.show_title()
        GameDisplay.show_message("Welcome to 5 Takes!", "info")
        GameDisplay.wait_for_enter()
        
        while True:
            self._play_game()
            
            if not InputHandler.confirm_play_again():
                break
        
        GameDisplay.show_message("Thanks for playing!", "success")
    
    def _play_game(self) -> None:
        """Play a complete game until someone exceeds 50 points."""
        player_names = InputHandler.get_player_names()
        self._game = Game(player_names)
        
        while not self._game.state.is_game_over:
            self._play_round()
            
            if not self._game.check_game_end():
                InputHandler.show_round_end(
                    self._game.players, 
                    self._game.state.round_number
                )
        
        GameDisplay.show_game_over(
            self._game.state.winner,
            self._game.get_scores()
        )
    
    def _play_round(self) -> None:
        """Play a complete round (10 turns)."""
        self._game.start_new_round()
        
        InputHandler.show_round_start(self._game.state.round_number)
        
        while not self._game.is_round_over():
            self._play_turn()
    
    def _play_turn(self) -> None:
        """Play a single turn with all players selecting cards."""
        InputHandler.show_turn_start(
            self._game.state.round_number,
            self._game.state.turn_number + 1
        )
        
        self._collect_card_selections()
        
        self._handle_forced_row_choices()
        
        results = self._game.process_turn()
        
        InputHandler.show_turn_results(results, self._game.table)
    
    def _collect_card_selections(self) -> None:
        """Collect card selections from all players with privacy handling."""
        for player in self._game.players:
            GameDisplay.show_pass_device_prompt(player.name)
            
            selected_card = InputHandler.get_card_selection(
                player, 
                self._game.table,
                self._game.state.round_number,
                self._game.state.turn_number + 1
            )
            
            self._game.select_card_for_player(player, selected_card)
            
            colors.clear_screen()
            GameDisplay.show_message(f"{player.name} has selected their card.", "success")
            GameDisplay.wait_for_enter("Press Enter to continue...")
    
    def _handle_forced_row_choices(self) -> None:
        """Handle players who need to choose rows to wipe.
        
        Processes players whose cards are too low for any row.
        """
        players_needing_choice = self._game.get_players_needing_row_choice()
        
        # Get all selections for display
        all_selections = [(p.name, p.selected_card) 
                         for p in self._game.players 
                         if p.has_selected_card]
        
        for player, card in players_needing_choice:
            GameDisplay.show_pass_device_prompt(player.name)
            
            row_choice = InputHandler.get_row_choice(player, self._game.table, all_selections)
            self._game.set_forced_row_choice(player, row_choice)
            
            colors.clear_screen()
            GameDisplay.show_message(f"{player.name} has chosen their row.", "success")
            GameDisplay.wait_for_enter("Press Enter to continue...")


def main() -> None:
    """Main function to start the game.
    
    Entry point that handles initialization and error handling.
    """
    try:
        controller = GameController()
        controller.run()
    except KeyboardInterrupt:
        colors.clear_screen()
        print(colors.colored_text("\n\nThanks for playing 5 Takes!", colors.SUCCESS))
        print(colors.colored_text("Game ended by user.", colors.INFO))
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
