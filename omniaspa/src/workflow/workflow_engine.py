"""Implementation of the Workflow Engine."""

import logging
import re # For checking "major issue"
import os # Added for path operations
import json # Added for persistence
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timezone # Already present, ensure it stays

# Import necessary components
from src.models.proposal import Proposal
from src.models.idea import Idea
from src.models.evaluation import Evaluation
from src.agents.base_agent import Agent
from src.data_storage.sqlite_repository import (
    ProposalRepository, IdeaRepository, EvaluationRepository
)
from src import config # For settings like MAX_REFINEMENT_LOOPS

logger = logging.getLogger(__name__)

class WorkflowEngine:
    """Orchestrates the proposal generation workflow using various agents."""

    # Define agent keys for clarity
    IDEATOR_AGENT = "ideator"
    JUDGE_AGENT = "judge"
    EXPERT_AGENT = "expert" # Assuming an expert agent key
    FOUNDER_AGENT = "founder" # Assuming a founder agent key
    WRITER_AGENT = "writer"

    # Define status constants
    STATUS_IDEATION = "ideation"
    STATUS_CRITIQUE = "critique"
    STATUS_REFINEMENT = "refinement"
    STATUS_WRITING = "writing"
    STATUS_FINALIZING = "finalizing"
    STATUS_COMPLETED = "completed"
    STATUS_ERROR = "error"
    STATUS_FINAL_REVIEW = "final_review" # Added status

    # Refinement constants
    # REFINEMENT_SCORE_THRESHOLD = 80 # Now read from config
    # REFINEMENT_MAJOR_ISSUE_PHRASE = "major issue" # Now read from config

    def __init__(
        self,
        agents: Dict[str, Agent],
        proposal_repo: ProposalRepository,
        idea_repo: IdeaRepository,
        evaluation_repo: EvaluationRepository
    ):
        """Initializes the WorkflowEngine."""
        if not agents:
            raise ValueError("WorkflowEngine requires at least one agent.")
        self.agents = agents
        self.proposal_repo = proposal_repo
        self.idea_repo = idea_repo
        self.evaluation_repo = evaluation_repo
        # Removed in-memory caches, state is now persisted in Proposal object
        # self.section_cache: Dict[str, Dict[str, str]] = {}
        # self.selected_ideas: Dict[str, str] = {}
        logger.info(f"WorkflowEngine initialized with agents: {list(agents.keys())}")

    def register_agent(self, agent_key: str, agent_instance: Agent):
        """Registers or replaces an agent in the engine."""
        if not isinstance(agent_instance, Agent):
            raise TypeError(f"Object provided for key '{agent_key}' is not an Agent subclass.")
        self.agents[agent_key] = agent_instance
        logger.info(f"Agent '{agent_key}' registered/updated in WorkflowEngine.")

    def start_new_proposal(self, topic: str) -> Proposal:
        """Starts a new proposal generation process."""
        logger.info(f"Starting new proposal process for topic: {topic}")
        new_proposal = Proposal(
            title=f"Proposal for {topic}",
            description=f"Initial proposal related to the topic: {topic}",
            status=self.STATUS_IDEATION
        )
        try:
            self.proposal_repo.save(new_proposal)
            logger.info(f"New proposal {new_proposal.id} created and saved.")
            return new_proposal
        except Exception as e:
            logger.error(f"Failed to save new proposal for topic '{topic}': {e}", exc_info=True)
            raise

    def _get_agent(self, agent_key: str) -> Optional[Agent]:
        """Safely retrieves an agent, logging an error if not found."""
        agent = self.agents.get(agent_key)
        if not agent:
            logger.error(f"Agent '{agent_key}' not found in WorkflowEngine.")
        return agent

    def _update_proposal_status(self, proposal: Proposal, new_status: str):
        """Updates proposal status in memory and DB, with logging."""
        if proposal.status != new_status:
            logger.info(f"Updating proposal {proposal.id} status from '{proposal.status}' to '{new_status}'")
            proposal.status = new_status
            proposal.updated_at = datetime.now(timezone.utc)
            try:
                self.proposal_repo.update(proposal)
            except Exception as e:
                logger.error(f"Failed to update proposal {proposal.id} status to '{new_status}': {e}", exc_info=True)
                # Consider setting status to ERROR here
        else:
            logger.debug(f"Proposal {proposal.id} status already '{new_status}'. No update needed.")

    def _get_latest_evaluation(self, idea_id: str) -> Optional[Evaluation]:
        """Retrieves the most recent evaluation for a given idea."""
        try:
            evaluations = self.evaluation_repo.get_by_idea_id(idea_id)
            if evaluations:
                # Sort by created_at descending and return the first one
                evaluations.sort(key=lambda x: x.created_at, reverse=True)
                return evaluations[0]
            return None
        except Exception as e:
            logger.error(f"Failed to retrieve evaluations for idea {idea_id}: {e}", exc_info=True)
            return None

    def run_step(self, proposal_id: str):
        """Runs the next logical step in the workflow for a given proposal."""
        logger.info(f"Running workflow step for proposal: {proposal_id}")
        proposal = self.proposal_repo.get_by_id(proposal_id)
        if not proposal:
            logger.error(f"Proposal {proposal_id} not found. Cannot run step.")
            return

        current_status = proposal.status
        logger.debug(f"Current proposal status: {current_status}")

        try:
            if current_status == self.STATUS_IDEATION:
                self._execute_ideation_step(proposal)
            elif current_status == self.STATUS_CRITIQUE:
                self._execute_critique_step(proposal)
            elif current_status == self.STATUS_REFINEMENT:
                self._execute_refinement_step(proposal)
            elif current_status == self.STATUS_WRITING:
                self._execute_writing_step(proposal)
            elif current_status == self.STATUS_FINALIZING:
                self._execute_finalizing_step(proposal)
            elif current_status == self.STATUS_FINAL_REVIEW: # Added step
                self._execute_final_review_step(proposal)
            else:
                # Handles statuses like 'completed', 'error', or any unexpected status
                logger.warning(f"No action defined or needed for proposal status: {current_status}")

        except Exception as e:
            logger.error(f"Error during workflow step for proposal {proposal_id} (status: {current_status}): {e}", exc_info=True)
            self._update_proposal_status(proposal, self.STATUS_ERROR)

    def _execute_ideation_step(self, proposal: Proposal):
        """Generates initial ideas for the proposal."""
        logger.info(f"Executing ideation step for proposal {proposal.id}...")
        ideator = self._get_agent(self.IDEATOR_AGENT)
        if not ideator: return

        task_details = {
            "type": "generate_ideas",
            "topic": proposal.title,
            "quantity": 3 # Example quantity
        }
        result = ideator.execute_task(task_details)

        if result.get("status") == "completed":
            generated_ideas_data = result.get("generated_ideas", [])
            if not generated_ideas_data:
                 logger.warning(f"Ideator agent completed but returned no ideas for proposal {proposal.id}.")
                 # Decide how to handle - maybe retry or error? Stay in ideation for now.
                 return

            for idea_data in generated_ideas_data:
                new_idea = Idea(
                    title=idea_data.get("title", "Untitled Idea"),
                    description=idea_data.get("description", ""),
                    proposal_id=proposal.id,
                    refinement_cycle=0 # Initialize cycle count
                )
                self.idea_repo.save(new_idea)
                logger.info(f"Saved new idea {new_idea.id} for proposal {proposal.id}")

            self._update_proposal_status(proposal, self.STATUS_CRITIQUE)
        else:
            logger.error(f"Ideation task failed for proposal {proposal.id}. Result: {result}")
            self._update_proposal_status(proposal, self.STATUS_ERROR)

    def _execute_critique_step(self, proposal: Proposal):
        """Critiques all current ideas for the proposal."""
        logger.info(f"Executing critique step for proposal {proposal.id}...")
        judge = self._get_agent(self.JUDGE_AGENT)
        if not judge: return

        ideas_to_critique = self.idea_repo.get_by_proposal_id(proposal.id)
        if not ideas_to_critique:
            logger.warning(f"No ideas found for proposal {proposal.id} to critique. Moving back to ideation.")
            self._update_proposal_status(proposal, self.STATUS_IDEATION)
            return

        critique_failed = False
        for idea in ideas_to_critique:
            # Avoid re-critiquing if already done in this state (more complex state needed for perfect check)
            logger.debug(f"Critiquing idea {idea.id}: {idea.title}")
            task_details = {
                "type": "critique_idea",
                "idea_data": {"id": idea.id, "title": idea.title, "description": idea.description}
            }
            result = judge.execute_task(task_details)

            if result.get("status") == "completed":
                new_evaluation = Evaluation(
                    evaluator=judge.name,
                    score=result.get("score"),
                    feedback=result.get("critique", "No critique provided."),
                    idea_id=idea.id
                )
                self.evaluation_repo.save(new_evaluation)
                logger.info(f"Saved evaluation {new_evaluation.id} for idea {idea.id}")
            else:
                logger.error(f"Critique task failed for idea {idea.id}. Result: {result}")
                critique_failed = True # Mark that at least one critique failed

        if critique_failed:
            logger.warning(f"One or more critiques failed for proposal {proposal.id}. Setting status to ERROR.")
            self._update_proposal_status(proposal, self.STATUS_ERROR)
        else:
            # --- Select Best Idea After All Critiques are Done ---
            best_idea: Optional[Idea] = None
            highest_score = -1
            ideas_map = {idea.id: idea for idea in ideas_to_critique} # Map IDs to ideas for easy lookup
            latest_evals: Dict[str, Evaluation] = {} # Store latest evals for checking threshold

            # Iterate through the ideas again to find the best one based on the *latest* evaluation
            for idea_id, idea_obj in ideas_map.items():
                latest_eval = self._get_latest_evaluation(idea_id) # Use helper to get latest eval for *this* idea
                if latest_eval:
                    latest_evals[idea_id] = latest_eval # Store for threshold check
                    score = latest_eval.score or -1 # Default to -1 if score is None
                    if score > highest_score:
                        highest_score = score
                        best_idea = idea_obj
                else:
                    # This case should ideally not happen if critique succeeded, but handle defensively
                    logger.warning(f"No evaluation found for idea {idea_id} during selection, even after critique step.")

            if best_idea:
                # Check if the best idea already meets the threshold
                latest_eval_for_best = latest_evals.get(best_idea.id)
                score_for_best = latest_eval_for_best.score if latest_eval_for_best else -1
                feedback_for_best = latest_eval_for_best.feedback if latest_eval_for_best else ""
                # Use config value for phrase check
                has_major_issue_for_best = re.search(config.REFINEMENT_MAJOR_ISSUE_PHRASE, feedback_for_best, re.IGNORECASE) is not None

                if score_for_best >= config.REFINEMENT_SCORE_THRESHOLD and not has_major_issue_for_best:
                    logger.info(f"Best idea {best_idea.id} (Score: {score_for_best}) already meets threshold. Skipping refinement, moving directly to writing.")
                    # No need to store selected_idea_id if skipping refinement
                    self._update_proposal_status(proposal, self.STATUS_WRITING)
                else:
                    proposal.selected_idea_id = best_idea.id # Persist selected idea ID
                    logger.info(f"Selected best idea {best_idea.id} (Score: {score_for_best}) requires refinement. Persisting selection and moving to refinement.")
                    try:
                        self.proposal_repo.update(proposal) # Save the selected ID
                        self._update_proposal_status(proposal, self.STATUS_REFINEMENT)
                    except Exception as e:
                         logger.error(f"Failed to update proposal {proposal.id} with selected idea ID: {e}", exc_info=True)
                         self._update_proposal_status(proposal, self.STATUS_ERROR) # Set error if update fails
            else:
                # This means no ideas had valid evaluations after the critique step
                logger.error(f"Could not select a best idea for proposal {proposal.id} after critique (no valid evaluations found). Setting status to ERROR.")
                self._update_proposal_status(proposal, self.STATUS_ERROR)

    def _execute_refinement_step(self, proposal: Proposal):
        """Iteratively refines ideas based on critiques."""
        logger.info(f"Executing refinement step for proposal {proposal.id}...")
        judge = self._get_agent(self.JUDGE_AGENT)
        expert = self._get_agent(self.EXPERT_AGENT)
        founder = self._get_agent(self.FOUNDER_AGENT)

        if not all([judge, expert, founder]):
            logger.error("One or more required agents (Judge, Expert, Founder) not found for refinement.")
            self._update_proposal_status(proposal, self.STATUS_ERROR)
            return

        # --- Get the selected idea ---
        selected_idea_id = proposal.selected_idea_id # Retrieve from proposal object
        if not selected_idea_id:
            logger.error(f"No selected_idea_id found in proposal {proposal.id}. Cannot refine. Setting status to ERROR.")
            self._update_proposal_status(proposal, self.STATUS_ERROR)
            return

        idea = self.idea_repo.get_by_id(selected_idea_id)
        if not idea:
            logger.error(f"Selected idea {selected_idea_id} not found in database for proposal {proposal.id}. Setting status to ERROR.")
            self._update_proposal_status(proposal, self.STATUS_ERROR)
            return

        idea_ready = False # Track if the selected idea becomes ready
        refinement_action_taken = False # Track if refinement was performed in this step

        # --- Refine the selected idea ---
        logger.debug(f"Considering refinement for selected idea {idea.id} (Cycle: {idea.refinement_cycle})")

        # --- Refine the selected idea ---
        logger.debug(f"Considering refinement for selected idea {idea.id} (Cycle: {idea.refinement_cycle})")

        # Check max refinement loops first
        if idea.refinement_cycle >= config.MAX_REFINEMENT_LOOPS:
            logger.warning(f"Selected idea {idea.id} reached max refinement loops ({config.MAX_REFINEMENT_LOOPS}). Considering it ready.")
            idea_ready = True
        else:
            # Get latest critique if not already at max loops

            # Get latest critique
            latest_eval = self._get_latest_evaluation(idea.id)
            if not latest_eval:
                logger.warning(f"No evaluation found for idea {idea.id}. Cannot determine refinement need. Skipping.")
                # Cannot proceed without evaluation, stay in refinement but log error
                logger.error(f"No evaluation found for idea {idea.id}. Cannot determine refinement need. Staying in refinement.")
                self._update_proposal_status(proposal, self.STATUS_REFINEMENT) # Stay in refinement
                return # Exit step execution

            # Check exit conditions
            score = latest_eval.score or 0
            feedback = latest_eval.feedback or ""
            has_major_issue = re.search(config.REFINEMENT_MAJOR_ISSUE_PHRASE, feedback, re.IGNORECASE) is not None # Use config value

            if score >= config.REFINEMENT_SCORE_THRESHOLD and not has_major_issue:
                logger.info(f"Selected idea {idea.id} meets refinement criteria (Score: {score}, No Major Issues). Ready for writing.")
                idea_ready = True
            else:
                # Conditions not met, proceed with refinement cycle
                logger.info(f"Refining idea {idea.id} (Score: {score}, Major Issue: {has_major_issue}, Cycle: {idea.refinement_cycle + 1})")
                # Idea needs refinement
                refinement_action_taken = True
                idea.refinement_cycle += 1

                # --- Sequential Refinement by Judge, Expert, Founder ---
                current_idea_data = {"id": idea.id, "title": idea.title, "description": idea.description}
                last_feedback = feedback # Start with the critique feedback

                # 1. Judge Improves
                logger.debug(f"Asking Judge to improve idea {idea.id}")
                judge_task = {"type": "improve_idea", "idea_data": current_idea_data, "critique": last_feedback}
                judge_result = judge.execute_task(judge_task)
                if judge_result.get("status") == "completed" and "improved_idea" in judge_result:
                    current_idea_data = judge_result["improved_idea"] # Update data for next agent
                    # Optionally save Judge's evaluation/improvement rationale
                    logger.info(f"Idea {idea.id} improved by Judge.")
                else:
                    logger.warning(f"Judge failed to improve idea {idea.id}. Using previous version.")

                # 2. Expert Improves (based on Judge's output)
                logger.debug(f"Asking Expert to improve idea {idea.id}")
                expert_task = {"type": "improve_idea", "idea_data": current_idea_data, "critique": last_feedback} # Provide original critique? Or judge's rationale? Needs thought.
                expert_result = expert.execute_task(expert_task)
                if expert_result.get("status") == "completed" and "improved_idea" in expert_result:
                    current_idea_data = expert_result["improved_idea"]
                    logger.info(f"Idea {idea.id} further improved by Expert.")
                else:
                    logger.warning(f"Expert failed to improve idea {idea.id}. Using previous version.")

                # 3. Founder Improves (based on Expert's output)
                logger.debug(f"Asking Founder to improve idea {idea.id}")
                founder_task = {"type": "improve_idea", "idea_data": current_idea_data, "critique": last_feedback}
                founder_result = founder.execute_task(founder_task)
                if founder_result.get("status") == "completed" and "improved_idea" in founder_result:
                    current_idea_data = founder_result["improved_idea"]
                    logger.info(f"Idea {idea.id} further improved by Founder.")
                else:
                    logger.warning(f"Founder failed to improve idea {idea.id}. Using previous version.")

                # Update the idea in the database with the final refined version
                idea.title = current_idea_data.get("title", idea.title)
                idea.description = current_idea_data.get("description", idea.description)
                idea.updated_at = datetime.now(timezone.utc)
                self.idea_repo.update(idea)
                logger.info(f"Saved refined idea {idea.id} after cycle {idea.refinement_cycle}.")

                # After refinement, trigger a new critique for the next cycle
                logger.debug(f"Triggering new critique for refined idea {idea.id}")
                critique_task = {
                    "type": "critique_idea",
                    "idea_data": {"id": idea.id, "title": idea.title, "description": idea.description}
                }
                critique_result = judge.execute_task(critique_task)
                if critique_result.get("status") == "completed":
                    new_evaluation = Evaluation(
                        evaluator=judge.name,
                        score=critique_result.get("score"),
                        feedback=critique_result.get("critique", "No critique provided."),
                        idea_id=idea.id
                    )
                    self.evaluation_repo.save(new_evaluation)
                    logger.info(f"Saved new evaluation {new_evaluation.id} for refined idea {idea.id}")
                else:
                    logger.error(f"Critique task failed for refined idea {idea.id}. Result: {critique_result}")
                    # Consider setting proposal status to error if post-refinement critique fails

            # Conditions not met, proceed with refinement cycle
            logger.info(f"Refining idea {idea.id} (Score: {score}, Major Issue: {has_major_issue}, Cycle: {idea.refinement_cycle + 1})")
            # Idea needs refinement
            refinement_action_taken = True
            idea.refinement_cycle += 1

            # --- Sequential Refinement by Judge, Expert, Founder ---
            current_idea_data = {"id": idea.id, "title": idea.title, "description": idea.description}
            last_feedback = feedback # Start with the critique feedback

            # 1. Judge Improves
            logger.debug(f"Asking Judge to improve idea {idea.id}")
            judge_task = {"type": "improve_idea", "idea_data": current_idea_data, "critique": last_feedback}
            judge_result = judge.execute_task(judge_task)
            if judge_result.get("status") == "completed" and "improved_idea" in judge_result:
                current_idea_data = judge_result["improved_idea"] # Update data for next agent
                # Optionally save Judge's evaluation/improvement rationale
                logger.info(f"Idea {idea.id} improved by Judge.")
            else:
                logger.warning(f"Judge failed to improve idea {idea.id}. Using previous version.")

            # 2. Expert Improves (based on Judge's output)
            logger.debug(f"Asking Expert to improve idea {idea.id}")
            expert_task = {"type": "improve_idea", "idea_data": current_idea_data, "critique": last_feedback} # Provide original critique? Or judge's rationale? Needs thought.
            expert_result = expert.execute_task(expert_task)
            if expert_result.get("status") == "completed" and "improved_idea" in expert_result:
                current_idea_data = expert_result["improved_idea"]
                logger.info(f"Idea {idea.id} further improved by Expert.")
            else:
                logger.warning(f"Expert failed to improve idea {idea.id}. Using previous version.")

            # 3. Founder Improves (based on Expert's output)
            logger.debug(f"Asking Founder to improve idea {idea.id}")
            founder_task = {"type": "improve_idea", "idea_data": current_idea_data, "critique": last_feedback}
            founder_result = founder.execute_task(founder_task)
            if founder_result.get("status") == "completed" and "improved_idea" in founder_result:
                current_idea_data = founder_result["improved_idea"]
                logger.info(f"Idea {idea.id} further improved by Founder.")
            else:
                logger.warning(f"Founder failed to improve idea {idea.id}. Using previous version.")

            # Update the idea in the database with the final refined version
            idea.title = current_idea_data.get("title", idea.title)
            idea.description = current_idea_data.get("description", idea.description)
            idea.updated_at = datetime.now(timezone.utc)
            self.idea_repo.update(idea)
            logger.info(f"Saved refined idea {idea.id} after cycle {idea.refinement_cycle}.")

            # After refinement, trigger a new critique for the next cycle
            logger.debug(f"Triggering new critique for refined idea {idea.id}")
            critique_task = {
                "type": "critique_idea",
                "idea_data": {"id": idea.id, "title": idea.title, "description": idea.description}
            }
            critique_result = judge.execute_task(critique_task)
            if critique_result.get("status") == "completed":
                new_evaluation = Evaluation(
                    evaluator=judge.name,
                    score=critique_result.get("score"),
                    feedback=critique_result.get("critique", "No critique provided."),
                    idea_id=idea.id
                )
                self.evaluation_repo.save(new_evaluation)
                logger.info(f"Saved new evaluation {new_evaluation.id} for refined idea {idea.id}")
            else:
                logger.error(f"Critique task failed for refined idea {idea.id}. Result: {critique_result}")
                # Consider setting proposal status to error if post-refinement critique fails

        # --- Decide next state based on the single selected idea ---
        if idea_ready:
            logger.info(f"Selected idea {idea.id} for proposal {proposal.id} is ready. Moving to writing.")
            # Clear the selected idea ID from the proposal as it's now ready for writing
            proposal.selected_idea_id = None
            try:
                self.proposal_repo.update(proposal) # Save the cleared ID
                self._update_proposal_status(proposal, self.STATUS_WRITING)
            except Exception as e:
                logger.error(f"Failed to clear selected idea ID for proposal {proposal.id}: {e}", exc_info=True)
                self._update_proposal_status(proposal, self.STATUS_ERROR)
        elif refinement_action_taken:
            logger.info(f"Selected idea {idea.id} for proposal {proposal.id} was refined. Staying in refinement state for next cycle.")
            # Status remains 'refinement', next run_step will re-evaluate this same idea
            self._update_proposal_status(proposal, self.STATUS_REFINEMENT) # Explicitly set to ensure DB is updated if needed
        else:
            # Should not happen if logic is correct (either ready, refined, or error occurred)
            logger.error(f"Unexpected state in refinement for proposal {proposal.id}, idea {idea.id}. Setting status to ERROR.")
            self._update_proposal_status(proposal, self.STATUS_ERROR)

    def _get_selected_idea_for_writing(self, proposal_id: str) -> Optional[Idea]:
        """Retrieves the single idea selected for refinement and checks its final status."""
        # Retrieve the proposal again to ensure we have the latest selected_idea_id
        proposal = self.proposal_repo.get_by_id(proposal_id)
        if not proposal:
            logger.error(f"Proposal {proposal_id} not found when trying to get selected idea for writing.")
            return None
        selected_idea_id = proposal.selected_idea_id # Read from proposal object
        if not selected_idea_id:
            # This might happen if the workflow moves to writing prematurely or cache is lost
            logger.error(f"No selected idea ID found in cache for proposal {proposal_id} during writing phase.")
            # Fallback: Try selecting the highest scoring idea directly from DB
            ideas = self.idea_repo.get_by_proposal_id(proposal_id)
            best_idea_fallback: Optional[Idea] = None
            highest_score = -1
            for idea_fallback in ideas:
                 latest_eval = self._get_latest_evaluation(idea_fallback.id)
                 if latest_eval:
                     score = latest_eval.score or -1
                     if score > highest_score:
                         highest_score = score
                         best_idea_fallback = idea_fallback
            if best_idea_fallback:
                 logger.warning(f"Falling back to highest scoring idea {best_idea_fallback.id} (Score: {highest_score}) for writing.")
                 return best_idea_fallback
            else:
                 logger.error(f"No ideas found at all for proposal {proposal_id} during fallback.")
                 return None

        idea = self.idea_repo.get_by_id(selected_idea_id)
        if not idea:
            logger.error(f"Selected idea {selected_idea_id} not found in database for proposal {proposal_id}.")
            return None

        # Log final status before writing
        latest_eval = self._get_latest_evaluation(idea.id)
        score = latest_eval.score if latest_eval else -1
        logger.info(f"Proceeding to write with selected idea {idea.id} (Final Score: {score}, Cycle: {idea.refinement_cycle}).")
        return idea

    def _execute_writing_step(self, proposal: Proposal):
        """Writes proposal sections based on the selected best idea."""
        logger.info(f"Executing writing step for proposal {proposal.id}...")
        writer = self._get_agent(self.WRITER_AGENT)
        if not writer: return

        selected_idea = self._get_selected_idea_for_writing(proposal.id) # Use updated function name
        if not selected_idea:
            logger.error(f"No suitable idea selected for writing for proposal {proposal.id}. Setting status to ERROR.")
            self._update_proposal_status(proposal, self.STATUS_ERROR)
            return

        # Example: Write Introduction and Methodology based on the selected idea
        sections_to_write = ["Introduction", "Methodology"] # Define sections needed
        writing_failed = False
        generated_content = {}

        for section_name in sections_to_write:
            logger.debug(f"Writing section '{section_name}' based on idea {selected_idea.id}")
            task_details = {
                "type": "write_section",
                "section_name": section_name,
                "input_data": { # Pass more context
                    "proposal_title": proposal.title,
                    "idea_title": selected_idea.title,
                    "idea_description": selected_idea.description,
                    # Optionally add latest critique/evaluations here too
                }
            }
            result = writer.execute_task(task_details)
            logger.debug(f"Writer agent result for section '{section_name}', proposal {proposal.id}: {result}") # DEBUG ADDED

            if result.get("status") == "completed":
                section_content = result.get("section_content") # Check for None explicitly
                if section_content is not None:
                    generated_content[section_name] = section_content
                    logger.info(f"Writer generated section '{section_name}' for proposal {proposal.id}")
                else:
                    # Log if content is missing even if status is completed
                    logger.error(f"Writing task completed for section '{section_name}', proposal {proposal.id}, but 'section_content' key is missing or None in result: {result}")
                    # Decide how to handle missing content. Let's fail the step.
                    writing_failed = True
                    break # Stop writing if content is missing
            else:
                logger.error(f"Writing task failed for section '{section_name}', proposal {proposal.id}. Result: {result}")
                writing_failed = True
                break # Stop writing if one section fails

        if writing_failed:
            logger.error(f"Writing step failed for proposal {proposal.id}. Not persisting sections or proceeding to finalizing.") # DEBUG ADDED
            self._update_proposal_status(proposal, self.STATUS_ERROR)
        else:
            # Persist generated sections as JSON
            try:
                proposal.generated_sections = json.dumps(generated_content)
                logger.debug(f"Persisting generated sections for proposal {proposal.id}: {list(generated_content.keys())}")
                self.proposal_repo.update(proposal) # Save sections to DB
                logger.info(f"Successfully persisted {len(generated_content)} sections for proposal {proposal.id}")
                self._update_proposal_status(proposal, self.STATUS_FINALIZING)
            except (json.JSONDecodeError, TypeError) as e:
                 logger.error(f"Failed to serialize generated sections for proposal {proposal.id}: {e}", exc_info=True)
                 self._update_proposal_status(proposal, self.STATUS_ERROR)
            except Exception as e:
                 logger.error(f"Failed to update proposal {proposal.id} with generated sections: {e}", exc_info=True)
                 self._update_proposal_status(proposal, self.STATUS_ERROR)

    def _execute_finalizing_step(self, proposal: Proposal):
        """Compiles the final proposal document."""
        logger.info(f"Executing finalizing step for proposal {proposal.id}...")
        writer = self._get_agent(self.WRITER_AGENT)
        if not writer: return

        sections_json = proposal.generated_sections
        sections_to_compile = {}
        if sections_json:
            try:
                sections_to_compile = json.loads(sections_json)
                logger.debug(f"Loaded {len(sections_to_compile)} sections from proposal {proposal.id} for compilation.")
            except json.JSONDecodeError as e:
                logger.error(f"Failed to decode generated_sections JSON for proposal {proposal.id}: {e}", exc_info=True)
                self._update_proposal_status(proposal, self.STATUS_ERROR)
                return
        else:
            logger.warning(f"Proposal {proposal.id} has no persisted generated_sections. Cannot compile.")
            # This might be an error state or indicate writing step failed/was skipped unexpectedly
            self._update_proposal_status(proposal, self.STATUS_ERROR) # Treat as error for now
            return

        if not sections_to_compile: # Double check after loading
            logger.warning(f"No generated sections found in cache for proposal {proposal.id}. Cannot compile.")
            # Decide how to handle - maybe error, maybe try writing again?
            self._update_proposal_status(proposal, self.STATUS_ERROR) # Error for now
            return

        task_details = {
            "type": "compile_final_proposal",
            "sections": sections_to_compile
        }
        result = writer.execute_task(task_details)

        if result.get("status") == "completed":
            final_md = result.get("final_proposal_md", "")
            logger.info(f"Writer compiled final proposal MD for proposal {proposal.id}")
            # Persist compiled markdown
            proposal.compiled_markdown = final_md
            try:
                self.proposal_repo.update(proposal)
                logger.info(f"Persisted final compiled proposal MD for proposal {proposal.id}")
                # Transition to final review status
                self._update_proposal_status(proposal, self.STATUS_FINAL_REVIEW)
            except Exception as e:
                logger.error(f"Failed to update proposal {proposal.id} with compiled markdown: {e}", exc_info=True)
                self._update_proposal_status(proposal, self.STATUS_ERROR)
        else:
            logger.error(f"Finalizing task failed for proposal {proposal.id}. Result: {result}")
            self._update_proposal_status(proposal, self.STATUS_ERROR)

    def _execute_final_review_step(self, proposal: Proposal):
        """Sends the compiled proposal for final review and approval."""
        logger.info(f"Executing final review step for proposal {proposal.id}...")
        reviewer = self._get_agent(self.EXPERT_AGENT) # Using Expert for final review
        if not reviewer:
            logger.error(f"Reviewer agent ({self.EXPERT_AGENT}) not found. Cannot perform final review.")
            self._update_proposal_status(proposal, self.STATUS_ERROR)
            return

        # Retrieve the compiled markdown directly from the proposal object
        final_md = proposal.compiled_markdown

        if not final_md:
            logger.error(f"Compiled proposal markdown not found in cache for proposal {proposal.id}. Cannot review.")
            self._update_proposal_status(proposal, self.STATUS_ERROR)
            return

        # Define the review task
        task_details = {
            "type": "review_final_proposal", # New task type needed for agent
            "proposal_title": proposal.title,
            "proposal_markdown": final_md
        }

        # Execute review task
        result = reviewer.execute_task(task_details)

        if result.get("status") == "completed" and result.get("approved", False): # Agent needs to return 'approved': True/False
            logger.info(f"Final review approved for proposal {proposal.id} by {reviewer.name}.")
            # --- Save Final Proposal to File ---
            try:
                # Ensure output directory exists
                output_dir = config.PROPOSAL_OUTPUT_DIR
                os.makedirs(output_dir, exist_ok=True)

                # Create filename with proposal ID and date
                timestamp = datetime.now().strftime("%Y-%m-%d")
                # Sanitize proposal title slightly for filename (optional)
                safe_title = re.sub(r'[^\w\-]+', '_', proposal.title).strip('_').lower()
                filename = f"{safe_title}_{proposal.id}_{timestamp}.md"
                filepath = os.path.join(output_dir, filename)

                # Write the markdown content
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(f"# {proposal.title}\n\n") # Add title as H1
                    f.write(final_md)
                logger.info(f"Final proposal saved to: {filepath}")

            except Exception as e:
                logger.error(f"Failed to save final proposal file for {proposal.id}: {e}", exc_info=True)
                # Don't fail the whole process, just log the error

            # --- Update Status and Clear Cache ---
            # Store final MD in proposal description (optional, maybe remove later)
            proposal.description += f"\n\n--- FINAL OUTPUT (also saved to file) ---\n{final_md}"
            self._update_proposal_status(proposal, self.STATUS_COMPLETED)
            # Cache is no longer used, state is persisted
            logger.debug(f"Proposal {proposal.id} completed.")
        elif result.get("status") == "completed" and not result.get("approved", False):
            feedback = result.get("feedback", "No feedback provided.")
            logger.warning(f"Final review rejected for proposal {proposal.id} by {reviewer.name}. Feedback: {feedback}")
            # Decide how to handle rejection - e.g., back to writing or error? Setting to error for now.
            proposal.description += f"\n\n--- FINAL REVIEW REJECTED ---\nFeedback: {feedback}"
            self._update_proposal_status(proposal, self.STATUS_ERROR)
            # Cache is no longer used
        else:
            logger.error(f"Final review task failed for proposal {proposal.id}. Result: {result}")
            self._update_proposal_status(proposal, self.STATUS_ERROR)
            # Cache is no longer used

    # Add helper methods for determining next step, checking convergence etc. later
    # def _determine_next_step(self, proposal: Proposal) -> str: ...
    # def _check_convergence(self, proposal: Proposal) -> bool: ...
