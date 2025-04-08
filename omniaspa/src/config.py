"""Application Configuration Module."""

import os
from dotenv import load_dotenv
import logging

# Load environment variables from .env file
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env') # Look for .env in project root
load_dotenv(dotenv_path=dotenv_path)

logger = logging.getLogger(__name__)

# --- Database Configuration ---
DATABASE_TYPE = os.getenv("DATABASE_TYPE", "sqlite")
SQLITE_DB_PATH = os.getenv("SQLITE_DB_PATH", "data/proposal_generator.db") # Default path relative to project root
PROPOSAL_OUTPUT_DIR = os.getenv("PROPOSAL_OUTPUT_DIR", "output/proposals").split('#', 1)[0].strip() # Directory for final MD files

# --- LLM Configuration ---
# Example: Define which LLM to use for each agent role or globally
# These will likely point to specific API keys or model identifiers loaded from .env
# Using placeholders for now as requested
LLM_PROVIDER_DEFAULT = os.getenv("LLM_PROVIDER_DEFAULT", "placeholder")
LLM_MODEL_DEFAULT = os.getenv("LLM_MODEL_DEFAULT", "placeholder-model")

# Agent-specific LLM overrides (Example)
LLM_PROVIDER_IDEATOR = os.getenv("LLM_PROVIDER_IDEATOR", LLM_PROVIDER_DEFAULT)
LLM_MODEL_IDEATOR = os.getenv("LLM_MODEL_IDEATOR", LLM_MODEL_DEFAULT)

LLM_PROVIDER_WRITER = os.getenv("LLM_PROVIDER_WRITER", LLM_PROVIDER_DEFAULT)
LLM_MODEL_WRITER = os.getenv("LLM_MODEL_WRITER", LLM_MODEL_DEFAULT)

# Token settings (can be overridden in .env)
LLM_TOKENS_IDEATOR = int(os.getenv("LLM_TOKENS_IDEATOR", "2000").split('#', 1)[0].strip())

# API Keys (Loaded directly from environment, not stored here)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
# Add others as needed
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434").split('#', 1)[0].strip()


# --- Logging Configuration ---
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").split('#', 1)[0].strip().upper()
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

def setup_logging():
    """Sets up global logging configuration."""
    logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)
    logger.info(f"Logging setup complete. Level: {LOG_LEVEL}")

# --- Other Settings ---
MAX_ITERATIONS = int(os.getenv("MAX_ITERATIONS", "10").split('#', 1)[0].strip()) # Max iterations for *overall* proposal refinement (if used)
MAX_REFINEMENT_LOOPS = int(os.getenv("MAX_REFINEMENT_LOOPS", "5").split('#', 1)[0].strip()) # Max loops for *idea* refinement cycle
REFINEMENT_SCORE_THRESHOLD = int(os.getenv("REFINEMENT_SCORE_THRESHOLD", "80").split('#', 1)[0].strip()) # Score threshold to exit refinement
REFINEMENT_MAJOR_ISSUE_PHRASE = os.getenv("REFINEMENT_MAJOR_ISSUE_PHRASE", "major issue").split('#', 1)[0].strip() # Phrase indicating major issue in critique


# --- LLM Call Parameters (can be overridden in .env) ---

# Ideator Generate Ideas
# LLM_TOKENS_IDEATOR already added previously
LLM_TEMP_IDEATOR = float(os.getenv("LLM_TEMP_IDEATOR", "0.8").split('#', 1)[0].strip())

# Judge Critique Idea
LLM_TOKENS_JUDGE_CRITIQUE = int(os.getenv("LLM_TOKENS_JUDGE_CRITIQUE", "500").split('#', 1)[0].strip())
LLM_TEMP_JUDGE_CRITIQUE = float(os.getenv("LLM_TEMP_JUDGE_CRITIQUE", "0.4").split('#', 1)[0].strip())

# Judge Improve Idea
LLM_TOKENS_JUDGE_IMPROVE = int(os.getenv("LLM_TOKENS_JUDGE_IMPROVE", "600").split('#', 1)[0].strip())
LLM_TEMP_JUDGE_IMPROVE = float(os.getenv("LLM_TEMP_JUDGE_IMPROVE", "0.6").split('#', 1)[0].strip())

# Expert Improve Idea
LLM_TOKENS_EXPERT_IMPROVE = int(os.getenv("LLM_TOKENS_EXPERT_IMPROVE", "600").split('#', 1)[0].strip())
LLM_TEMP_EXPERT_IMPROVE = float(os.getenv("LLM_TEMP_EXPERT_IMPROVE", "0.6").split('#', 1)[0].strip())

# Expert Review Proposal
LLM_TOKENS_EXPERT_REVIEW = int(os.getenv("LLM_TOKENS_EXPERT_REVIEW", "500").split('#', 1)[0].strip()) # Tokens for review feedback
LLM_TEMP_EXPERT_REVIEW = float(os.getenv("LLM_TEMP_EXPERT_REVIEW", "0.4").split('#', 1)[0].strip())

# Founder Improve Idea
LLM_TOKENS_FOUNDER_IMPROVE = int(os.getenv("LLM_TOKENS_FOUNDER_IMPROVE", "600").split('#', 1)[0].strip())
LLM_TEMP_FOUNDER_IMPROVE = float(os.getenv("LLM_TEMP_FOUNDER_IMPROVE", "0.6").split('#', 1)[0].strip())

# Writer Write Section
LLM_TOKENS_WRITER_SECTION = int(os.getenv("LLM_TOKENS_WRITER_SECTION", "1000").split('#', 1)[0].strip())
LLM_TEMP_WRITER_SECTION = float(os.getenv("LLM_TEMP_WRITER_SECTION", "0.6").split('#', 1)[0].strip())

# Writer Compile Proposal
LLM_TOKENS_WRITER_COMPILE = int(os.getenv("LLM_TOKENS_WRITER_COMPILE", "2500").split('#', 1)[0].strip())
LLM_TEMP_WRITER_COMPILE = float(os.getenv("LLM_TEMP_WRITER_COMPILE", "0.5").split('#', 1)[0].strip())
MAX_PROPOSAL_LENGTH_TOKENS = int(os.getenv("MAX_PROPOSAL_LENGTH_TOKENS", "8000").split('#', 1)[0].strip()) # Max tokens for final proposal compilation call
TARGET_PROPOSAL_LENGTH_DESC = os.getenv("TARGET_PROPOSAL_LENGTH_DESC", "approx 20 pages / 8000 tokens") # Target length description for prompt


# Log loaded config (excluding sensitive keys)
logger.info(f"Database Type: {DATABASE_TYPE}")
logger.info(f"SQLite DB Path: {SQLITE_DB_PATH}")
logger.info(f"Default LLM Provider: {LLM_PROVIDER_DEFAULT}")
logger.info(f"Default LLM Model: {LLM_MODEL_DEFAULT}")
logger.info(f"Max Iterations: {MAX_ITERATIONS}")
# Avoid logging API keys