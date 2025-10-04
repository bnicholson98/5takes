"""Unit tests for Game and GameState classes."""

import pytest
from game.game import Game, GameState
from game.card import Card
from game.player import Player


class TestGameState:
    """Tests for GameState class."""
    
    def test_game_state_initialization(self):
        """Test GameState initial values."""
        state = GameState()
        
        assert state.round_number == 0
        assert state.turn_number == 0
        assert state.is_game_over == False
        assert state.winner is None


class TestGame:
    """Tests for Game class."""
    
    def test_game_creation_valid(self):
        """Test creating game with valid players."""
        game = Game(["Alice", "Bob", "Charlie"])
        
        assert len(game.players) == 3
        assert game.players[0].name == "Alice"
        assert game.players[1].name == "Bob"
        assert game.players[2].name == "Charlie"
        assert game.table is None  # No round started
        assert game.state.round_number == 0
    
    def test_game_creation_invalid_count(self):
        """Test creating game with invalid player count."""
        with pytest.raises(ValueError):
            Game(["Alice", "Bob"])  # Too few
        
        with pytest.raises(ValueError):
            Game(["P1", "P2", "P3", "P4", "P5", "P6", "P7", "P8", "P9", "P10", "P11"])  # Too many
    
    def test_game_creation_duplicate_names(self):
        """Test creating game with duplicate names."""
        with pytest.raises(ValueError):
            Game(["Alice", "Bob", "Alice"])
    
    def test_start_new_round(self):
        """Test starting a new round."""
        game = Game(["Alice", "Bob", "Charlie"])
        
        game.start_new_round()
        
        assert game.state.round_number == 1
        assert game.state.turn_number == 0
        assert game.table is not None
        assert len(game.table.rows) == 4
        
        # Each player should have 10 cards
        for player in game.players:
            assert player.hand_size == 10
    
    def test_select_card_for_player(self):
        """Test selecting a card for a player."""
        game = Game(["Alice", "Bob", "Charlie"])
        game.start_new_round()
        
        player = game.players[0]
        card = player.hand[0]
        
        game.select_card_for_player(player, card)
        
        assert player.selected_card == card
        assert player.has_selected_card
    
    def test_select_card_invalid(self):
        """Test selecting invalid card."""
        game = Game(["Alice", "Bob", "Charlie"])
        game.start_new_round()
        
        player = game.players[0]
        # Find a card definitely not in hand by checking all values
        hand_values = set(card.value for card in player.hand)
        invalid_value = None
        for value in range(1, 105):
            if value not in hand_values:
                invalid_value = value
                break
        
        if invalid_value:
            invalid_card = Card(invalid_value)
            with pytest.raises(ValueError):
                game.select_card_for_player(player, invalid_card)
    
    def test_all_players_selected(self):
        """Test checking if all players have selected."""
        game = Game(["Alice", "Bob", "Charlie"])
        game.start_new_round()
        
        assert not game.all_players_selected()
        
        # Select cards for all players
        for player in game.players:
            card = player.hand[0]
            game.select_card_for_player(player, card)
        
        assert game.all_players_selected()
    
    def test_process_turn(self):
        """Test processing a complete turn."""
        game = Game(["Alice", "Bob", "Charlie"])
        game.start_new_round()
        
        # Select cards for all players
        for i, player in enumerate(game.players):
            card = player.hand[i]  # Different cards
            game.select_card_for_player(player, card)
        
        results = game.process_turn()
        
        assert len(results) == 3
        assert game.state.turn_number == 1
        
        # Cards should be played
        for player in game.players:
            assert not player.has_selected_card
            assert player.hand_size == 9  # One card played
    
    def test_process_turn_without_selections(self):
        """Test processing turn without all selections."""
        game = Game(["Alice", "Bob", "Charlie"])
        game.start_new_round()
        
        # Only select for one player
        game.select_card_for_player(game.players[0], game.players[0].hand[0])
        
        with pytest.raises(ValueError):
            game.process_turn()
    
    def test_is_round_over(self):
        """Test checking if round is over."""
        game = Game(["Alice", "Bob", "Charlie"])
        game.start_new_round()
        
        assert not game.is_round_over()
        
        # Play all 10 turns
        for turn in range(10):
            for player in game.players:
                if player.hand_size > 0:
                    card = player.hand[0]
                    game.select_card_for_player(player, card)
            
            if game.all_players_selected():
                game.process_turn()
        
        assert game.is_round_over()
    
    def test_check_game_end(self):
        """Test checking and setting game end."""
        game = Game(["Alice", "Bob", "Charlie"])
        game.start_new_round()
        
        # Give one player >50 points
        game.players[0].add_penalty_points(51)
        
        assert game.check_game_end()
        assert game.state.is_game_over
        assert game.state.winner is not None
        assert game.state.winner.name == "Bob" or game.state.winner.name == "Charlie"  # Lowest score
    
    def test_get_scores(self):
        """Test getting player scores."""
        game = Game(["Alice", "Bob", "Charlie"])
        
        game.players[0].add_penalty_points(10)
        game.players[1].add_penalty_points(20)
        game.players[2].add_penalty_points(15)
        
        scores = game.get_scores()
        
        assert len(scores) == 3
        assert scores[0] == ("Alice", 10, 10)
        assert scores[1] == ("Bob", 20, 20)
        assert scores[2] == ("Charlie", 15, 15)
    
    def test_get_player_by_name(self):
        """Test finding player by name."""
        game = Game(["Alice", "Bob", "Charlie"])
        
        player = game.get_player_by_name("Bob")
        assert player is not None
        assert player.name == "Bob"
        
        player = game.get_player_by_name("David")
        assert player is None
    
    def test_clear_all_selections(self):
        """Test clearing all player selections."""
        game = Game(["Alice", "Bob", "Charlie"])
        game.start_new_round()
        
        # Select cards for all players
        for player in game.players:
            card = player.hand[0]
            game.select_card_for_player(player, card)
        
        game.clear_all_selections()
        
        for player in game.players:
            assert not player.has_selected_card
            assert player.selected_card is None
    
    def test_set_forced_row_choice(self):
        """Test setting forced row choice for player."""
        game = Game(["Alice", "Bob", "Charlie"])
        game.start_new_round()
        
        player = game.players[0]
        
        game.set_forced_row_choice(player, 2)
        assert hasattr(player, '_forced_row_choice')
        assert player._forced_row_choice == 2
    
    def test_set_forced_row_choice_invalid(self):
        """Test setting invalid forced row choice."""
        game = Game(["Alice", "Bob", "Charlie"])
        game.start_new_round()
        
        player = game.players[0]
        
        with pytest.raises(ValueError):
            game.set_forced_row_choice(player, -1)
        
        with pytest.raises(ValueError):
            game.set_forced_row_choice(player, 4)
    
    def test_get_players_needing_row_choice(self):
        """Test identifying players who must wipe rows."""
        game = Game(["Alice", "Bob", "Charlie"])
        game.start_new_round()
        
        # Find a card that's lower than all table cards
        lowest_table_card = min(row.last_card.value for row in game.table.rows)
        
        # Give players cards - one needs to wipe
        for player in game.players:
            # Find a low card in their hand
            for card in player.hand:
                if card.value < lowest_table_card:
                    game.select_card_for_player(player, card)
                    break
            else:
                # No low card, select any
                game.select_card_for_player(player, player.hand[0])
        
        needing_choice = game.get_players_needing_row_choice()
        
        # Should return list of (player, card) tuples
        assert isinstance(needing_choice, list)
        for item in needing_choice:
            assert len(item) == 2
            assert isinstance(item[0], Player)
            assert isinstance(item[1], Card)
