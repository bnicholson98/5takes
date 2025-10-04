"""Unit tests for Player class."""

import pytest
from game.player import Player
from game.card import Card


class TestPlayer:
    """Tests for Player class."""
    
    def test_player_creation_valid(self):
        """Test creating player with valid name."""
        player = Player("Alice")
        assert player.name == "Alice"
        assert player.hand_size == 0
        assert player.total_score == 0
        assert player.round_score == 0
        assert player.selected_card is None
    
    def test_player_creation_invalid(self):
        """Test player creation with invalid names."""
        with pytest.raises(ValueError):
            Player("")
        with pytest.raises(ValueError):
            Player("   ")
        with pytest.raises(ValueError):
            Player("\t\n")
    
    def test_player_name_stripped(self):
        """Test that player names are stripped of whitespace."""
        player = Player("  Bob  ")
        assert player.name == "Bob"
    
    def test_deal_cards_to_player(self):
        """Test dealing cards to player's hand."""
        player = Player("Alice")
        cards = [Card(10), Card(20), Card(30)]
        
        player.deal_cards(cards)
        assert player.hand_size == 3
        assert all(card in player.hand for card in cards)
    
    def test_player_hand_sorted(self):
        """Test that player's hand is always sorted."""
        player = Player("Alice")
        cards = [Card(30), Card(10), Card(20)]
        
        player.deal_cards(cards)
        hand_values = [card.value for card in player.hand]
        assert hand_values == [10, 20, 30]
    
    def test_has_card(self):
        """Test checking if player has specific card."""
        player = Player("Alice")
        card1 = Card(10)
        card2 = Card(20)
        card3 = Card(30)
        
        player.deal_cards([card1, card2])
        
        assert player.has_card(card1)
        assert player.has_card(card2)
        assert not player.has_card(card3)
    
    def test_select_card_valid(self):
        """Test selecting a card from hand."""
        player = Player("Alice")
        card = Card(10)
        player.deal_cards([card])
        
        player.select_card(card)
        assert player.selected_card == card
        assert player.has_selected_card
    
    def test_select_card_not_in_hand(self):
        """Test selecting card not in hand raises error."""
        player = Player("Alice")
        card1 = Card(10)
        card2 = Card(20)
        player.deal_cards([card1])
        
        with pytest.raises(ValueError):
            player.select_card(card2)
    
    def test_select_card_already_selected(self):
        """Test selecting when already selected raises error."""
        player = Player("Alice")
        card1 = Card(10)
        card2 = Card(20)
        player.deal_cards([card1, card2])
        
        player.select_card(card1)
        with pytest.raises(ValueError):
            player.select_card(card2)
    
    def test_play_selected_card(self):
        """Test playing the selected card."""
        player = Player("Alice")
        card = Card(10)
        player.deal_cards([card])
        player.select_card(card)
        
        played_card = player.play_selected_card()
        
        assert played_card == card
        assert player.hand_size == 0
        assert player.selected_card is None
        assert not player.has_selected_card
    
    def test_play_without_selection(self):
        """Test playing card without selection raises error."""
        player = Player("Alice")
        
        with pytest.raises(ValueError):
            player.play_selected_card()
    
    def test_add_penalty_points(self):
        """Test adding penalty points to player."""
        player = Player("Alice")
        
        player.add_penalty_points(5)
        assert player.round_score == 5
        assert player.total_score == 5
        
        player.add_penalty_points(3)
        assert player.round_score == 8
        assert player.total_score == 8
    
    def test_add_negative_penalty_points(self):
        """Test that negative penalty points raise error."""
        player = Player("Alice")
        
        with pytest.raises(ValueError):
            player.add_penalty_points(-5)
    
    def test_reset_round_score(self):
        """Test resetting round score."""
        player = Player("Alice")
        player.add_penalty_points(10)
        
        player.reset_round_score()
        assert player.round_score == 0
        assert player.total_score == 10  # Total remains
    
    def test_clear_selection(self):
        """Test clearing card selection."""
        player = Player("Alice")
        card = Card(10)
        player.deal_cards([card])
        player.select_card(card)
        
        player.clear_selection()
        assert player.selected_card is None
        assert not player.has_selected_card
        assert player.has_card(card)  # Card still in hand
    
    def test_get_card_by_index(self):
        """Test getting card from hand by index."""
        player = Player("Alice")
        cards = [Card(10), Card(20), Card(30)]
        player.deal_cards(cards)
        
        assert player.get_card_by_index(0).value == 10
        assert player.get_card_by_index(1).value == 20
        assert player.get_card_by_index(2).value == 30
    
    def test_get_card_invalid_index(self):
        """Test getting card with invalid index."""
        player = Player("Alice")
        cards = [Card(10), Card(20)]
        player.deal_cards(cards)
        
        with pytest.raises(IndexError):
            player.get_card_by_index(-1)
        with pytest.raises(IndexError):
            player.get_card_by_index(2)
    
    def test_player_string_representation(self):
        """Test player string representations."""
        player = Player("Alice")
        player.add_penalty_points(15)
        player.deal_cards([Card(10), Card(20)])
        
        assert str(player) == "Alice (Score: 15)"
        assert repr(player) == "Player('Alice', score=15, hand_size=2)"
