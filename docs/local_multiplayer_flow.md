# Local Multiplayer Flow Design

## Overview
5 Takes is designed as a local hot-seat multiplayer game where players take turns using the same terminal/computer. This document outlines how we handle the challenges of local multiplayer, particularly maintaining card privacy.

## Turn Flow

### Card Selection Phase
1. **Display prompt**: "Pass device to Player 1 (Alice)"
2. **Wait for confirmation**: Player presses Enter when ready
3. **Clear screen**: Ensure previous player's information is hidden
4. **Show player's hand**: Display only current player's cards
5. **Player selects card**: Input validation and confirmation
6. **Hide selection**: Clear screen again
7. **Repeat**: Continue for all players

### Reveal Phase
1. **All players have selected**: Confirm all selections are made
2. **Clear screen**: Prepare for reveal
3. **Show all selections**: Display all players' chosen cards simultaneously
4. **Process in order**: Place cards according to game rules
5. **Update scores**: Show any points gained
6. **Continue**: Next turn or round end

## Privacy Mechanisms

### Screen Clearing
```python
def clear_screen():
    """Clear terminal screen for privacy between players."""
    os.system('cls' if os.name == 'nt' else 'clear')
```

### Pass Device Prompt
```python
def pass_device_prompt(player_name: str):
    """Prompt to pass device to next player."""
    clear_screen()
    print(f"Please pass the device to {player_name}")
    print("Press Enter when ready...")
    input()
    clear_screen()
```

### Hidden Card Selection
```python
def select_card_privately(player: Player):
    """Allow player to select a card without others seeing."""
    pass_device_prompt(player.name)
    display_hand(player.hand)
    selection = get_card_selection()
    clear_screen()
    print(f"{player.name} has made their selection.")
    print("Press Enter to continue...")
    input()
    return selection
```

## Display States

### 1. Waiting for Player
```
========================================
          5 TAKES - Round 3
========================================

Please pass the device to Alice

Press Enter when ready...
```

### 2. Player's Turn
```
========================================
    Alice's Turn - Round 3, Turn 5
========================================

Table:
Row 1: [12] [15] [18]
Row 2: [34]
Row 3: [56] [67] [72] [88]
Row 4: [91] [95]

Your Hand:
1. [23] (1 pt)    6. [55] (7 pts)
2. [31] (1 pt)    7. [64] (1 pt)
3. [40] (3 pts)   8. [77] (5 pts)
4. [45] (2 pts)   9. [89] (1 pt)
5. [50] (3 pts)   10. [102] (1 pt)

Select a card (1-10): _
```

### 3. All Cards Revealed
```
========================================
       All Cards Revealed - Turn 5
========================================

Players' Selections:
- Alice:   [45] (2 pts)
- Bob:     [23] (1 pt)
- Charlie: [89] (1 pt)
- Diana:   [77] (5 pts)

Processing in order: 23, 45, 77, 89...

[Press Enter to see placement]
```

## Session Management

### Player Setup
- At game start, register all players with names
- Store player order for consistent turn rotation
- Option to randomize seating order each round

### Between Rounds
- Show full scoreboard with all players
- Option to continue or end game
- No need for privacy during score display

### Game End
- Final scores visible to all
- Winner announcement
- Statistics summary

## Future Enhancements

### Network Mode (Future)
- Each player uses their own device
- Central server manages game state
- Real-time updates across devices

### Computer Players (Future)
- Add as optional players
- No privacy needed for computer turns
- Instant card selection

## Implementation Priority

1. **Phase 1**: Basic pass-and-play without screen clearing
2. **Phase 2**: Add screen clearing and privacy prompts  
3. **Phase 3**: Improve UI with colors and formatting
4. **Phase 4**: Add session management and statistics
5. **Future**: Network or computer players
