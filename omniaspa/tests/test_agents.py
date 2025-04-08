"""Tests for the Agent Collaboration Layer."""

import pytest
from abc import ABC, abstractmethod

# Import the base agent class (will fail initially)
from src.agents.base_agent import Agent
# Import specific agent implementations later as needed
from src.agents.programme_expert import ProgrammeExpertAgent
from src.agents.creative_ideator import CreativeIdeatorAgent
from src.agents.startup_founder import StartupFounderAgent
from src.agents.practical_judge import PracticalJudgeAgent
from src.agents.proposal_writer import ProposalWriterAgent # Will fail until implemented


# Define a concrete subclass for testing the abstract Agent class
class ConcreteTestAgent(Agent):
    """A concrete agent implementation for testing purposes."""
    def __init__(self, name: str = "TestAgent"):
        super().__init__(name)

    def execute_task(self, task_details: dict) -> dict:
        """Simulates executing a task."""
        # Simple echo task for testing
        result = {"status": "completed", "output": f"Task executed by {self.name} with details: {task_details}"}
        self.log_interaction(task_details, result)
        return result

    def get_capabilities(self) -> list[str]:
        """Returns the capabilities of this test agent."""
        return ["test_capability_1", "test_capability_2"]


class TestBaseAgent:
    """Tests for the abstract base Agent class."""

    def test_agent_initialization(self):
        """Test that an agent can be initialized with a name."""
        agent_name = "MyTestAgent"
        agent = ConcreteTestAgent(name=agent_name)
        assert agent.name == agent_name
        assert agent.interaction_history == []

    def test_agent_requires_name(self):
        """Test that initializing an agent without a name might use a default or raise error (design choice)."""
        # Assuming a default name is provided by ConcreteTestAgent if none is given
        agent = ConcreteTestAgent()
        assert agent.name == "TestAgent" # Default name from ConcreteTestAgent

    def test_abstract_methods_exist(self):
        """Check if necessary abstract methods are defined (implicitly tested by subclassing)."""
        # Ensure Agent itself cannot be instantiated
        with pytest.raises(TypeError):
            Agent("AbstractAgent") # Cannot instantiate abstract class

        # Check existence of abstract methods by trying to create a subclass without implementing them
        class IncompleteAgent(Agent):
            def __init__(self, name: str):
                super().__init__(name)
            # Missing execute_task and get_capabilities

        with pytest.raises(TypeError):
            IncompleteAgent("Incomplete")

    def test_execute_task_signature(self):
        """Test the signature and basic execution of the execute_task method."""
        agent = ConcreteTestAgent()
        task = {"instruction": "Perform test action"}
        result = agent.execute_task(task)
        assert isinstance(result, dict)
        assert result["status"] == "completed"
        assert "Task executed by TestAgent" in result["output"]

    def test_get_capabilities_signature(self):
        """Test the signature and return type of get_capabilities."""
        agent = ConcreteTestAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert "test_capability_1" in capabilities

    def test_log_interaction(self):
        """Test that interactions are logged correctly."""
        agent = ConcreteTestAgent()
        task = {"input": "test input"}
        result = {"output": "test output"}

        # Simulate logging via execute_task or directly if log_interaction is public
        agent.log_interaction(task, result) # Assuming log_interaction is accessible for testing

        assert len(agent.interaction_history) == 1
        log_entry = agent.interaction_history[0]
        assert "timestamp" in log_entry
        assert log_entry["input"] == task
        assert log_entry["output"] == result


# Add tests for Agent Communication Framework later (e.g., message passing, shared state)

# Add tests for specific agent implementations later (e.g., ProgrammeExpertAgent)

class TestProgrammeExpertAgent:
    """Tests for the ProgrammeExpertAgent."""

    def test_programme_expert_initialization(self):
        """Test initialization of the ProgrammeExpertAgent."""
        agent = ProgrammeExpertAgent()
        assert agent.name == "Programme Expert" # Default name assumption

    def test_programme_expert_capabilities(self):
        """Test the specific capabilities of the ProgrammeExpertAgent."""
        agent = ProgrammeExpertAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert "evaluate_criteria" in capabilities
        assert "provide_guidance" in capabilities
        # Add more expected capabilities based on PRD

    def test_programme_expert_execute_task_evaluate(self):
        """Test a basic evaluation task execution."""
        agent = ProgrammeExpertAgent()
        # Simulate task details for evaluation
        task_details = {
            "type": "evaluate_criteria",
            "proposal_data": {"title": "Test Proposal", "description": "..."}
        }
        result = agent.execute_task(task_details)
        assert result["status"] == "completed" # Or appropriate status
        assert "evaluation_score" in result # Example expected output
        assert "feedback" in result

    def test_programme_expert_execute_task_guidance(self):
        """Test a basic guidance task execution."""
        agent = ProgrammeExpertAgent()
        # Simulate task details for guidance
        task_details = {
            "type": "provide_guidance",
            "topic": "Alignment with EU Green Deal"
        }
        result = agent.execute_task(task_details)
        assert result["status"] == "completed"
        assert "guidance_text" in result # Example expected output


class TestCreativeIdeatorAgent:
    """Tests for the CreativeIdeatorAgent."""

    def test_creative_ideator_initialization(self):
        """Test initialization of the CreativeIdeatorAgent."""
        agent = CreativeIdeatorAgent()
        assert agent.name == "Creative Ideator" # Default name assumption

    def test_creative_ideator_capabilities(self):
        """Test the specific capabilities of the CreativeIdeatorAgent."""
        agent = CreativeIdeatorAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert "generate_ideas" in capabilities
        # Add more expected capabilities based on PRD

    def test_creative_ideator_execute_task_generate(self):
        """Test a basic idea generation task execution."""
        agent = CreativeIdeatorAgent()
        # Simulate task details for generation
        task_details = {
            "type": "generate_ideas",
            "topic": "Sustainable Urban Mobility",
            "quantity": 3 # Request 3 ideas
        }
        result = agent.execute_task(task_details)
        assert result["status"] == "completed"
        assert "generated_ideas" in result
        assert isinstance(result["generated_ideas"], list)
        # Check if the number of ideas matches the request (minimal check)
        # A more robust test would check the structure of each idea dict
        assert len(result["generated_ideas"]) >= 1 # Expect at least one idea


class TestStartupFounderAgent:
    """Tests for the StartupFounderAgent."""

    def test_startup_founder_initialization(self):
        """Test initialization of the StartupFounderAgent."""
        agent = StartupFounderAgent()
        assert agent.name == "Startup Founder" # Default name assumption

    def test_startup_founder_capabilities(self):
        """Test the specific capabilities of the StartupFounderAgent."""
        agent = StartupFounderAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert "assess_stakeholders" in capabilities
        assert "validate_best_practices" in capabilities
        assert "assess_implementation_path" in capabilities
        # Add more expected capabilities based on PRD

    def test_startup_founder_execute_task_assess_stakeholders(self):
        """Test a basic stakeholder assessment task execution."""
        agent = StartupFounderAgent()
        # Simulate task details for assessment
        task_details = {
            "type": "assess_stakeholders",
            "proposal_data": {"title": "Test Proposal", "area": "Healthcare AI"}
        }
        result = agent.execute_task(task_details)
        assert result["status"] == "completed"
        assert "stakeholder_analysis" in result # Example expected output
        assert isinstance(result["stakeholder_analysis"], dict)

    def test_startup_founder_execute_task_validate_practices(self):
        """Test a basic best practice validation task execution."""
        agent = StartupFounderAgent()
        # Simulate task details for validation
        task_details = {
            "type": "validate_best_practices",
            "proposal_section": "Work Package 1 Description"
        }
        result = agent.execute_task(task_details)
        assert result["status"] == "completed"
        assert "validation_feedback" in result # Example expected output


class TestPracticalJudgeAgent:
    """Tests for the PracticalJudgeAgent."""

    def test_practical_judge_initialization(self):
        """Test initialization of the PracticalJudgeAgent."""
        agent = PracticalJudgeAgent()
        assert agent.name == "Practical Judge" # Default name assumption

    def test_practical_judge_capabilities(self):
        """Test the specific capabilities of the PracticalJudgeAgent."""
        agent = PracticalJudgeAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert "critique_idea" in capabilities
        assert "improve_idea" in capabilities
        # Add more expected capabilities based on PRD

    def test_practical_judge_execute_task_critique(self):
        """Test a basic critique task execution."""
        agent = PracticalJudgeAgent()
        # Simulate task details for critique
        task_details = {
            "type": "critique_idea",
            "idea_data": {"title": "Test Idea", "description": "..."}
        }
        result = agent.execute_task(task_details)
        assert result["status"] == "completed"
        assert "critique" in result # Example expected output
        assert "score" in result # Example expected output

    def test_practical_judge_execute_task_improve(self):
        """Test a basic improvement task execution."""
        agent = PracticalJudgeAgent()
        # Simulate task details for improvement
        task_details = {
            "type": "improve_idea",
            "idea_data": {"title": "Test Idea", "description": "Needs work"}
        }
        result = agent.execute_task(task_details)
        assert result["status"] == "completed"
        assert "improved_idea" in result # Example expected output
        assert isinstance(result["improved_idea"], dict)
        # Check if description is different (minimal check)
        assert result["improved_idea"].get("description") != "Needs work"


class TestProposalWriterAgent:
    """Tests for the ProposalWriterAgent."""

    def test_proposal_writer_initialization(self):
        """Test initialization of the ProposalWriterAgent."""
        agent = ProposalWriterAgent()
        assert agent.name == "Proposal Writer" # Default name assumption

    def test_proposal_writer_capabilities(self):
        """Test the specific capabilities of the ProposalWriterAgent."""
        agent = ProposalWriterAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert "write_section" in capabilities
        assert "compile_final_proposal" in capabilities
        # Add more expected capabilities based on PRD

    def test_proposal_writer_execute_task_write_section(self):
        """Test a basic section writing task execution."""
        agent = ProposalWriterAgent()
        # Simulate task details for writing a section
        task_details = {
            "type": "write_section",
            "section_name": "Introduction",
            "input_data": {"key_points": ["Point 1", "Point 2"]}
        }
        result = agent.execute_task(task_details)
        assert result["status"] == "completed"
        assert "section_content" in result # Example expected output
        assert isinstance(result["section_content"], str)
        assert "Introduction" in result["section_content"] # Minimal check

    def test_proposal_writer_execute_task_compile(self):
        """Test a basic final proposal compilation task execution."""
        agent = ProposalWriterAgent()
        # Simulate task details for compilation
        task_details = {
            "type": "compile_final_proposal",
            "sections": {
                "Introduction": "Intro content...",
                "Methodology": "Methodology content..."
            }
        }
        result = agent.execute_task(task_details)
        assert result["status"] == "completed"
        assert "final_proposal_md" in result # Example expected output
        assert isinstance(result["final_proposal_md"], str)
        # Check if sections are included (minimal check)
        assert "Intro content..." in result["final_proposal_md"]
        assert "Methodology content..." in result["final_proposal_md"]