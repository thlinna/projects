"""Tests for the Workflow Orchestration Layer."""

import pytest
import sqlite3 # For setting up mock repo connection

# Import models and repositories
from src.models.proposal import Proposal
from src.data_storage.sqlite_repository import (
    ProposalRepository, IdeaRepository, EvaluationRepository
)

# Import agents (using existing implementations for testing workflow)
from src.agents.base_agent import Agent
from src.agents.creative_ideator import CreativeIdeatorAgent
from src.agents.practical_judge import PracticalJudgeAgent
from src.agents.programme_expert import ProgrammeExpertAgent
from src.agents.startup_founder import StartupFounderAgent
from src.agents.proposal_writer import ProposalWriterAgent

# Import the WorkflowEngine (will fail initially)
from src.workflow.workflow_engine import WorkflowEngine


# --- Fixtures ---

@pytest.fixture
def test_db_connection():
    """Provides an initialized in-memory SQLite connection for workflow tests."""
    conn = sqlite3.connect(":memory:", detect_types=sqlite3.PARSE_DECLTYPES)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    # Use the create_tables function from test_data_storage or redefine here
    # For simplicity, redefine here:
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
    yield conn
    conn.close()

@pytest.fixture
def proposal_repo(test_db_connection):
    return ProposalRepository(test_db_connection)

@pytest.fixture
def idea_repo(test_db_connection):
    return IdeaRepository(test_db_connection)

@pytest.fixture
def evaluation_repo(test_db_connection):
    return EvaluationRepository(test_db_connection)

@pytest.fixture(scope="function") # Ensure fresh agents for each test
def agents():
    """Provides a dictionary of all initialized agents."""
    return {
        "ideator": CreativeIdeatorAgent(),
        "judge": PracticalJudgeAgent(),
        "expert": ProgrammeExpertAgent(),
        "founder": StartupFounderAgent(),
        "writer": ProposalWriterAgent(),
    }

@pytest.fixture
def workflow_engine(proposal_repo, idea_repo, evaluation_repo, agents):
    """Provides an initialized WorkflowEngine instance."""
    return WorkflowEngine(
        agents=agents,
        proposal_repo=proposal_repo,
        idea_repo=idea_repo,
        evaluation_repo=evaluation_repo
    )


# --- Tests ---

class TestWorkflowEngine:
    """Tests for the WorkflowEngine class."""

    def test_workflow_engine_initialization(self, workflow_engine, agents):
        """Test that the engine initializes correctly with agents and repos."""
        assert workflow_engine is not None
        assert workflow_engine.agents == agents
        assert workflow_engine.proposal_repo is not None
        assert workflow_engine.idea_repo is not None
        assert workflow_engine.evaluation_repo is not None

    def test_register_agent(self, workflow_engine):
        """Test registering a new agent."""
        # Assuming a method to register agents exists
        new_agent = CreativeIdeatorAgent(name="Ideator 2")
        workflow_engine.register_agent("ideator2", new_agent)
        assert "ideator2" in workflow_engine.agents
        assert workflow_engine.agents["ideator2"] == new_agent

    def test_run_initial_ideation_cycle(self, workflow_engine, proposal_repo):
        """Test running a basic workflow cycle: create proposal -> ideate."""
        # 1. Start a new proposal process
        initial_topic = "Test Topic for Workflow"
        proposal = workflow_engine.start_new_proposal(initial_topic)

        assert proposal is not None
        assert proposal.title == f"Proposal for {initial_topic}" # Assuming default title
        assert proposal.status == "ideation" # Assuming status is updated

        # Verify proposal is saved
        saved_proposal = proposal_repo.get_by_id(proposal.id)
        assert saved_proposal is not None
        assert saved_proposal.id == proposal.id

        # 2. Run one step of the workflow (should trigger ideation)
        # Assuming a method like run_step() or run_cycle()
        workflow_engine.run_step(proposal.id)

        # Verify: Check if ideas were generated and saved (minimal check)
        # This requires the engine to call the ideator and save results
        # We expect this test to fail until run_step is implemented
        ideas = workflow_engine.idea_repo.get_by_proposal_id(proposal.id)
        assert len(ideas) > 0
        assert ideas[0].proposal_id == proposal.id

    def test_run_ideation_critique_cycle(self, workflow_engine, proposal_repo, idea_repo, evaluation_repo):
        """Test ideation followed by critique."""
        # 1. Start and run ideation
        initial_topic = "Test Topic for Critique"
        proposal = workflow_engine.start_new_proposal(initial_topic)
        workflow_engine.run_step(proposal.id) # Assume this runs ideation

        # Verify ideas exist
        ideas = idea_repo.get_by_proposal_id(proposal.id)
        assert len(ideas) > 0
        original_idea = ideas[0]

        # 2. Run another step (should trigger critique/judgement)
        workflow_engine.run_step(proposal.id)

        # Verify: Check if evaluations were created for the idea
        # We expect this test to fail until run_step handles critique
        evaluations = evaluation_repo.get_by_idea_id(original_idea.id)
        assert len(evaluations) > 0
        assert evaluations[0].evaluator == "Practical Judge" # Based on agent fixture
        assert evaluations[0].idea_id == original_idea.id

    # Add more tests later for:
    # - Iteration loop (multiple cycles)
    # - Convergence criteria
    # - Handling different proposal statuses
    # - Integration with all 5 agents
    # - Final proposal compilation trigger

    def test_run_full_cycle_to_completion(self, workflow_engine, proposal_repo, idea_repo, evaluation_repo):
        """Test a simplified full workflow leading to a final proposal."""
        # 1. Start
        topic = "Full Cycle Test"
        proposal = workflow_engine.start_new_proposal(topic)
        assert proposal.status == "ideation"

        # 2. Ideation
        workflow_engine.run_step(proposal.id)
        proposal = proposal_repo.get_by_id(proposal.id) # Refresh proposal state
        assert proposal.status == "critique"
        ideas = idea_repo.get_by_proposal_id(proposal.id)
        assert len(ideas) > 0

        # 3. Critique
        workflow_engine.run_step(proposal.id)
        proposal = proposal_repo.get_by_id(proposal.id)
        assert proposal.status == "refinement" # Assume critique leads to refinement
        evaluations = evaluation_repo.get_by_idea_id(ideas[0].id) # Check first idea
        assert len(evaluations) > 0

        # 4. Refinement (Simplified: Assume judge improves, then writer takes over)
        # In a real scenario, this would involve more agent calls (expert, founder)
        # and potentially looping based on evaluation scores.
        # For this test, we'll just simulate the state transition.
        workflow_engine.run_step(proposal.id) # Assume this runs refinement (e.g., judge improves)
        proposal = proposal_repo.get_by_id(proposal.id)
        assert proposal.status == "writing" # Assume refinement leads to writing

        # 5. Writing
        workflow_engine.run_step(proposal.id) # Assume this runs writing (writer agent)
        proposal = proposal_repo.get_by_id(proposal.id)
        # Check if proposal description or a dedicated field was updated
        # For now, just check status transition
        assert proposal.status == "finalizing" # Assume writing leads to finalizing

        # 6. Finalizing (Compile)
        workflow_engine.run_step(proposal.id) # Assume this compiles the final doc
        proposal = proposal_repo.get_by_id(proposal.id)
        # Check final status and potentially existence of output file/data
        assert proposal.status == "completed" # Assume final state is 'completed'
        # A real test might check for the generated markdown file or content