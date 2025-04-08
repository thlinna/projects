"""Tests for the core data structures."""

import pytest
from datetime import datetime
import uuid

# These imports will fail until we implement the models
from src.models.proposal import Proposal
from src.models.idea import Idea
from src.models.evaluation import Evaluation


class TestProposal:
    """Tests for the Proposal data structure."""

    def test_proposal_initialization(self):
        """Test that a Proposal can be initialized with the required attributes."""
        proposal_id = str(uuid.uuid4())
        title = "AI-Driven Healthcare Solutions"
        created_at = datetime.now()
        updated_at = datetime.now()
        status = "draft"
        description = "A proposal for AI-driven healthcare solutions in the EU"
        
        proposal = Proposal(
            id=proposal_id,
            title=title,
            created_at=created_at,
            updated_at=updated_at,
            status=status,
            description=description
        )
        
        assert proposal.id == proposal_id
        assert proposal.title == title
        assert proposal.created_at == created_at
        assert proposal.updated_at == updated_at
        assert proposal.status == status
        assert proposal.description == description
        assert proposal.ideas == []
        assert proposal.evaluations == []
    
    def test_proposal_add_idea(self):
        """Test that an Idea can be added to a Proposal."""
        proposal = Proposal(
            id=str(uuid.uuid4()),
            title="AI-Driven Healthcare Solutions",
            created_at=datetime.now(),
            updated_at=datetime.now(),
            status="draft",
            description="A proposal for AI-driven healthcare solutions in the EU"
        )
        
        idea = Idea(
            id=str(uuid.uuid4()),
            title="Remote Patient Monitoring",
            created_at=datetime.now(),
            description="Use AI to monitor patients remotely",
            proposal_id=proposal.id
        )
        
        proposal.add_idea(idea)
        
        assert len(proposal.ideas) == 1
        assert proposal.ideas[0] == idea
    
    def test_proposal_add_evaluation(self):
        """Test that an Evaluation can be added to a Proposal."""
        proposal = Proposal(
            id=str(uuid.uuid4()),
            title="AI-Driven Healthcare Solutions",
            created_at=datetime.now(),
            updated_at=datetime.now(),
            status="draft",
            description="A proposal for AI-driven healthcare solutions in the EU"
        )
        
        evaluation = Evaluation(
            id=str(uuid.uuid4()),
            created_at=datetime.now(),
            score=85,
            feedback="Strong proposal with good alignment to EU priorities",
            evaluator="Programme Expert",
            proposal_id=proposal.id
        )
        
        proposal.add_evaluation(evaluation)
        
        assert len(proposal.evaluations) == 1
        assert proposal.evaluations[0] == evaluation


class TestIdea:
    """Tests for the Idea data structure."""

    def test_idea_initialization(self):
        """Test that an Idea can be initialized with the required attributes."""
        idea_id = str(uuid.uuid4())
        title = "Remote Patient Monitoring"
        created_at = datetime.now()
        description = "Use AI to monitor patients remotely"
        proposal_id = str(uuid.uuid4())
        
        idea = Idea(
            id=idea_id,
            title=title,
            created_at=created_at,
            description=description,
            proposal_id=proposal_id
        )
        
        assert idea.id == idea_id
        assert idea.title == title
        assert idea.created_at == created_at
        assert idea.description == description
        assert idea.proposal_id == proposal_id
        assert idea.evaluations == []
    
    def test_idea_add_evaluation(self):
        """Test that an Evaluation can be added to an Idea."""
        idea = Idea(
            id=str(uuid.uuid4()),
            title="Remote Patient Monitoring",
            created_at=datetime.now(),
            description="Use AI to monitor patients remotely",
            proposal_id=str(uuid.uuid4())
        )
        
        evaluation = Evaluation(
            id=str(uuid.uuid4()),
            created_at=datetime.now(),
            score=90,
            feedback="Innovative idea with strong market potential",
            evaluator="Startup Founder",
            idea_id=idea.id
        )
        
        idea.add_evaluation(evaluation)
        
        assert len(idea.evaluations) == 1
        assert idea.evaluations[0] == evaluation


class TestEvaluation:
    """Tests for the Evaluation data structure."""

    def test_evaluation_initialization_for_proposal(self):
        """Test that an Evaluation for a Proposal can be initialized with the required attributes."""
        evaluation_id = str(uuid.uuid4())
        created_at = datetime.now()
        score = 85
        feedback = "Strong proposal with good alignment to EU priorities"
        evaluator = "Programme Expert"
        proposal_id = str(uuid.uuid4())
        
        evaluation = Evaluation(
            id=evaluation_id,
            created_at=created_at,
            score=score,
            feedback=feedback,
            evaluator=evaluator,
            proposal_id=proposal_id
        )
        
        assert evaluation.id == evaluation_id
        assert evaluation.created_at == created_at
        assert evaluation.score == score
        assert evaluation.feedback == feedback
        assert evaluation.evaluator == evaluator
        assert evaluation.proposal_id == proposal_id
        assert evaluation.idea_id is None
    
    def test_evaluation_initialization_for_idea(self):
        """Test that an Evaluation for an Idea can be initialized with the required attributes."""
        evaluation_id = str(uuid.uuid4())
        created_at = datetime.now()
        score = 90
        feedback = "Innovative idea with strong market potential"
        evaluator = "Startup Founder"
        idea_id = str(uuid.uuid4())
        
        evaluation = Evaluation(
            id=evaluation_id,
            created_at=created_at,
            score=score,
            feedback=feedback,
            evaluator=evaluator,
            idea_id=idea_id
        )
        
        assert evaluation.id == evaluation_id
        assert evaluation.created_at == created_at
        assert evaluation.score == score
        assert evaluation.feedback == feedback
        assert evaluation.evaluator == evaluator
        assert evaluation.idea_id == idea_id
        assert evaluation.proposal_id is None
    
    def test_evaluation_requires_either_proposal_or_idea(self):
        """Test that an Evaluation requires either a proposal_id or an idea_id."""
        with pytest.raises(ValueError):
            Evaluation(
                id=str(uuid.uuid4()),
                created_at=datetime.now(),
                score=85,
                feedback="Strong proposal with good alignment to EU priorities",
                evaluator="Programme Expert"
            )
    
    def test_evaluation_cannot_have_both_proposal_and_idea(self):
        """Test that an Evaluation cannot have both a proposal_id and an idea_id."""
        with pytest.raises(ValueError):
            Evaluation(
                id=str(uuid.uuid4()),
                created_at=datetime.now(),
                score=85,
                feedback="Strong proposal with good alignment to EU priorities",
                evaluator="Programme Expert",
                proposal_id=str(uuid.uuid4()),
                idea_id=str(uuid.uuid4())
            )