# 5 Takes - Terminal Card Game

A Python implementation of the popular card game "5 Takes" (also known as "6 Nimmt!" or "Take 5").

## About the Game

5 Takes is a strategic card game where players simultaneously play cards, trying to avoid collecting penalty points. The player with the fewest points at the end wins!

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd 5takes
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## How to Play

### Starting the Game
```bash
python src/main.py
```

### Game Rules

#### Setup
- 104 cards numbered 1-104
- 3-10 players (human or AI)
- Each player gets 10 cards
- 4 rows on the table, each starting with 1 card

#### Gameplay
1. Each turn, all players select a card simultaneously
2. Cards are revealed and placed in ascending order
3. Each card goes in the row where it's closest to (but higher than) the last card
4. If your card is lower than all rows, you must take a row and start fresh
5. The 5th card in a row causes you to take the first 4 cards

#### Scoring (Lower is Better!)
- Base: 1 point per card
- Multiples of 5: 2 points
- Multiples of 10: 3 points  
- Multiples of 11: 5 points
- The number 55: 7 points

#### Winning
The game ends when someone exceeds 50 points. The player with the lowest score wins!

## Features

- **Single Player**: Play against AI opponents
- **Multiplayer**: Local multiplayer for 3-10 players
- **AI Difficulty**: Choose from Easy, Medium, or Hard AI opponents
- **Colorful Display**: Easy-to-read terminal interface
- **Statistics**: Track your wins and average scores

## Controls

- **Number keys (1-10)**: Select a card from your hand
- **Arrow keys**: Navigate menus
- **Enter**: Confirm selection
- **Q**: Quit game

## Development

### Running Tests
```bash
pytest tests/
```

### Contributing
Please read CONTRIBUTING.md for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Inspired by the original "6 Nimmt!" by Wolfgang Kramer
- Thanks to all contributors and testers

## Support

For issues, questions, or suggestions, please open an issue on GitHub.
