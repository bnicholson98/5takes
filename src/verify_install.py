#!/usr/bin/env python3
"""Verify that 5 Takes installation is working correctly."""

import sys
import os

def check_python_version():
    """Check if Python version is 3.8+."""
    if sys.version_info < (3, 8):
        print(f"❌ Python 3.8+ required, found {sys.version}")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    return True

def check_dependencies():
    """Check if required dependencies are available."""
    try:
        import colorama
        print("✅ colorama available")
        return True
    except ImportError:
        print("❌ colorama not found. Run: pip install colorama")
        return False

def check_game_imports():
    """Check if game modules can be imported."""
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
    
    try:
        from game.card import Card, Deck
        from game.player import Player
        from game.table import Table
        from game.rules import GameRules
        from game.game import Game
        print("✅ Game logic modules")
        
        from ui.display import GameDisplay
        from ui.input import InputHandler
        from ui.colors import colors
        print("✅ UI modules")
        
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_basic_functionality():
    """Test basic game functionality."""
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
    
    try:
        from game.card import Card, Deck
        from game.game import Game
        
        # Test card creation and scoring
        card = Card(55)
        assert card.points == 7, "Card 55 should have 7 points"
        
        # Test deck
        deck = Deck()
        assert deck.remaining_cards == 104, "Deck should have 104 cards"
        
        # Test game creation
        game = Game(["Alice", "Bob", "Charlie"])
        assert len(game.players) == 3, "Game should have 3 players"
        
        print("✅ Basic functionality tests pass")
        return True
        
    except Exception as e:
        print(f"❌ Functionality test failed: {e}")
        return False

def main():
    """Run all verification checks."""
    print("5 Takes Installation Verification")
    print("=" * 35)
    
    all_good = True
    
    all_good &= check_python_version()
    all_good &= check_dependencies()
    all_good &= check_game_imports()
    all_good &= test_basic_functionality()
    
    print("=" * 35)
    
    if all_good:
        print("🎉 Installation verified! Run 'python run_game.py' to play.")
    else:
        print("❌ Installation has issues. Please fix the problems above.")
    
    return 0 if all_good else 1

if __name__ == "__main__":
    exit(main())
