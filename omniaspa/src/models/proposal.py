"""Defines the Proposal data structure."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Dict, TYPE_CHECKING # Added Optional, Dict
import uuid

# Use TYPE_CHECKING to avoid circular imports at runtime
if TYPE_CHECKING:
    from .idea import Idea
    from .evaluation import Evaluation

@dataclass
class Proposal:
    """Represents a funding proposal being generated."""
    # Fields without defaults must come first
    title: str
    description: str
    # Fields with defaults
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    status: str = "draft"  # e.g., draft, under_review, finalized, submitted
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    ideas: List['Idea'] = field(default_factory=list)
    evaluations: List['Evaluation'] = field(default_factory=list)
    # New fields for state persistence
    selected_idea_id: Optional[str] = None # ID of the idea chosen for refinement/writing
    generated_sections: Optional[str] = None # JSON string of generated sections {section_name: content}
    compiled_markdown: Optional[str] = None # Stores the final compiled markdown output

    def add_idea(self, idea: 'Idea'):
        """Adds an Idea to this Proposal."""
        if idea not in self.ideas:
            self.ideas.append(idea)
            self.updated_at = datetime.now()

    def add_evaluation(self, evaluation: 'Evaluation'):
        """Adds an Evaluation to this Proposal."""
        if evaluation not in self.evaluations:
            # Ensure the evaluation is actually for this proposal
            if evaluation.proposal_id == self.id:
                self.evaluations.append(evaluation)
                self.updated_at = datetime.now()
            else:
                # Or handle error appropriately
                print(f"Warning: Attempted to add evaluation {evaluation.id} to wrong proposal {self.id}")

    def __post_init__(self):
        # Ensure IDs are strings if provided
        if not isinstance(self.id, str):
            self.id = str(self.id)
        # Ensure JSON fields are None or strings (basic check)
        if self.generated_sections is not None and not isinstance(self.generated_sections, str):
            raise TypeError("generated_sections must be a JSON string or None")
        if self.compiled_markdown is not None and not isinstance(self.compiled_markdown, str):
            raise TypeError("compiled_markdown must be a string or None")
        # Basic status validation could go here if needed