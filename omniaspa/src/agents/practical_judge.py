"""Implementation of the Practical Judge Agent."""

from .base_agent import Agent
from typing import List, Dict, Any
import logging
import copy # To simulate modifying the idea data
import json # For parsing potential LLM JSON output

# Import the placeholder LLM call function and config
from src.llm_integration import call_llm
from src import config

logger = logging.getLogger(__name__)

class PracticalJudgeAgent(Agent):
    """
    Agent specialized in critically evaluating and improving ideas.
    """
    DEFAULT_NAME = "Practical Judge"

    def __init__(self, name: str = DEFAULT_NAME):
        super().__init__(name)
        logger.info(f"Initialized {self.name}")

    def execute_task(self, task_details: Dict[str, Any]) -> Dict[str, Any]:
        """Executes tasks like critiquing or improving ideas."""
        task_type = task_details.get("type")
        result = {"status": "failed", "output": f"Unknown task type: {task_type}"}

        if task_type == "critique_idea":
            idea_data = task_details.get("idea_data", {})
            title = idea_data.get('title', 'N/A')
            description = idea_data.get('description', 'N/A')
            logger.info(f"{self.name} critiquing idea: {title}")

            # Construct prompt for LLM
            prompt = (
                f"Critically evaluate the following project idea for an EU Digital Europe Programme application. "
                f"Focus on its practicality, potential weaknesses, risks, and overall viability. "
                f"Idea Title: {title}\nIdea Description: {description}\n\n"
                f"Provide a numerical score (0-100, lower means more concerns) and concise critical feedback. "
                f"Format the output as a JSON object with 'score' and 'critique' keys."
            )

            # Call LLM (placeholder)
            llm_response_str = call_llm(
                prompt,
                provider=config.LLM_PROVIDER_DEFAULT, # Or specific override
                model=config.LLM_MODEL_DEFAULT,
                max_tokens=config.LLM_TOKENS_JUDGE_CRITIQUE, # Use configurable tokens
                temperature=config.LLM_TEMP_JUDGE_CRITIQUE # Use configurable temperature
            )

            # Parse response or use defaults
            score = 60 # Default dummy score
            critique = f"Critique for '{title}': Strengths are X, weaknesses are Y."
            if llm_response_str:
                try:
                    if llm_response_str.strip().startswith('{'):
                        critique_data = json.loads(llm_response_str)
                        score = critique_data.get("score", score)
                        critique = critique_data.get("critique", critique)
                    else:
                        critique = llm_response_str # Use raw string if not JSON
                except Exception as e:
                    logger.error(f"Failed to parse LLM critique response: {e}. Using defaults.")
                    critique = f"Default critique - Error parsing LLM response: {llm_response_str}"
            else:
                critique = "Default critique - LLM call failed."

            result = {
                "status": "completed",
                "critique": critique,
                "score": score
            }

        elif task_type == "improve_idea":
            idea_data = task_details.get("idea_data", {})
            title = idea_data.get('title', 'N/A')
            description = idea_data.get('description', 'N/A')
            logger.info(f"{self.name} improving idea: {title}")

            # Construct prompt for LLM
            prompt = (
                f"Based on the following project idea, suggest concrete improvements to enhance its practicality, "
                f"address potential weaknesses, and increase its chances of success for an EU Digital Europe Programme grant. "
                f"Original Idea Title: {title}\nOriginal Idea Description: {description}\n\n"
                f"Rewrite the title and description with these improvements incorporated. "
                f"Format the output as a JSON object with 'title' and 'description' keys containing the improved versions."
            )

            # Call LLM (placeholder)
            llm_response_str = call_llm(
                prompt,
                provider=config.LLM_PROVIDER_DEFAULT, # Or specific override
                model=config.LLM_MODEL_DEFAULT,
                max_tokens=config.LLM_TOKENS_JUDGE_IMPROVE, # Use configurable tokens
                temperature=config.LLM_TEMP_JUDGE_IMPROVE # Use configurable temperature
            )

            # Simulate improvement - create a modified copy
            improved_idea = copy.deepcopy(idea_data)
            improved_idea["description"] = description + " [Improved by Judge]" # Default improvement
            improved_idea["title"] = title + " (Revised)" # Default improvement

            if llm_response_str:
                try:
                    if llm_response_str.strip().startswith('{'):
                        improvement_data = json.loads(llm_response_str)
                        improved_idea["title"] = improvement_data.get("title", improved_idea["title"])
                        improved_idea["description"] = improvement_data.get("description", improved_idea["description"])
                    else:
                            # If not JSON, maybe append suggestion to description?
                            improved_idea["description"] += f"\n\nLLM Suggestion: {llm_response_str}"
                except Exception as e:
                    logger.error(f"Failed to parse LLM improvement response: {e}. Using defaults.")
                    improved_idea["description"] += f"\n\n[Error parsing LLM improvement: {llm_response_str}]"
            else:
                    improved_idea["description"] += "\n\n[LLM call failed during improvement.]"


            result = {
                "status": "completed",
                "improved_idea": improved_idea
            }

        else:
            logger.warning(f"{self.name} received unknown task type: {task_type}")

        self.log_interaction(task_details, result)
        return result

    def get_capabilities(self) -> List[str]:
        """Returns the capabilities of this agent."""
        return ["critique_idea", "improve_idea"]