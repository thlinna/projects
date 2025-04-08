"""Defines the Idea data structure."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, TYPE_CHECKING
import uuid

# Use TYPE_CHECKING to avoid circular imports at runtime
if TYPE_CHECKING:
    from .evaluation import Evaluation

@dataclass
class Idea:
    """Represents a specific idea or concept within a proposal."""
    # Fields without defaults must come first
    title: str
    description: str
    proposal_id: str  # Link back to the parent Proposal
    # Fields with defaults
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=datetime.now)
    evaluations: List['Evaluation'] = field(default_factory=list)
    refinement_cycle: int = 0 # Track refinement iterations for this idea

    def add_evaluation(self, evaluation: 'Evaluation'):
        """Adds an Evaluation to this Idea."""
        if evaluation not in self.evaluations:
            # Ensure the evaluation is actually for this idea
            if evaluation.idea_id == self.id:
                self.evaluations.append(evaluation)
            else:
                # Or handle error appropriately
                print(f"Warning: Attempted to add evaluation {evaluation.id} to wrong idea {self.id}")

    def __post_init__(self):
        # Ensure IDs are strings if provided
        if not isinstance(self.id, str):
            self.id = str(self.id)
        if not isinstance(self.proposal_id, str):
            self.proposal_id = str(self.proposal_id)