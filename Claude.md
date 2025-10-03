# 5 Takes - Terminal Card Game

## Project Overview
A Python-based terminal implementation of the card game "5 Takes" (also known as "6 Nimmt!" or "Take 5"). This is a strategic card game where players try to avoid collecting penalty points by cleverly placing cards in rows.

## Game Rules

### Setup
- **Deck**: 104 cards numbered from 1 to 104
- **Players**: 3-10 players
- **Hand Size**: Each player receives 10 cards at the start of a round
- **Table**: 4 rows, each starting with 1 random card

### Gameplay

#### Turn Structure
1. All players simultaneously select one card from their hand (hidden)
2. All selected cards are revealed at the same time
3. Cards are placed in ascending order of their value

#### Card Placement Rules
- A card must be placed in the row where the rightmost card is the highest value that is still lower than the played card
- Example: Playing a 54 when rows end with [10, 53, 52, 100] → Card goes after 53
- If a card is lower than all rightmost values, the player must:
  - Choose a row to "wipe" (take all cards as penalty points)
  - Place their card as the new starting card for that row
- If a card becomes the 5th card in a row:
  - The player takes the first 4 cards as penalty points
  - Their card becomes the new starting card for that row

#### Scoring System
Each card has a point value (points are penalties - lower is better):
- **Base**: All cards = 1 point minimum
- **Multiples of 5**: 2 points (5, 15, 25, 35, 45, 65, 75, 85, 95)
- **Multiples of 10**: 3 points (10, 20, 30, 40, 50, 60, 70, 80, 90, 100)
- **Multiples of 11**: 5 points (11, 22, 33, 44, 66, 77, 88, 99)
- **Special**: 55 = 7 points (both multiple of 5 and 11)

#### Game End
- Rounds continue until at least one player exceeds 50 points
- The player with the lowest total score wins

## Project Structure

```
5takes/
├── .git/               # Git repository
├── .gitignore          # Git ignore rules
├── Claude.md           # This file - project documentation
├── README.md           # User-facing documentation
├── requirements.txt    # Python dependencies
├── setup.py            # Package installation script
│
├── src/
│   ├── __init__.py
│   ├── main.py         # Entry point for the game
│   ├── game/
│   │   ├── __init__.py
│   │   ├── card.py     # Card class and deck management
│   │   ├── player.py   # Player class
│   │   ├── table.py    # Game table and row management
│   │   ├── game.py     # Main game logic and round management
│   │   └── rules.py    # Game rules and scoring logic
│   └── ui/
│       ├── __init__.py
│       ├── display.py  # Terminal display and formatting
│       ├── input.py    # User input handling
│       └── colors.py   # Terminal color schemes
│
├── tests/
│   ├── __init__.py
│   ├── test_card.py
│   ├── test_player.py
│   ├── test_table.py
│   ├── test_game.py
│   └── test_rules.py
│
└── docs/
    └── design.md       # Technical design document
```

## Implementation Plan

### Phase 1: Core Game Logic ✅
- [ ] Create Card class with value and point calculation
- [ ] Implement Deck class for card management
- [ ] Create Table class with 4 rows
- [ ] Implement basic placement rules
- [ ] Add scoring system

### Phase 2: Player Management
- [ ] Create Player class
- [ ] Implement player input handling
- [ ] Add hand management
- [ ] Create turn selection mechanism
- [ ] Support 3-10 players

### Phase 3: Game Flow
- [ ] Implement Game class for round management
- [ ] Add simultaneous card reveal logic
- [ ] Handle card placement in order
- [ ] Implement row wiping logic
- [ ] Add round and game ending conditions

### Phase 4: User Interface
- [ ] Create terminal display system
- [ ] Add colored output for better readability
- [ ] Implement clear game state visualization
- [ ] Add input validation and error handling
- [ ] Show all players' cards simultaneously after selection

### Phase 5: Polish & Testing
- [ ] Add comprehensive unit tests
- [ ] Implement game statistics tracking
- [ ] Add game save/load functionality
- [ ] Add tutorial mode
- [ ] Create quick play options

### Phase 6: Future Enhancements
- [ ] Network multiplayer support
- [ ] Computer opponents (if desired)
- [ ] Tournament mode
- [ ] Custom rule variations

## Technical Decisions

### Language & Version
- Python 3.8+ for modern features and type hints

### Key Libraries
- `colorama` - Cross-platform colored terminal output
- `pytest` - Testing framework
- `typing` - Type hints for better code documentation

### Multiplayer Approach
- **Hot-seat multiplayer**: Players take turns at the same terminal
- **Privacy handling**: Clear screen between players, show "Pass to Player X" prompts
- **Card selection**: Hidden input mode where only the player can see their cards
- **Simultaneous reveal**: Store selections, then show all at once

### Design Patterns
- **Observer Pattern**: For game state updates and display
- **Command Pattern**: For player actions and undo functionality
- **State Pattern**: For game phases (setup, playing, scoring)

### Data Structures
- **Card**: Class with value and point properties
- **Row**: List with max size of 5 cards
- **Table**: List of 4 Row objects
- **Hand**: Set/List of Card objects per player
- **Player**: Class containing name, hand, and score
- **GameState**: Current round, turn, and player information

## Development Guidelines

### Code Style
- Follow PEP 8 Python style guide
- Use type hints for all function signatures
- Maximum line length: 100 characters
- Use descriptive variable names

### Git Workflow
1. Work on feature branches (`feature/description`)
2. Make atomic commits with clear messages
3. Use conventional commit format: `type: description`
   - `feat:` New feature
   - `fix:` Bug fix
   - `docs:` Documentation
   - `test:` Testing
   - `refactor:` Code refactoring

### Testing Strategy
- Unit tests for all game logic components
- Integration tests for game flow
- Property-based tests for rule validation
- Aim for >80% code coverage

## Current Status
- Project initialized with basic structure
- Game rules documented
- Implementation plan created

## Next Steps
1. Set up Python virtual environment
2. Create basic project structure
3. Implement Card and Deck classes
4. Begin with core game logic

## Notes for Development
- Keep terminal display simple but informative
- Ensure game state is always clear to all players
- Prioritize game rule correctness over features
- Consider accessibility (clear text, good contrast)
- Support hot-seat multiplayer (players take turns at the same terminal)

## Questions to Resolve
- How to handle screen clearing between players (privacy for card selection)?
- Should game history be saved between sessions?
- What statistics should we track for players?
- Should we add variations of the rules?
- Should we add a "pass device" mode for mobile/tablet play?
