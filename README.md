## Using uv for this repository

This project uses **uv** for environment/dependency management.

### 1. Install uv

**macOS / Linux**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```
**Windows (PowerShell)**
```
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. Create the environment and install dependencies
From the repository root (where pyproject.toml is):
```bash
uv sync
```
This will create/update the local virtual environment and install all locked dependencies.


### 3. Run code inside the uv environment
Run a script:
```bash
uv run script.py
```

### 4. Adding dependencies
Add a runtime dependency like so:
```bash
uv add <package>
```
Add a dev dependency like so:
```bash
uv add --dev <package>
```
Update the lockfile:
```bash
uv lock
uv sync
```
