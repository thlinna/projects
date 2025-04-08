# EU Digital Europe Programme Proposal Generator

An AI-native, local application designed to autonomously generate highly successful project proposals for the EU Digital Europe Programme, aiming at securing funding between €10M and €20M per application.

## Project Structure

- `src/`: Source code
  - `agents/`: Agent implementations (base, specific roles)
  - `config.py`: Application configuration loader
  - `data_storage/`: Database interaction logic (repositories)
  - `llm_integration.py`: LLM interaction (currently placeholders)
  - `models/`: Core data structures (Proposal, Idea, Evaluation)
  - `workflow/`: Workflow orchestration logic (WorkflowEngine)
  - `cli.py`: Command-line interface entry point
- `tests/`: Test files (unit, integration)
- `data/`: Default directory for the SQLite database (gitignored)
- `docs/`: Project documentation (Architecture, PRD)
- `.env.sample`: Sample environment variable file
- `.gitignore`: Specifies intentionally untracked files
- `IMPLEMENTATION_PLAN.md`: High-level task list
- `PRD.md`: Product Requirements Document
- `pyproject.toml`: Project metadata and dependencies
- `README.md`: This file

## Development

### Setup

```bash
# Install dependencies (assuming they are listed in pyproject.toml or requirements.txt)
# If using pyproject.toml with optional dev dependencies:
pip install -e ".[dev]"
# Or if using requirements.txt:
# pip install -r requirements.txt
# pip install -r requirements-dev.txt # If you have separate dev requirements

# 2. Set up environment variables
# Copy the sample .env file and configure it with your settings (e.g., API keys)
cp .env.sample .env
# nano .env # Or use your preferred editor to add API keys etc.

# 3. Initialize Database (optional, CLI does this on first run)
# The database file (e.g., data/proposal_generator.db) will be created automatically.
```

### Running Tests

```bash
pytest -v

### Running the CLI

Use `python -m src.cli` followed by a command:

```bash
# Generate a new proposal for a given topic
python -m src.cli generate "Your Proposal Topic Here"

# List existing proposals in the database
python -m src.cli list

# Run a single step of the workflow for an existing proposal (for debugging)
python -m src.cli runstep <PROPOSAL_ID>
```