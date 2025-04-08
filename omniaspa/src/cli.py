"""Command-Line Interface for the EU Proposal Generator."""

import argparse
import logging
import os
import sqlite3
from typing import Dict, Optional # Added Optional
import re # For checking major issue in selection logic

# Setup logging first
from src import config
config.setup_logging() # Use the setup function from config

logger = logging.getLogger(__name__)

# Import core components
from src.agents.base_agent import Agent
from src.agents.programme_expert import ProgrammeExpertAgent
from src.agents.creative_ideator import CreativeIdeatorAgent
from src.agents.startup_founder import StartupFounderAgent
from src.agents.practical_judge import PracticalJudgeAgent
from src.agents.proposal_writer import ProposalWriterAgent
from src.data_storage.sqlite_repository import (
    ProposalRepository, IdeaRepository, EvaluationRepository,
    initialize_database # Import the initialization function
)
from src.workflow.workflow_engine import WorkflowEngine
from src.models.proposal import Proposal # For type hinting
from src.models.idea import Idea # For type hinting
from src.models.evaluation import Evaluation # For type hinting


def setup_dependencies() -> WorkflowEngine:
    """Initializes and wires up dependencies (DB, Agents, Engine)."""
    logger.info("Setting up application dependencies...")

    # Database setup
    # Ensure data directory exists
    db_dir = os.path.dirname(config.SQLITE_DB_PATH)
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir)
        logger.info(f"Created data directory: {db_dir}")

    # Create connection (will also initialize tables via repo constructor)
    # For CLI, manage connection lifecycle explicitly
    try:
        # Use check_same_thread=False for simplicity in single-threaded CLI
        # Review if threading is introduced later
        db_connection = sqlite3.connect(config.SQLITE_DB_PATH, detect_types=sqlite3.PARSE_DECLTYPES, check_same_thread=False)
        db_connection.row_factory = sqlite3.Row
        db_connection.execute("PRAGMA foreign_keys = ON")
        logger.info(f"Database connection established: {config.SQLITE_DB_PATH}")
    except sqlite3.Error as e:
        logger.error(f"Fatal: Could not connect to database at {config.SQLITE_DB_PATH}: {e}")
        raise # Exit if DB connection fails

    # Initialize database tables on the connection
    initialize_database(db_connection)

    # Initialize repositories with the connection
    proposal_repo = ProposalRepository(db_connection)
    idea_repo = IdeaRepository(db_connection)
    evaluation_repo = EvaluationRepository(db_connection)
    logger.info("Repositories initialized.")

    # Initialize agents
    agents: Dict[str, Agent] = {
        "expert": ProgrammeExpertAgent(),
        "ideator": CreativeIdeatorAgent(),
        "founder": StartupFounderAgent(),
        "judge": PracticalJudgeAgent(),
        "writer": ProposalWriterAgent(),
    }
    logger.info("Agents initialized.")

    # Initialize workflow engine
    workflow_engine = WorkflowEngine(
        agents=agents,
        proposal_repo=proposal_repo,
        idea_repo=idea_repo,
        evaluation_repo=evaluation_repo
        # Pass the connection if needed by engine, or let repos handle it
    )
    logger.info("WorkflowEngine initialized.")

    # Return engine and connection (so connection can be closed later)
    # Modify if engine should manage connection lifecycle
    return workflow_engine, db_connection


def run_proposal_generation(engine: WorkflowEngine, topic: str):
    """Runs the full proposal generation workflow."""
    logger.info(f"--- Starting Proposal Generation for topic: '{topic}' ---")
    try:
        # 1. Start Proposal
        proposal = engine.start_new_proposal(topic)
        proposal_id = proposal.id
        logger.info(f"Proposal created with ID: {proposal_id}, Status: {proposal.status}")

        # 2. Run Workflow Steps Iteratively
        iteration = 0
        max_iterations = config.MAX_ITERATIONS
        while proposal.status != "completed" and iteration < max_iterations:
            iteration += 1
            logger.info(f"--- Running Workflow Iteration {iteration}/{max_iterations} (Status: {proposal.status}) ---")
            engine.run_step(proposal_id)
            # Refresh proposal state after step
            proposal = engine.proposal_repo.get_by_id(proposal_id)
            if not proposal:
                logger.error(f"Proposal {proposal_id} disappeared during workflow!")
                break
            logger.info(f"Iteration {iteration} complete. New Status: {proposal.status}")

        # 3. Final Output
        if proposal.status == "completed":
            logger.info(f"--- Proposal Generation Completed for ID: {proposal_id} ---")
            # Retrieve final proposal details (e.g., the compiled markdown)
            final_proposal = engine.proposal_repo.get_by_id(proposal_id)
            print("\n=== FINAL PROPOSAL OUTPUT ===")
            # Assuming final output is appended to description or stored elsewhere
            # Find the start of the final output marker
            output_marker = "\n\n--- FINAL OUTPUT ---\n"
            marker_pos = final_proposal.description.find(output_marker)
            if marker_pos != -1:
                final_md = final_proposal.description[marker_pos + len(output_marker):]
                print(final_md)
            else:
                # Fallback if marker not found (e.g., older proposal)
                print(final_proposal.description)
            print("============================")
        elif iteration >= max_iterations:
            logger.warning(f"--- Proposal Generation Halted: Max iterations ({max_iterations}) reached ---")
            print(f"\nWorkflow stopped after {max_iterations} iterations. Final status: {proposal.status}")
        else:
             logger.error(f"--- Proposal Generation Failed for ID: {proposal_id} ---")
             print(f"\nWorkflow failed. Final status: {proposal.status}")

    except Exception as e:
        logger.error(f"An unexpected error occurred during proposal generation: {e}", exc_info=True)
        print(f"\nAn error occurred: {e}")


def list_proposals(engine: WorkflowEngine):
    """Lists existing proposals."""
    logger.info("--- Listing Existing Proposals ---")
    try:
        proposals = engine.proposal_repo.get_all()
        if not proposals:
            print("No proposals found in the database.")
            return

        print("\n--- Existing Proposals ---")
        for p in proposals:
            print(f"ID: {p.id} | Status: {p.status} | Title: {p.title} | Updated: {p.updated_at.strftime('%Y-%m-%d %H:%M')}")
        print("------------------------")

    except Exception as e:
        logger.error(f"An unexpected error occurred while listing proposals: {e}", exc_info=True)
        print(f"\nAn error occurred: {e}")

# Helper function copied/adapted from WorkflowEngine to avoid circular import/dependency
def _get_latest_evaluation_cli(evaluation_repo: EvaluationRepository, idea_id: str) -> Optional[Evaluation]:
    """Retrieves the most recent evaluation for a given idea."""
    try:
        evaluations = evaluation_repo.get_by_idea_id(idea_id)
        if evaluations:
            evaluations.sort(key=lambda x: x.created_at, reverse=True)
            return evaluations[0]
        return None
    except Exception as e:
        logger.error(f"Failed to retrieve evaluations for idea {idea_id}: {e}", exc_info=True)
        return None

def show_best_idea(engine: WorkflowEngine, proposal_id: str):
    """Retrieves and displays the best refined idea for a proposal."""
    logger.info(f"--- Showing Best Idea for Proposal ID: {proposal_id} ---")
    try:
        proposal = engine.proposal_repo.get_by_id(proposal_id)
        if not proposal:
            print(f"Proposal with ID {proposal_id} not found.")
            return

        ideas = engine.idea_repo.get_by_proposal_id(proposal_id)
        if not ideas:
            print(f"No ideas found for proposal {proposal_id}.")
            return

        best_idea: Optional[Idea] = None
        highest_score = -1

        # Logic adapted from _select_best_idea_for_writing
        for idea in ideas:
            latest_eval = _get_latest_evaluation_cli(engine.evaluation_repo, idea.id)
            if latest_eval:
                score = latest_eval.score or 0
                feedback = latest_eval.feedback or ""
                has_major_issue = re.search(config.REFINEMENT_MAJOR_ISSUE_PHRASE, feedback, re.IGNORECASE) is not None

                # Priority 1: Meets threshold and no major issues
                if score >= config.REFINEMENT_SCORE_THRESHOLD and not has_major_issue:
                    best_idea = idea
                    logger.info(f"Selected idea {idea.id} (Score: {score}, Cycle: {idea.refinement_cycle}) - Met threshold.")
                    break # Found the best possible, stop searching

                # Priority 2: Keep track of the highest scoring idea below threshold (or if max loops hit)
                if score > highest_score:
                    highest_score = score
                    best_idea = idea # Tentatively select this one

        if not best_idea and ideas: # Fallback if no suitable idea found by score logic
            best_idea = ideas[-1] # Just pick the last one processed
            logger.warning(f"No idea met criteria or had score. Falling back to last idea: {best_idea.id}")

        if best_idea:
            print(f"\n--- Best Idea for Proposal {proposal_id} (Cycle: {best_idea.refinement_cycle}) ---")
            print(f"\n## {best_idea.title}\n")
            print(best_idea.description)
            print("\n----------------------------------------------------")
        else:
            # This case should ideally not happen if there are ideas
            print(f"Could not determine the best idea for proposal {proposal_id}.")

    except Exception as e:
        logger.error(f"An unexpected error occurred while showing best idea: {e}", exc_info=True)
        print(f"\nAn error occurred: {e}")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="EU Proposal Generator CLI - Automates proposal creation using AI agents.",
        formatter_class=argparse.RawTextHelpFormatter # Allows for better formatting in help
    )
    subparsers = parser.add_subparsers(
        dest="command",
        help="Available actions. Use '<command> --help' for more details.",
        required=True # Make command mandatory
    )

    # --- 'generate' command ---
    parser_generate = subparsers.add_parser(
        "generate",
        help="Starts the full AI-driven workflow to generate a new proposal.",
        description="Creates a new proposal entry in the database and runs the agent workflow (ideation, critique, refinement, writing, finalization) based on the provided topic."
    )
    parser_generate.add_argument(
        "topic",
        type=str,
        help="The central theme or subject area for the new proposal (e.g., 'AI in Healthcare')."
    )

    # --- 'list' command ---
    parser_list = subparsers.add_parser(
        "list",
        help="Displays a summary of all proposals currently stored in the database.",
        description="Lists proposals with their ID, status, title, and last updated timestamp."
    )

    # --- 'runstep' command (for debugging/manual control) ---
    parser_runstep = subparsers.add_parser(
        "runstep",
        help="Manually executes the next logical workflow step for a specific proposal.",
        description="Useful for debugging or stepping through the process. Identifies the proposal's current status and triggers the corresponding agent action(s)."
    )
    parser_runstep.add_argument(
        "proposal_id",
        type=str,
        help="The unique ID (UUID) of the existing proposal to advance."
    )

    # --- 'show-idea' command ---
    parser_show = subparsers.add_parser(
        "show-idea",
        help="Displays the title and description of the best refined idea for a proposal.",
        description="Retrieves a proposal by ID, selects the idea that best meets the refinement criteria (or the highest scoring/latest otherwise), and prints its details."
    )
    parser_show.add_argument(
        "proposal_id",
        type=str,
        help="The unique ID (UUID) of the proposal whose best idea you want to view."
    )


    args = parser.parse_args()

    engine, db_conn = None, None # Initialize to None
    try:
        engine, db_conn = setup_dependencies()

        if args.command == "generate":
            run_proposal_generation(engine, args.topic)
        elif args.command == "list":
            list_proposals(engine)
        elif args.command == "runstep":
             logger.info(f"--- Manually running step for Proposal ID: {args.proposal_id} ---")
             engine.run_step(args.proposal_id)
             logger.info(f"--- Step completed for Proposal ID: {args.proposal_id} ---")
             # Optionally show status after step
             proposal = engine.proposal_repo.get_by_id(args.proposal_id)
             if proposal:
                 print(f"Current status of proposal {args.proposal_id}: {proposal.status}")
             else:
                 print(f"Proposal {args.proposal_id} not found after running step.")
        elif args.command == "show-idea":
            show_best_idea(engine, args.proposal_id)

        else:
            parser.print_help()

    except Exception as e:
        # Catch-all for setup errors or other unexpected issues during execution
        error_type = type(e).__name__
        logger.critical(f"CLI execution failed due to {error_type}: {e}", exc_info=True)
        print(f"\nERROR: A critical error occurred ({error_type}).")
        print(f"Details: {e}")
        print("Check the application logs for more information.")
    finally:
        # Ensure database connection is closed if it was opened
        if db_conn:
            try:
                db_conn.close()
                logger.info("Database connection closed.")
            except sqlite3.Error as e:
                logger.error(f"Error closing database connection: {e}")


if __name__ == "__main__":
    main()