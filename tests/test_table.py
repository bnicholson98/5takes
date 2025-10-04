"""Unit tests for Table and Row classes."""

import pytest
from game.table import Table, Row
from game.card import Card


class TestRow:
    """Tests for Row class."""
    
    def test_row_creation(self):
        """Test creating row with starting card."""
        card = Card(50)
        row = Row(card)
        
        assert row.cards == [card]
        assert row.last_card == card
        assert row.card_count == 1
        assert not row.is_full
    
    def test_row_can_place_card(self):
        """Test checking if card can be placed."""
        row = Row(Card(20))
        
        assert row.can_place_card(Card(21))
        assert row.can_place_card(Card(100))
        assert not row.can_place_card(Card(20))  # Same value
        assert not row.can_place_card(Card(19))  # Lower value
    
    def test_row_place_card_valid(self):
        """Test placing valid cards in row."""
        row = Row(Card(20))
        
        result = row.place_card(Card(30))
        assert result is None  # No cards wiped
        assert row.card_count == 2
        assert row.last_card.value == 30
    
    def test_row_place_card_invalid(self):
        """Test placing invalid card raises error."""
        row = Row(Card(20))
        
        with pytest.raises(ValueError):
            row.place_card(Card(10))
    
    def test_row_full_after_five_cards(self):
        """Test row becomes full with 5 cards."""
        row = Row(Card(10))
        
        row.place_card(Card(20))
        row.place_card(Card(30))
        row.place_card(Card(40))
        assert not row.is_full
        
        wiped = row.place_card(Card(50))
        assert not row.is_full  # After wiping, only 1 card left
        assert wiped is not None
        assert len(wiped) == 4
        assert row.card_count == 1
        assert row.last_card.value == 50
    
    def test_row_wipe_and_replace(self):
        """Test wiping row and replacing with new card."""
        row = Row(Card(10))
        row.place_card(Card(20))
        row.place_card(Card(30))
        
        wiped = row.wipe_and_replace(Card(5))
        
        assert len(wiped) == 3
        assert wiped[0].value == 10
        assert wiped[1].value == 20
        assert wiped[2].value == 30
        assert row.card_count == 1
        assert row.last_card.value == 5
    
    def test_row_total_points(self):
        """Test calculating total points in row."""
        row = Row(Card(10))  # 3 points
        row.place_card(Card(55))  # 7 points
        row.place_card(Card(77))  # 5 points (must be higher than 55)
        
        assert row.total_points == 15
    
    def test_row_string_representation(self):
        """Test row string representation."""
        row = Row(Card(10))
        row.place_card(Card(20))
        
        assert str(row) == "[10] [20]"


class TestTable:
    """Tests for Table class."""
    
    def test_table_creation_valid(self):
        """Test creating table with 4 starting cards."""
        cards = [Card(10), Card(20), Card(30), Card(40)]
        table = Table(cards)
        
        assert len(table.rows) == 4
        for i, row in enumerate(table.rows):
            assert row.last_card.value == cards[i].value
    
    def test_table_creation_invalid(self):
        """Test table creation with wrong number of cards."""
        with pytest.raises(ValueError):
            Table([Card(10), Card(20), Card(30)])
        
        with pytest.raises(ValueError):
            Table([Card(10), Card(20), Card(30), Card(40), Card(50)])
    
    def test_get_row_valid(self):
        """Test getting specific row by index."""
        cards = [Card(10), Card(20), Card(30), Card(40)]
        table = Table(cards)
        
        assert table.get_row(0).last_card.value == 10
        assert table.get_row(3).last_card.value == 40
    
    def test_get_row_invalid(self):
        """Test getting row with invalid index."""
        table = Table([Card(10), Card(20), Card(30), Card(40)])
        
        with pytest.raises(IndexError):
            table.get_row(-1)
        with pytest.raises(IndexError):
            table.get_row(4)
    
    def test_find_target_row(self):
        """Test finding best row for card placement."""
        table = Table([Card(10), Card(20), Card(30), Card(40)])
        
        # Card 25 should go after 20 (smallest gap)
        assert table.find_target_row(Card(25)) == 1
        
        # Card 45 should go after 40
        assert table.find_target_row(Card(45)) == 3
        
        # Card 5 can't be placed
        assert table.find_target_row(Card(5)) is None
    
    def test_must_wipe_row(self):
        """Test checking if card forces row wipe."""
        table = Table([Card(10), Card(20), Card(30), Card(40)])
        
        assert table.must_wipe_row(Card(5))  # Lower than all
        assert not table.must_wipe_row(Card(15))  # Can be placed
    
    def test_place_card_normal(self):
        """Test normal card placement."""
        table = Table([Card(10), Card(20), Card(30), Card(40)])
        
        row_idx, wiped = table.place_card(Card(25))
        
        assert row_idx == 1
        assert wiped is None
        assert table.get_row(1).card_count == 2
    
    def test_place_card_forced_row(self):
        """Test forced row placement (wipe)."""
        table = Table([Card(10), Card(20), Card(30), Card(40)])
        
        row_idx, wiped = table.place_card(Card(5), forced_row=2)
        
        assert row_idx == 2
        assert len(wiped) == 1
        assert wiped[0].value == 30
        assert table.get_row(2).last_card.value == 5
    
    def test_place_card_causes_wipe(self):
        """Test placing 5th card causes wipe."""
        table = Table([Card(10), Card(20), Card(30), Card(40)])
        
        # Fill row 0 to 4 cards
        table.place_card(Card(11))
        table.place_card(Card(12))
        table.place_card(Card(13))
        
        # 5th card should cause wipe
        row_idx, wiped = table.place_card(Card(14))
        
        assert row_idx == 0
        assert len(wiped) == 4
        assert table.get_row(0).card_count == 1
        assert table.get_row(0).last_card.value == 14
    
    def test_place_card_no_valid_row(self):
        """Test placing card with no valid row."""
        table = Table([Card(10), Card(20), Card(30), Card(40)])
        
        with pytest.raises(ValueError):
            table.place_card(Card(5))  # No forced_row specified
    
    def test_get_row_choices(self):
        """Test getting available row indices."""
        table = Table([Card(10), Card(20), Card(30), Card(40)])
        
        choices = table.get_row_choices()
        assert choices == [0, 1, 2, 3]
    
    def test_table_string_representation(self):
        """Test table string representation."""
        table = Table([Card(10), Card(20), Card(30), Card(40)])
        
        output = str(table)
        assert "Row 1: [10]" in output
        assert "Row 2: [20]" in output
        assert "Row 3: [30]" in output
        assert "Row 4: [40]" in output
