"""Tests for the Data Storage Layer using SQLite."""

import pytest
import os
import sqlite3
from datetime import datetime
import uuid

# Import our models
from src.models.proposal import Proposal
from src.models.idea import Idea
from src.models.evaluation import Evaluation

# Import the repository classes that are still needed
from src.data_storage.sqlite_repository import (
    ProposalRepository,
    IdeaRepository,
    EvaluationRepository
)
# The _initialize_database_on_connection is no longer needed as
# table creation is handled by the local create_tables helper.


@pytest.fixture
def test_db_path():
    """Fixture to provide a test database path."""
    # Use an in-memory database for testing
    return ":memory:"


# Helper function (can be moved to a conftest.py or test utils later)
def create_tables(conn):
    """Creates the necessary tables on the given connection."""
    create_proposals_table = """
    CREATE TABLE proposals (
        id TEXT PRIMARY KEY, title TEXT NOT NULL, description TEXT NOT NULL,
        status TEXT NOT NULL, created_at TEXT NOT NULL, updated_at TEXT NOT NULL
    );"""
    create_ideas_table = """
    CREATE TABLE ideas (
        id TEXT PRIMARY KEY, title TEXT NOT NULL, description TEXT NOT NULL,
        proposal_id TEXT NOT NULL, created_at TEXT NOT NULL,
        FOREIGN KEY (proposal_id) REFERENCES proposals (id) ON DELETE CASCADE
    );"""
    create_evaluations_table = """
    CREATE TABLE evaluations (
        id TEXT PRIMARY KEY, evaluator TEXT NOT NULL, score INTEGER,
        feedback TEXT NOT NULL, created_at TEXT NOT NULL, proposal_id TEXT, idea_id TEXT,
        FOREIGN KEY (proposal_id) REFERENCES proposals (id) ON DELETE CASCADE,
        FOREIGN KEY (idea_id) REFERENCES ideas (id) ON DELETE CASCADE,
        CHECK (proposal_id IS NOT NULL OR idea_id IS NOT NULL),
        CHECK (proposal_id IS NULL OR idea_id IS NULL)
    );"""
    cursor = conn.cursor()
    cursor.execute(create_proposals_table)
    cursor.execute(create_ideas_table)
    cursor.execute(create_evaluations_table)
    conn.commit()


@pytest.fixture
def db_connection(test_db_path):
    """Fixture to provide an initialized in-memory SQLite connection."""
    conn = sqlite3.connect(test_db_path, detect_types=sqlite3.PARSE_DECLTYPES)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    create_tables(conn) # Create tables directly on this connection
    yield conn
    conn.close() # Close the connection after the test


@pytest.fixture
def proposal_repo(db_connection): # Use the connection fixture
    """Fixture to provide a ProposalRepository instance."""
    # Pass the connection directly (requires ProposalRepository update)
    return ProposalRepository(db_connection)


@pytest.fixture
def idea_repo(db_connection): # Use the connection fixture
    """Fixture to provide an IdeaRepository instance."""
    # Pass the connection directly (requires IdeaRepository update)
    return IdeaRepository(db_connection)


@pytest.fixture
def evaluation_repo(db_connection): # Use the connection fixture
    """Fixture to provide an EvaluationRepository instance."""
    # Pass the connection directly (requires EvaluationRepository update)
    return EvaluationRepository(db_connection)


@pytest.fixture
def sample_proposal():
    """Fixture to provide a sample Proposal."""
    return Proposal(
        title="AI-Driven Healthcare Solutions",
        description="A proposal for AI-driven healthcare solutions in the EU"
    )


@pytest.fixture
def sample_idea(sample_proposal):
    """Fixture to provide a sample Idea."""
    return Idea(
        title="Remote Patient Monitoring",
        description="Use AI to monitor patients remotely",
        proposal_id=sample_proposal.id
    )


@pytest.fixture
def sample_evaluation(sample_proposal):
    """Fixture to provide a sample Evaluation for a Proposal."""
    return Evaluation(
        evaluator="Programme Expert",
        feedback="Strong proposal with good alignment to EU priorities",
        score=85,
        proposal_id=sample_proposal.id
    )


class TestSQLiteRepository:
    """Tests for the SQLiteRepository class."""
    
    # This test might become redundant or needs adjustment as initialization
    # is now handled directly in the db_connection fixture.
    # We can test if the connection fixture works as expected.
    def test_db_connection_fixture(self, db_connection):
        """Test that the db_connection fixture provides a valid connection with tables."""
        assert db_connection is not None
        cursor = db_connection.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = {row[0] for row in cursor.fetchall()}
        assert "proposals" in tables
        assert "ideas" in tables
        assert "evaluations" in tables


class TestProposalRepository:
    """Tests for the ProposalRepository class."""
    
    def test_save_proposal(self, proposal_repo, sample_proposal):
        """Test that a Proposal can be saved to the database."""
        # Save the proposal
        proposal_repo.save(sample_proposal)
        
        # Retrieve the proposal by ID
        retrieved_proposal = proposal_repo.get_by_id(sample_proposal.id)
        
        # Verify the retrieved proposal matches the original
        assert retrieved_proposal is not None
        assert retrieved_proposal.id == sample_proposal.id
        assert retrieved_proposal.title == sample_proposal.title
        assert retrieved_proposal.description == sample_proposal.description
    
    def test_get_all_proposals(self, proposal_repo, sample_proposal):
        """Test that all Proposals can be retrieved from the database."""
        # Save a proposal
        proposal_repo.save(sample_proposal)
        
        # Create and save another proposal
        another_proposal = Proposal(
            title="Digital Education Platform",
            description="A proposal for a digital education platform in the EU"
        )
        proposal_repo.save(another_proposal)
        
        # Retrieve all proposals
        proposals = proposal_repo.get_all()
        
        # Verify we have the expected number of proposals
        assert len(proposals) == 2
        
        # Verify the proposals are in the list
        proposal_ids = [p.id for p in proposals]
        assert sample_proposal.id in proposal_ids
        assert another_proposal.id in proposal_ids
    
    def test_update_proposal(self, proposal_repo, sample_proposal):
        """Test that a Proposal can be updated in the database."""
        # Save the proposal
        proposal_repo.save(sample_proposal)
        
        # Modify the proposal
        sample_proposal.title = "Updated: AI-Driven Healthcare Solutions"
        sample_proposal.description = "Updated description for AI-driven healthcare"
        
        # Update the proposal in the database
        proposal_repo.update(sample_proposal)
        
        # Retrieve the updated proposal
        updated_proposal = proposal_repo.get_by_id(sample_proposal.id)
        
        # Verify the changes were saved
        assert updated_proposal.title == "Updated: AI-Driven Healthcare Solutions"
        assert updated_proposal.description == "Updated description for AI-driven healthcare"
    
    def test_delete_proposal(self, proposal_repo, sample_proposal):
        """Test that a Proposal can be deleted from the database."""
        # Save the proposal
        proposal_repo.save(sample_proposal)
        
        # Delete the proposal
        proposal_repo.delete(sample_proposal.id)
        
        # Try to retrieve the deleted proposal
        deleted_proposal = proposal_repo.get_by_id(sample_proposal.id)
        
        # Verify the proposal is no longer in the database
        assert deleted_proposal is None


class TestIdeaRepository:
    """Tests for the IdeaRepository class."""
    
    # Add proposal_repo fixture to save the parent proposal first
    def test_save_idea(self, proposal_repo, idea_repo, sample_proposal, sample_idea):
        """Test that an Idea can be saved to the database."""
        # Ensure the proposal exists in the DB first
        proposal_repo.save(sample_proposal)
        # Now save the idea
        idea_repo.save(sample_idea)
        
        # Retrieve the idea by ID
        retrieved_idea = idea_repo.get_by_id(sample_idea.id)
        
        # Verify the retrieved idea matches the original
        assert retrieved_idea is not None
        assert retrieved_idea.id == sample_idea.id
        assert retrieved_idea.title == sample_idea.title
        assert retrieved_idea.description == sample_idea.description
        assert retrieved_idea.proposal_id == sample_idea.proposal_id
    
    # Add proposal_repo fixture
    def test_get_ideas_by_proposal(self, proposal_repo, idea_repo, sample_proposal, sample_idea):
        """Test that Ideas can be retrieved by proposal ID."""
        # Ensure the proposal exists
        proposal_repo.save(sample_proposal)
        # Save the idea
        idea_repo.save(sample_idea)
        
        # Create and save another idea for the same proposal
        another_idea = Idea(
            title="AI Diagnostic Tools",
            description="AI tools for medical diagnostics",
            proposal_id=sample_proposal.id
        )
        idea_repo.save(another_idea)
        
        # Retrieve ideas for the proposal
        ideas = idea_repo.get_by_proposal_id(sample_proposal.id)
        
        # Verify we have the expected number of ideas
        assert len(ideas) == 2
        
        # Verify the ideas are in the list
        idea_ids = [i.id for i in ideas]
        assert sample_idea.id in idea_ids
        assert another_idea.id in idea_ids


class TestEvaluationRepository:
    """Tests for the EvaluationRepository class."""
    
    # Add proposal_repo fixture
    def test_save_evaluation(self, proposal_repo, evaluation_repo, sample_proposal, sample_evaluation):
        """Test that an Evaluation can be saved to the database."""
        # Ensure the proposal exists
        proposal_repo.save(sample_proposal)
        # Save the evaluation
        evaluation_repo.save(sample_evaluation)
        
        # Retrieve the evaluation by ID
        retrieved_evaluation = evaluation_repo.get_by_id(sample_evaluation.id)
        
        # Verify the retrieved evaluation matches the original
        assert retrieved_evaluation is not None
        assert retrieved_evaluation.id == sample_evaluation.id
        assert retrieved_evaluation.evaluator == sample_evaluation.evaluator
        assert retrieved_evaluation.feedback == sample_evaluation.feedback
        assert retrieved_evaluation.score == sample_evaluation.score
        assert retrieved_evaluation.proposal_id == sample_evaluation.proposal_id
    
    # Add proposal_repo fixture
    def test_get_evaluations_by_proposal(self, proposal_repo, evaluation_repo, sample_proposal, sample_evaluation):
        """Test that Evaluations can be retrieved by proposal ID."""
        # Ensure the proposal exists
        proposal_repo.save(sample_proposal)
        # Save the evaluation
        evaluation_repo.save(sample_evaluation)
        
        # Create and save another evaluation for the same proposal
        another_evaluation = Evaluation(
            evaluator="Startup Founder",
            feedback="Good market potential but needs refinement",
            score=75,
            proposal_id=sample_proposal.id
        )
        evaluation_repo.save(another_evaluation)
        
        # Retrieve evaluations for the proposal
        evaluations = evaluation_repo.get_by_proposal_id(sample_proposal.id)
        
        # Verify we have the expected number of evaluations
        assert len(evaluations) == 2
        
        # Verify the evaluations are in the list
        evaluation_ids = [e.id for e in evaluations]
        assert sample_evaluation.id in evaluation_ids
        assert another_evaluation.id in evaluation_ids
    
    # Add proposal_repo and idea_repo fixtures
    def test_get_evaluations_by_idea(self, proposal_repo, idea_repo, evaluation_repo, sample_proposal, sample_idea):
        """Test that Evaluations can be retrieved by idea ID."""
        # Ensure the proposal and idea exist first
        proposal_repo.save(sample_proposal)
        idea_repo.save(sample_idea)

        # Create an evaluation for the idea
        idea_evaluation = Evaluation(
            evaluator="Practical Judge",
            feedback="Innovative idea with practical applications",
            score=90,
            idea_id=sample_idea.id # Link to the saved idea
        )

        # Save the evaluation
        evaluation_repo.save(idea_evaluation)
        
        # Retrieve evaluations for the idea
        evaluations = evaluation_repo.get_by_idea_id(sample_idea.id)
        
        # Verify we have the expected number of evaluations
        assert len(evaluations) == 1
        
        # Verify the evaluation is in the list
        assert evaluations[0].id == idea_evaluation.id