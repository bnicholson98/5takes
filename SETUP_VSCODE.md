# VSCode Setup Instructions for 5 Takes

## Git Repository Setup

### If you haven't already initialized git:
```bash
git init
git branch -m main
git add .
git commit -m "Initial commit"
```

### To connect to a remote repository (e.g., GitHub):
1. Create a new repository on GitHub (without initializing with README)
2. Add the remote:
```bash
git remote add origin https://github.com/YOUR_USERNAME/5takes.git
git push -u origin main
```

## VSCode Configuration

### Recommended Extensions
Install these VSCode extensions for the best development experience:

1. **Python** (ms-python.python) - Essential Python support
2. **Pylance** (ms-python.vscode-pylance) - Python language server
3. **GitLens** (eamodio.gitlens) - Enhanced Git capabilities
4. **Python Docstring Generator** (njpwerner.autodocstring) - Auto-generate docstrings
5. **Better Comments** (aaron-bond.better-comments) - Highlight important comments

### Workspace Settings
Create `.vscode/settings.json` in your project root:

```json
{
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.linting.pylintEnabled": false,
    "python.formatting.provider": "black",
    "python.testing.pytestEnabled": true,
    "python.testing.unittestEnabled": false,
    "python.testing.pytestArgs": [
        "tests"
    ],
    "editor.formatOnSave": true,
    "editor.rulers": [100],
    "files.exclude": {
        "**/__pycache__": true,
        "**/*.pyc": true
    }
}
```

### Launch Configuration
Create `.vscode/launch.json` for debugging:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: 5 Takes Game",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/src/main.py",
            "console": "integratedTerminal",
            "justMyCode": true
        },
        {
            "name": "Python: Current File",
            "type": "python",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal",
            "justMyCode": true
        }
    ]
}
```

## Python Environment Setup

### Create Virtual Environment
In VSCode terminal (Ctrl+`):
```bash
python -m venv venv
```

### Activate Virtual Environment
- **Windows**: `venv\Scripts\activate`
- **Mac/Linux**: `source venv/bin/activate`

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Select Python Interpreter in VSCode
1. Press `Ctrl+Shift+P` (Cmd+Shift+P on Mac)
2. Type "Python: Select Interpreter"
3. Choose the interpreter from `./venv/`

## Quick Commands

### VSCode Shortcuts
- **Run Python File**: `Ctrl+F5`
- **Debug Python File**: `F5`
- **Run Tests**: `Ctrl+Shift+P` → "Python: Run All Tests"
- **Terminal**: `Ctrl+`` (backtick)
- **Command Palette**: `Ctrl+Shift+P`

### Git Commands in VSCode
- **Source Control Panel**: `Ctrl+Shift+G`
- **Stage Changes**: Click `+` next to files
- **Commit**: Type message and `Ctrl+Enter`
- **Push/Pull**: Click sync button in status bar

## Project Structure Creation

Run this to create the full project structure:
```bash
# Create directories
mkdir -p src/game src/ui src/ai tests docs

# Create __init__.py files
touch src/__init__.py
touch src/game/__init__.py
touch src/ui/__init__.py
touch src/ai/__init__.py
touch tests/__init__.py

# Create main Python files
touch src/main.py
touch src/game/card.py src/game/player.py src/game/table.py src/game/game.py src/game/rules.py
touch src/ui/display.py src/ui/input.py src/ui/colors.py
touch src/ai/base_ai.py src/ai/easy_ai.py src/ai/hard_ai.py
```

## Verification

To verify everything is set up correctly:
```bash
# Check Python version
python --version  # Should be 3.8+

# Check virtual environment is activated
which python  # Should point to venv/bin/python

# Check git status
git status

# Run a simple test (once main.py exists)
python src/main.py
```

## Troubleshooting

### If Python interpreter not found:
1. Make sure virtual environment is activated
2. Reinstall Python extension in VSCode
3. Reload VSCode window (`Ctrl+Shift+P` → "Developer: Reload Window")

### If imports not working:
1. Add project root to PYTHONPATH in `.env` file:
```
PYTHONPATH=${workspaceFolder}
```

### If terminal colors not working on Windows:
Install Windows Terminal from Microsoft Store for better color support

## Next Steps
1. Follow the implementation plan in `Claude.md`
2. Start with creating the Card class in `src/game/card.py`
3. Write tests as you go in the `tests/` directory
4. Commit changes frequently with descriptive messages
