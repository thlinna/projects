"""Core data models for the proposal generation system."""

from .proposal import Proposal
from .idea import Idea
from .evaluation import Evaluation

__all__ = ["Proposal", "Idea", "Evaluation"]