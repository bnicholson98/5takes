"""Unit tests for GameRules class."""

import pytest
from game.rules import GameRules
from game.player import Player
from game.card import Card


class TestGameRules:
    """Tests for GameRules class."""
    
    def test_validate_player_count_valid(self):
        """Test valid player counts."""
        GameRules.validate_player_count(3)
        GameRules.validate_player_count(5)
        GameRules.validate_player_count(10)
        # Should not raise any exceptions
    
    def test_validate_player_count_invalid(self):
        """Test invalid player counts."""
        with pytest.raises(ValueError):
            GameRules.validate_player_count(2)
        with pytest.raises(ValueError):
            GameRules.validate_player_count(11)
        with pytest.raises(ValueError):
            GameRules.validate_player_count(0)
        with pytest.raises(ValueError):
            GameRules.validate_player_count(-1)
    
    def test_validate_player_names_valid(self):
        """Test valid player name lists."""
        GameRules.validate_player_names(["Alice", "Bob", "Charlie"])
        GameRules.validate_player_names(["Player1"])
        # Should not raise any exceptions
    
    def test_validate_player_names_empty_list(self):
        """Test empty player list."""
        with pytest.raises(ValueError):
            GameRules.validate_player_names([])
    
    def test_validate_player_names_empty_string(self):
        """Test empty player names."""
        with pytest.raises(ValueError):
            GameRules.validate_player_names(["Alice", "", "Charlie"])
        with pytest.raises(ValueError):
            GameRules.validate_player_names(["   "])
    
    def test_validate_player_names_duplicates(self):
        """Test duplicate player names."""
        with pytest.raises(ValueError):
            GameRules.validate_player_names(["Alice", "Bob", "Alice"])
        # Case-sensitive names are considered different
        GameRules.validate_player_names(["Alice", "alice"])  # Should pass
    
    def test_validate_player_names_whitespace_handling(self):
        """Test names with whitespace are considered duplicates."""
        with pytest.raises(ValueError):
            GameRules.validate_player_names(["Alice", "  Alice  "])
    
    def test_calculate_cards_needed(self):
        """Test calculating cards needed for game."""
        assert GameRules.calculate_cards_needed(3) == 34  # 3*10 + 4
        assert GameRules.calculate_cards_needed(5) == 54  # 5*10 + 4
        assert GameRules.calculate_cards_needed(10) == 104  # 10*10 + 4
    
    def test_is_game_over(self):
        """Test checking if game is over."""
        players = [
            Player("Alice"),
            Player("Bob"),
            Player("Charlie")
        ]
        
        # No one over threshold
        players[0].add_penalty_points(30)
        players[1].add_penalty_points(40)
        players[2].add_penalty_points(50)
        assert not GameRules.is_game_over(players)
        
        # One player over threshold
        players[0].add_penalty_points(21)  # Total 51
        assert GameRules.is_game_over(players)
    
    def test_find_winner(self):
        """Test finding winner with lowest score."""
        players = [
            Player("Alice"),
            Player("Bob"),
            Player("Charlie")
        ]
        
        players[0].add_penalty_points(30)
        players[1].add_penalty_points(20)  # Lowest
        players[2].add_penalty_points(40)
        
        winner = GameRules.find_winner(players)
        assert winner.name == "Bob"
    
    def test_find_winner_empty_list(self):
        """Test finding winner with no players."""
        with pytest.raises(ValueError):
            GameRules.find_winner([])
    
    def test_is_round_over(self):
        """Test checking if round is over."""
        players = [
            Player("Alice"),
            Player("Bob")
        ]
        
        # Players have cards
        players[0].deal_cards([Card(10), Card(20)])
        players[1].deal_cards([Card(30), Card(40)])
        assert not GameRules.is_round_over(players)
        
        # Play all cards
        players[0].select_card(Card(10))
        players[0].play_selected_card()
        players[0].select_card(Card(20))
        players[0].play_selected_card()
        
        players[1].select_card(Card(30))
        players[1].play_selected_card()
        players[1].select_card(Card(40))
        players[1].play_selected_card()
        
        assert GameRules.is_round_over(players)
    
    def test_all_players_selected(self):
        """Test checking if all players have selected cards."""
        players = [
            Player("Alice"),
            Player("Bob")
        ]
        
        cards = [Card(10), Card(20), Card(30), Card(40)]
        players[0].deal_cards(cards[:2])
        players[1].deal_cards(cards[2:])
        
        # No selections
        assert not GameRules.all_players_selected(players)
        
        # One player selected
        players[0].select_card(Card(10))
        assert not GameRules.all_players_selected(players)
        
        # All selected
        players[1].select_card(Card(30))
        assert GameRules.all_players_selected(players)
    
    def test_calculate_penalty_points(self):
        """Test calculating total penalty points."""
        cards = [
            Card(1),   # 1 point
            Card(5),   # 2 points
            Card(10),  # 3 points
            Card(11),  # 5 points
            Card(55)   # 7 points
        ]
        
        assert GameRules.calculate_penalty_points(cards) == 18
        assert GameRules.calculate_penalty_points([]) == 0
    
    def test_sort_players_by_card_value(self):
        """Test sorting players by selected card values."""
        players = [
            Player("Alice"),
            Player("Bob"),
            Player("Charlie")
        ]
        
        players[0].deal_cards([Card(50)])
        players[1].deal_cards([Card(10)])
        players[2].deal_cards([Card(30)])
        
        players[0].select_card(Card(50))
        players[1].select_card(Card(10))
        players[2].select_card(Card(30))
        
        sorted_players = GameRules.sort_players_by_card_value(players)
        
        assert sorted_players[0].name == "Bob"  # Card 10
        assert sorted_players[1].name == "Charlie"  # Card 30
        assert sorted_players[2].name == "Alice"  # Card 50
    
    def test_validate_card_selection_valid(self):
        """Test valid card selection."""
        player = Player("Alice")
        card = Card(10)
        player.deal_cards([card])
        
        GameRules.validate_card_selection(player, card)
        # Should not raise exception
    
    def test_validate_card_selection_not_in_hand(self):
        """Test selecting card not in hand."""
        player = Player("Alice")
        player.deal_cards([Card(10)])
        
        with pytest.raises(ValueError):
            GameRules.validate_card_selection(player, Card(20))
    
    def test_validate_card_selection_already_selected(self):
        """Test selecting when already selected."""
        player = Player("Alice")
        card1 = Card(10)
        card2 = Card(20)
        player.deal_cards([card1, card2])
        player.select_card(card1)
        
        with pytest.raises(ValueError):
            GameRules.validate_card_selection(player, card2)
