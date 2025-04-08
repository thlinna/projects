"""Defines the Evaluation data structure."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
import uuid

@dataclass
class Evaluation:
    """Represents an evaluation of a Proposal or an Idea."""
    # Fields without defaults must come first
    evaluator: str  # Identifier for the agent or user performing the evaluation
    feedback: str
    # Fields with defaults
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    score: Optional[int] = None  # e.g., a numerical score
    created_at: datetime = field(default_factory=datetime.now)
    proposal_id: Optional[str] = None  # Link to Proposal if evaluating the whole proposal
    idea_id: Optional[str] = None      # Link to Idea if evaluating a specific idea

    def __post_init__(self):
        # Ensure IDs are strings if provided
        if not isinstance(self.id, str):
            self.id = str(self.id)
        if self.proposal_id is not None and not isinstance(self.proposal_id, str):
            self.proposal_id = str(self.proposal_id)
        if self.idea_id is not None and not isinstance(self.idea_id, str):
            self.idea_id = str(self.idea_id)

        # Validate that exactly one of proposal_id or idea_id is set
        if self.proposal_id is None and self.idea_id is None:
            raise ValueError("Evaluation must be linked to either a Proposal or an Idea.")
        if self.proposal_id is not None and self.idea_id is not None:
            raise ValueError("Evaluation cannot be linked to both a Proposal and an Idea.")