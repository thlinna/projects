"""Implementation of the Programme Expert Agent."""

from .base_agent import Agent
from typing import List, Dict, Any
import logging
import json # For parsing potential LLM JSON output
import copy # To simulate modifying the idea data

# Import the placeholder LLM call function and config
from src.llm_integration import call_llm
from src import config

logger = logging.getLogger(__name__)

class ProgrammeExpertAgent(Agent):
    """
    Agent specialized in understanding EU Digital Europe Programme criteria
    and providing guidance.
    """
    DEFAULT_NAME = "Programme Expert"

    def __init__(self, name: str = DEFAULT_NAME):
        super().__init__(name)
        logger.info(f"Initialized {self.name}")

    def execute_task(self, task_details: Dict[str, Any]) -> Dict[str, Any]:
        """Executes tasks like evaluating criteria, providing guidance, or improving ideas."""
        task_type = task_details.get("type")
        result = {"status": "failed", "output": f"Unknown task type: {task_type}"} # Default failure

        if task_type == "evaluate_criteria":
            proposal_data = task_details.get("proposal_data", {})
            title = proposal_data.get('title', 'N/A')
            description = proposal_data.get('description', 'N/A')
            logger.info(f"{self.name} evaluating criteria for proposal: {title}")

            # Construct prompt for LLM
            prompt = (
                f"Evaluate the following proposal idea based on the typical criteria for the "
                f"EU Digital Europe Programme (e.g., innovation, impact, feasibility, relevance to call). "
                f"Proposal Title: {title}\nProposal Description: {description}\n\n"
                f"Provide a numerical score (0-100) and concise feedback."
                f"Format the output as a JSON object with 'evaluation_score' and 'feedback' keys."
            )

            # Call LLM
            llm_response_str = call_llm(
                prompt,
                provider=config.LLM_PROVIDER_DEFAULT, # Or specific override
                model=config.LLM_MODEL_DEFAULT,
                max_tokens=300, # Consider making configurable
                temperature=0.5 # Consider making configurable
            )

            # Parse response or use defaults
            score = 75 # Default dummy score
            feedback = f"Initial evaluation based on criteria for '{title}'."
            if llm_response_str:
                try:
                    # Attempt to parse JSON, find first '{' and last '}'
                    json_start = llm_response_str.find('{')
                    json_end = llm_response_str.rfind('}')
                    if json_start != -1 and json_end != -1 and json_end > json_start:
                        json_str = llm_response_str[json_start:json_end+1]
                        eval_data = json.loads(json_str)
                        score = eval_data.get("evaluation_score", score)
                        feedback = eval_data.get("feedback", feedback)
                    else:
                        feedback = llm_response_str # Use raw string if not JSON
                except Exception as e:
                    logger.error(f"Failed to parse LLM evaluation response: {e}. Using defaults.")
                    feedback = f"Default feedback - Error parsing LLM response: {llm_response_str}"
            else:
                    feedback = "Default feedback - LLM call failed."

            result = {
                "status": "completed",
                "evaluation_score": score,
                "feedback": feedback
            }

        elif task_type == "provide_guidance":
            topic = task_details.get("topic", "general")
            logger.info(f"{self.name} providing guidance on topic: {topic}")

            # Construct prompt for LLM
            prompt = (
                f"Provide expert guidance on '{topic}' specifically in the context of applying for "
                f"the EU Digital Europe Programme. Focus on key considerations and best practices."
            )

            # Call LLM
            llm_response_str = call_llm(
                prompt,
                provider=config.LLM_PROVIDER_DEFAULT, # Or specific override
                model=config.LLM_MODEL_DEFAULT,
                max_tokens=500, # Consider making configurable
                temperature=0.6 # Consider making configurable
            )

            # Use response or default
            guidance = llm_response_str if llm_response_str else f"Default guidance provided by {self.name} regarding {topic} (LLM failed)."

            result = {
                "status": "completed",
                "guidance_text": guidance
            }

        elif task_type == "improve_idea":
            # Focus on alignment with programme goals, impact, EU relevance
            idea_data = task_details.get("idea_data", {})
            title = idea_data.get('title', 'N/A')
            description = idea_data.get('description', 'N/A')
            critique = task_details.get("critique", "") # Get previous critique for context
            logger.info(f"{self.name} improving idea: {title} based on programme expertise.")

            prompt = (
                f"As an expert on the EU Digital Europe Programme, review the following project idea and suggest improvements "
                f"to better align it with the programme's objectives (e.g., innovation, impact, feasibility, cross-border dimension, sustainability, ethical considerations). "
                f"Consider the previous critique:\nCritique: {critique}\n\n"
                f"Original Idea Title: {title}\nOriginal Idea Description: {description}\n\n"
                f"Rewrite the title and description incorporating improvements focused on EU programme alignment and impact. "
                f"Format the output as a JSON object with 'title' and 'description' keys containing the improved versions."
            )

            llm_response_str = call_llm(
                prompt,
                provider=config.LLM_PROVIDER_DEFAULT, # Or specific override
                model=config.LLM_MODEL_DEFAULT,
                max_tokens=config.LLM_TOKENS_EXPERT_IMPROVE, # Use specific config
                temperature=config.LLM_TEMP_EXPERT_IMPROVE  # Use specific config
            )

            improved_idea = copy.deepcopy(idea_data) # Start with original data
            if llm_response_str:
                try:
                    # Attempt to parse JSON, find first '{' and last '}'
                    json_start = llm_response_str.find('{')
                    json_end = llm_response_str.rfind('}')
                    if json_start != -1 and json_end != -1 and json_end > json_start:
                        json_str = llm_response_str[json_start:json_end+1]
                        improvement_data = json.loads(json_str)
                        improved_idea["title"] = improvement_data.get("title", improved_idea["title"])
                        improved_idea["description"] = improvement_data.get("description", improved_idea["description"])
                        logger.info(f"Expert successfully generated improvements for idea {idea_data.get('id')}")
                    else:
                        logger.warning(f"Expert LLM response did not contain valid JSON object structure: {llm_response_str}")
                        improved_idea["description"] += f"\n\n[Expert Suggestion (non-JSON): {llm_response_str}]" # Append raw suggestion if not JSON
                except Exception as e:
                    logger.error(f"Failed to parse Expert LLM improvement response: {e}. Using previous version.")
                    improved_idea["description"] += f"\n\n[Error parsing Expert LLM improvement: {llm_response_str}]"
            else:
                logger.error(f"Expert LLM call failed for improving idea {idea_data.get('id')}")
                improved_idea["description"] += "\n\n[Expert LLM call failed during improvement.]"

            result = {
                "status": "completed",
                "improved_idea": improved_idea
            }

        elif task_type == "review_final_proposal":
            proposal_title = task_details.get("proposal_title", "N/A")
            proposal_markdown = task_details.get("proposal_markdown", "")
            logger.info(f"{self.name} reviewing final proposal: {proposal_title}")

            if not proposal_markdown:
                logger.error("No proposal markdown provided for final review.")
                result = {"status": "failed", "output": "Missing proposal markdown"}
            else:
                prompt = (
                    f"As an expert on the EU Digital Europe Programme, review the following compiled proposal document. "
                    f"Check for overall coherence, alignment with programme objectives, clarity, and completeness. "
                    f"Do not suggest major rewrites, only minor fixes or final approval.\n\n"
                    f"Proposal Title: {proposal_title}\n\n"
                    f"--- PROPOSAL MARKDOWN START ---\n{proposal_markdown}\n--- PROPOSAL MARKDOWN END ---\n\n"
                    f"Respond with a JSON object containing 'approved' (boolean: true if acceptable, false if minor fixes needed) "
                    f"and 'feedback' (string: concise feedback, especially if not approved)."
                )

                llm_response_str = call_llm(
                    prompt,
                    provider=config.LLM_PROVIDER_DEFAULT,
                    model=config.LLM_MODEL_DEFAULT,
                    max_tokens=config.LLM_TOKENS_EXPERT_REVIEW, # Use specific config
                    temperature=config.LLM_TEMP_EXPERT_REVIEW   # Use specific config
                )

                approved = False # Default to not approved
                feedback = "No feedback provided."
                if llm_response_str:
                    try:
                        # Attempt to parse JSON
                        json_start = llm_response_str.find('{')
                        json_end = llm_response_str.rfind('}')
                        if json_start != -1 and json_end != -1 and json_end > json_start:
                            json_str = llm_response_str[json_start:json_end+1]
                            review_data = json.loads(json_str)
                            approved = review_data.get("approved", False)
                            feedback = review_data.get("feedback", feedback)
                            logger.info(f"Expert review completed. Approved: {approved}")
                        else:
                            feedback = f"Review feedback (non-JSON): {llm_response_str}"
                            logger.warning(f"Expert LLM review response did not contain valid JSON: {llm_response_str}")
                    except Exception as e:
                        logger.error(f"Failed to parse Expert LLM review response: {e}. Assuming not approved.")
                        feedback = f"Error parsing review response: {llm_response_str}"
                else:
                    logger.error(f"Expert LLM call failed for final review of {proposal_title}")
                    feedback = "LLM call failed during final review."

                result = {
                    "status": "completed",
                    "approved": approved,
                    "feedback": feedback
                }
        else:
            logger.warning(f"{self.name} received unknown task type: {task_type}")
            # Keep default failure result from line 28

        self.log_interaction(task_details, result)
        return result

    def get_capabilities(self) -> List[str]:
        """Returns the capabilities of this agent."""
        return ["evaluate_criteria", "provide_guidance", "improve_idea", "review_final_proposal"] # Added review task