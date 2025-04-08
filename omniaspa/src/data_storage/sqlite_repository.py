"""SQLite repository implementation for the data storage layer."""

import sqlite3
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
import uuid
import logging

from src.models.proposal import Proposal
from src.models.idea import Idea
from src.models.evaluation import Evaluation

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Helper function to convert datetime to ISO format string for SQLite
def dt_to_iso(dt: datetime) -> str:
    """Converts datetime object to ISO 8601 string."""
    # Ensure datetime is timezone-aware (UTC) before formatting
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.isoformat()

# Helper function to convert ISO format string back to datetime object
def iso_to_dt(iso_str: str) -> datetime:
    """Converts ISO 8601 string back to datetime object."""
    dt = datetime.fromisoformat(iso_str)
    # Ensure datetime is timezone-aware (UTC)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt

# --- Database Initialization ---

def initialize_database(conn: sqlite3.Connection):
    """Creates the necessary database tables if they don't exist."""
    create_proposals_table = """
    CREATE TABLE IF NOT EXISTS proposals (
        id TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        status TEXT NOT NULL,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL,
        selected_idea_id TEXT, -- Added: ID of the idea chosen for refinement/writing
        generated_sections TEXT, -- Added: JSON string of generated sections
        compiled_markdown TEXT -- Added: Final compiled markdown output
    );
    """
    create_ideas_table = """
    CREATE TABLE IF NOT EXISTS ideas (
        id TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        proposal_id TEXT NOT NULL,
        created_at TEXT NOT NULL,
        FOREIGN KEY (proposal_id) REFERENCES proposals (id) ON DELETE CASCADE
    );
    """
    create_evaluations_table = """
    CREATE TABLE IF NOT EXISTS evaluations (
        id TEXT PRIMARY KEY,
        evaluator TEXT NOT NULL,
        score INTEGER,
        feedback TEXT NOT NULL,
        created_at TEXT NOT NULL,
        proposal_id TEXT,
        idea_id TEXT,
        FOREIGN KEY (proposal_id) REFERENCES proposals (id) ON DELETE CASCADE,
        FOREIGN KEY (idea_id) REFERENCES ideas (id) ON DELETE CASCADE,
        CHECK (proposal_id IS NOT NULL OR idea_id IS NOT NULL),
        CHECK (proposal_id IS NULL OR idea_id IS NULL)
    );
    """
    # Helper function to add a column if it doesn't exist
    def _add_column_if_not_exists(cursor: sqlite3.Cursor, table_name: str, column_name: str, column_type: str):
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = [column[1] for column in cursor.fetchall()]
        if column_name not in columns:
            try:
                logger.info(f"Adding column '{column_name}' to table '{table_name}'...")
                cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}")
                logger.info(f"Column '{column_name}' added successfully.")
            except sqlite3.OperationalError as e:
                # Handle cases where ALTER TABLE might fail unexpectedly (though unlikely for ADD COLUMN)
                logger.error(f"Failed to add column '{column_name}' to '{table_name}': {e}")
                raise
        else:
             logger.debug(f"Column '{column_name}' already exists in table '{table_name}'.")

    try:
        cursor = conn.cursor()
        logger.info("Ensuring database tables and columns exist...")

        # Create tables if they don't exist
        cursor.execute(create_proposals_table)
        cursor.execute(create_ideas_table)
        cursor.execute(create_evaluations_table)

        # Add columns to 'proposals' table if they don't exist
        _add_column_if_not_exists(cursor, "proposals", "selected_idea_id", "TEXT")
        _add_column_if_not_exists(cursor, "proposals", "generated_sections", "TEXT")
        _add_column_if_not_exists(cursor, "proposals", "compiled_markdown", "TEXT")

        conn.commit()
        logger.info("Database schema checked/updated successfully.")
    except sqlite3.Error as e:
        logger.error(f"Error initializing/updating database schema: {e}")
        raise # Re-raise critical initialization errors
#     pass


class ProposalRepository:
    """Repository for Proposal data operations."""

    def __init__(self, connection: sqlite3.Connection):
        """Initialize with a SQLite database connection."""
        self.conn = connection

    def _row_to_proposal(self, row: sqlite3.Row) -> Proposal:
        """Maps a database row to a Proposal object."""
        # Ensure the connection's row_factory is set to sqlite3.Row if not already
        # This allows accessing columns by name (e.g., row['id'])
        return Proposal(
            id=row['id'],
            title=row['title'],
            description=row['description'],
            status=row['status'],
            created_at=iso_to_dt(row['created_at']),
            updated_at=iso_to_dt(row['updated_at']),
            selected_idea_id=row['selected_idea_id'],
            generated_sections=row['generated_sections'],
            compiled_markdown=row['compiled_markdown'] # Added
            # Note: ideas and evaluations are not loaded here by default
        )

    def save(self, proposal: Proposal) -> None:
        """Save a Proposal to the database."""
        sql = """
        INSERT INTO proposals (id, title, description, status, created_at, updated_at, selected_idea_id, generated_sections, compiled_markdown)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        conn = None
        try:
            # Use the connection passed during initialization
            conn = self.conn
            cursor = conn.cursor()
            cursor.execute(sql, (
                proposal.id,
                proposal.title,
                proposal.description,
                proposal.status,
                dt_to_iso(proposal.created_at),
                dt_to_iso(proposal.updated_at),
                proposal.selected_idea_id,
                proposal.generated_sections,
                proposal.compiled_markdown # Added
            ))
            conn.commit()
            logger.info(f"Saved Proposal with ID: {proposal.id}")
        except sqlite3.Error as e:
            logger.error(f"Error saving Proposal {proposal.id}: {e}")
            raise
        # finally:
            # Don't close the connection here, especially for :memory:
            # if conn and self.sqlite_repo.db_path != ":memory:":
            #     conn.close()

    def get_by_id(self, proposal_id: str) -> Optional[Proposal]:
        """Get a Proposal by its ID."""
        sql = "SELECT * FROM proposals WHERE id = ?"
        conn = None
        try:
            conn = self.conn
            cursor = conn.cursor()
            cursor.execute(sql, (proposal_id,))
            row = cursor.fetchone()
            if row:
                logger.debug(f"Retrieved Proposal with ID: {proposal_id}")
                return self._row_to_proposal(row)
            else:
                logger.debug(f"Proposal with ID {proposal_id} not found.")
                return None
        except sqlite3.Error as e:
            logger.error(f"Error retrieving Proposal {proposal_id}: {e}")
            raise
        # finally:
            # Don't close connection

    def get_all(self) -> List[Proposal]:
        """Get all Proposals from the database."""
        sql = "SELECT * FROM proposals ORDER BY created_at DESC"
        proposals = []
        conn = None
        try:
            conn = self.conn
            cursor = conn.cursor()
            cursor.execute(sql)
            rows = cursor.fetchall()
            for row in rows:
                proposals.append(self._row_to_proposal(row))
            logger.info(f"Retrieved {len(proposals)} Proposals.")
            return proposals
        except sqlite3.Error as e:
            logger.error(f"Error retrieving all Proposals: {e}")
            raise
        # finally:
            # Don't close connection

    def update(self, proposal: Proposal) -> None:
        """Update a Proposal in the database."""
        sql = """
        UPDATE proposals
        SET title = ?, description = ?, status = ?, updated_at = ?,
            selected_idea_id = ?, generated_sections = ?, compiled_markdown = ?
        WHERE id = ?
        """
        # Ensure updated_at reflects the update time
        proposal.updated_at = datetime.now(timezone.utc)
        conn = None
        try:
            conn = self.conn
            cursor = conn.cursor()
            cursor.execute(sql, (
                proposal.title,
                proposal.description,
                proposal.status,
                dt_to_iso(proposal.updated_at),
                proposal.selected_idea_id,
                proposal.generated_sections,
                proposal.compiled_markdown, # Added
                proposal.id
            ))
            conn.commit()
            if cursor.rowcount == 0:
                 logger.warning(f"Attempted to update Proposal {proposal.id}, but it was not found.")
            else:
                logger.info(f"Updated Proposal with ID: {proposal.id}")
        except sqlite3.Error as e:
            logger.error(f"Error updating Proposal {proposal.id}: {e}")
            raise
        # finally:
            # Don't close connection

    def delete(self, proposal_id: str) -> None:
        """Delete a Proposal from the database (cascades to ideas/evaluations)."""
        sql = "DELETE FROM proposals WHERE id = ?"
        conn = None
        try:
            conn = self.conn
            # FKs should be enabled on connection creation now
            # conn.execute("PRAGMA foreign_keys = ON")
            cursor = conn.cursor()
            cursor.execute(sql, (proposal_id,))
            conn.commit()
            if cursor.rowcount == 0:
                logger.warning(f"Attempted to delete Proposal {proposal_id}, but it was not found.")
            else:
                logger.info(f"Deleted Proposal with ID: {proposal_id}")
        except sqlite3.Error as e:
            logger.error(f"Error deleting Proposal {proposal_id}: {e}")
            raise
        # finally:
            # Don't close connection


class IdeaRepository:
    """Repository for Idea data operations."""

    def __init__(self, connection: sqlite3.Connection):
        """Initialize with a SQLite database connection."""
        self.conn = connection

    def _row_to_idea(self, row: sqlite3.Row) -> Idea:
        """Maps a database row to an Idea object."""
        return Idea(
            id=row['id'],
            title=row['title'],
            description=row['description'],
            proposal_id=row['proposal_id'],
            created_at=iso_to_dt(row['created_at'])
            # Note: evaluations are not loaded here by default
        )

    def save(self, idea: Idea) -> None:
        """Save an Idea to the database."""
        sql = """
        INSERT INTO ideas (id, title, description, proposal_id, created_at)
        VALUES (?, ?, ?, ?, ?)
        """
        conn = None
        try:
            conn = self.conn
            cursor = conn.cursor()
            cursor.execute(sql, (
                idea.id,
                idea.title,
                idea.description,
                idea.proposal_id,
                dt_to_iso(idea.created_at)
            ))
            conn.commit()
            logger.info(f"Saved Idea with ID: {idea.id} for Proposal {idea.proposal_id}")
        except sqlite3.Error as e:
            logger.error(f"Error saving Idea {idea.id}: {e}")
            raise
        # finally:
            # Don't close connection

    def get_by_id(self, idea_id: str) -> Optional[Idea]:
        """Get an Idea by its ID."""
        sql = "SELECT * FROM ideas WHERE id = ?"
        conn = None
        try:
            conn = self.conn
            cursor = conn.cursor()
            cursor.execute(sql, (idea_id,))
            row = cursor.fetchone()
            if row:
                logger.debug(f"Retrieved Idea with ID: {idea_id}")
                return self._row_to_idea(row)
            else:
                logger.debug(f"Idea with ID {idea_id} not found.")
                return None
        except sqlite3.Error as e:
            logger.error(f"Error retrieving Idea {idea_id}: {e}")
            raise
        # finally:
            # Don't close connection

    def get_by_proposal_id(self, proposal_id: str) -> List[Idea]:
        """Get all Ideas for a specific Proposal."""
        sql = "SELECT * FROM ideas WHERE proposal_id = ? ORDER BY created_at ASC"
        ideas = []
        conn = None
        try:
            conn = self.conn
            cursor = conn.cursor()
            cursor.execute(sql, (proposal_id,))
            rows = cursor.fetchall()
            for row in rows:
                ideas.append(self._row_to_idea(row))
            logger.info(f"Retrieved {len(ideas)} Ideas for Proposal {proposal_id}.")
            return ideas
        except sqlite3.Error as e:
            logger.error(f"Error retrieving Ideas for Proposal {proposal_id}: {e}")
            raise
        # finally:
            # Don't close connection

    def update(self, idea: Idea) -> None:
        """Update an Idea in the database."""
        sql = """
        UPDATE ideas
        SET title = ?, description = ?
        WHERE id = ?
        """
        conn = None
        try:
            conn = self.conn
            cursor = conn.cursor()
            cursor.execute(sql, (
                idea.title,
                idea.description,
                idea.id
            ))
            conn.commit()
            if cursor.rowcount == 0:
                 logger.warning(f"Attempted to update Idea {idea.id}, but it was not found.")
            else:
                logger.info(f"Updated Idea with ID: {idea.id}")
        except sqlite3.Error as e:
            logger.error(f"Error updating Idea {idea.id}: {e}")
            raise
        # finally:
            # Don't close connection

    def delete(self, idea_id: str) -> None:
        """Delete an Idea from the database (cascades evaluations)."""
        sql = "DELETE FROM ideas WHERE id = ?"
        conn = None
        try:
            conn = self.conn
            # FKs should be enabled on connection creation now
            # conn.execute("PRAGMA foreign_keys = ON")
            cursor = conn.cursor()
            cursor.execute(sql, (idea_id,))
            conn.commit()
            if cursor.rowcount == 0:
                logger.warning(f"Attempted to delete Idea {idea_id}, but it was not found.")
            else:
                logger.info(f"Deleted Idea with ID: {idea_id}")
        except sqlite3.Error as e:
            logger.error(f"Error deleting Idea {idea_id}: {e}")
            raise
        # finally:
            # Don't close connection


class EvaluationRepository:
    """Repository for Evaluation data operations."""

    def __init__(self, connection: sqlite3.Connection):
        """Initialize with a SQLite database connection."""
        self.conn = connection

    def _row_to_evaluation(self, row: sqlite3.Row) -> Evaluation:
        """Maps a database row to an Evaluation object."""
        return Evaluation(
            id=row['id'],
            evaluator=row['evaluator'],
            score=row['score'],
            feedback=row['feedback'],
            created_at=iso_to_dt(row['created_at']),
            proposal_id=row['proposal_id'],
            idea_id=row['idea_id']
        )

    def save(self, evaluation: Evaluation) -> None:
        """Save an Evaluation to the database."""
        sql = """
        INSERT INTO evaluations (id, evaluator, score, feedback, created_at, proposal_id, idea_id)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        conn = None
        try:
            conn = self.conn
            cursor = conn.cursor()
            cursor.execute(sql, (
                evaluation.id,
                evaluation.evaluator,
                evaluation.score,
                evaluation.feedback,
                dt_to_iso(evaluation.created_at),
                evaluation.proposal_id,
                evaluation.idea_id
            ))
            conn.commit()
            target_id = evaluation.proposal_id or evaluation.idea_id
            target_type = "Proposal" if evaluation.proposal_id else "Idea"
            logger.info(f"Saved Evaluation {evaluation.id} for {target_type} {target_id}")
        except sqlite3.Error as e:
            logger.error(f"Error saving Evaluation {evaluation.id}: {e}")
            raise
        # finally:
            # Don't close connection

    def get_by_id(self, evaluation_id: str) -> Optional[Evaluation]:
        """Get an Evaluation by its ID."""
        sql = "SELECT * FROM evaluations WHERE id = ?"
        conn = None
        try:
            conn = self.conn
            cursor = conn.cursor()
            cursor.execute(sql, (evaluation_id,))
            row = cursor.fetchone()
            if row:
                logger.debug(f"Retrieved Evaluation with ID: {evaluation_id}")
                return self._row_to_evaluation(row)
            else:
                logger.debug(f"Evaluation with ID {evaluation_id} not found.")
                return None
        except sqlite3.Error as e:
            logger.error(f"Error retrieving Evaluation {evaluation_id}: {e}")
            raise
        # finally:
            # Don't close connection

    def get_by_proposal_id(self, proposal_id: str) -> List[Evaluation]:
        """Get all Evaluations for a specific Proposal."""
        sql = "SELECT * FROM evaluations WHERE proposal_id = ? ORDER BY created_at ASC"
        evaluations = []
        conn = None
        try:
            conn = self.conn
            cursor = conn.cursor()
            cursor.execute(sql, (proposal_id,))
            rows = cursor.fetchall()
            for row in rows:
                evaluations.append(self._row_to_evaluation(row))
            logger.info(f"Retrieved {len(evaluations)} Evaluations for Proposal {proposal_id}.")
            return evaluations
        except sqlite3.Error as e:
            logger.error(f"Error retrieving Evaluations for Proposal {proposal_id}: {e}")
            raise
        # finally:
            # Don't close connection

    def get_by_idea_id(self, idea_id: str) -> List[Evaluation]:
        """Get all Evaluations for a specific Idea."""
        sql = "SELECT * FROM evaluations WHERE idea_id = ? ORDER BY created_at ASC"
        evaluations = []
        conn = None
        try:
            conn = self.conn
            cursor = conn.cursor()
            cursor.execute(sql, (idea_id,))
            rows = cursor.fetchall()
            for row in rows:
                evaluations.append(self._row_to_evaluation(row))
            logger.info(f"Retrieved {len(evaluations)} Evaluations for Idea {idea_id}.")
            return evaluations
        except sqlite3.Error as e:
            logger.error(f"Error retrieving Evaluations for Idea {idea_id}: {e}")
            raise
        # finally:
            # Don't close connection

    def update(self, evaluation: Evaluation) -> None:
        """Update an Evaluation in the database."""
        sql = """
        UPDATE evaluations
        SET evaluator = ?, score = ?, feedback = ?
        WHERE id = ?
        """
        conn = None
        try:
            conn = self.conn
            cursor = conn.cursor()
            cursor.execute(sql, (
                evaluation.evaluator,
                evaluation.score,
                evaluation.feedback,
                evaluation.id
            ))
            conn.commit()
            if cursor.rowcount == 0:
                 logger.warning(f"Attempted to update Evaluation {evaluation.id}, but it was not found.")
            else:
                logger.info(f"Updated Evaluation with ID: {evaluation.id}")
        except sqlite3.Error as e:
            logger.error(f"Error updating Evaluation {evaluation.id}: {e}")
            raise
        # finally:
            # Don't close connection

    def delete(self, evaluation_id: str) -> None:
        """Delete an Evaluation from the database."""
        sql = "DELETE FROM evaluations WHERE id = ?"
        conn = None
        try:
            conn = self.conn
            cursor = conn.cursor()
            cursor.execute(sql, (evaluation_id,))
            conn.commit()
            if cursor.rowcount == 0:
                logger.warning(f"Attempted to delete Evaluation {evaluation_id}, but it was not found.")
            else:
                logger.info(f"Deleted Evaluation with ID: {evaluation_id}")
        except sqlite3.Error as e:
            logger.error(f"Error deleting Evaluation {evaluation_id}: {e}")
            raise
        # finally:
            # Don't close connection