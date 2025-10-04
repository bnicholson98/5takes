"""Pytest configuration and shared fixtures."""

import pytest
import sys
import os

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from game.card import Card, Deck
from game.player import Player
from game.table import Table, Row
from game.game import Game

@pytest.fixture
def sample_cards():
    """Provide sample cards for testing.
    
    Returns:
        List of cards with known values
    """
    return [Card(10), Card(20), Card(55), Card(77), Card(104)]

@pytest.fixture
def sample_deck():
    """Provide a fresh deck for testing.
    
    Returns:
        New shuffled deck
    """
    return Deck()

@pytest.fixture
def sample_player():
    """Provide a sample player for testing.
    
    Returns:
        Player with test name
    """
    return Player("TestPlayer")

@pytest.fixture
def sample_table():
    """Provide a sample table for testing.
    
    Returns:
        Table with 4 starting cards
    """
    starting_cards = [Card(10), Card(25), Card(50), Card(75)]
    return Table(starting_cards)

@pytest.fixture
def sample_game():
    """Provide a sample game for testing.
    
    Returns:
        Game with 3 players
    """
    return Game(["Alice", "Bob", "Charlie"])
