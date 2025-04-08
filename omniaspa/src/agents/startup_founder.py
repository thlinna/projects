"""Implementation of the Startup Founder Agent."""

from .base_agent import Agent
from typing import List, Dict, Any
import logging
import json # For parsing potential LLM JSON output
import copy # To simulate modifying the idea data

# Import the placeholder LLM call function and config
from src.llm_integration import call_llm
from src import config

logger = logging.getLogger(__name__)

class StartupFounderAgent(Agent):
    """
    Agent experienced with EU stakeholders, best practices, and strong networks.
    Ensures proposals have practical implementation paths.
    """
    DEFAULT_NAME = "Startup Founder"

    def __init__(self, name: str = DEFAULT_NAME):
        super().__init__(name)
        logger.info(f"Initialized {self.name}")

    def execute_task(self, task_details: Dict[str, Any]) -> Dict[str, Any]:
        """Executes tasks like assessing stakeholders, validating practices, or improving ideas."""
        task_type = task_details.get("type")
        result = {"status": "failed", "output": f"Unknown task type: {task_type}"} # Default failure

        if task_type == "assess_stakeholders":
            proposal_data = task_details.get("proposal_data", {})
            area = proposal_data.get("area", "general")
            title = proposal_data.get("title", "N/A")
            logger.info(f"{self.name} assessing stakeholders for area: {area} (Proposal: {title})")

            # Construct prompt for LLM
            prompt = (
                f"For a potential EU Digital Europe Programme project titled '{title}' in the area of '{area}', "
                f"identify key stakeholders (e.g., potential partners, user groups, relevant EU bodies, competitors). "
                f"Provide a brief analysis of their potential roles, interests, and any associated risks. "
                f"Format the output as a JSON object with keys like 'key_partners', 'target_groups', 'relevant_eu_bodies', 'potential_risks'."
            )

            # Call LLM
            llm_response_str = call_llm(
                prompt,
                provider=config.LLM_PROVIDER_DEFAULT, # Or specific override
                model=config.LLM_MODEL_DEFAULT,
                max_tokens=400, # Consider making configurable
                temperature=0.6 # Consider making configurable
            )

            # Parse response or use defaults
            analysis = {
                "key_partners": ["Default Partner A", "Default Partner B"],
                "target_groups": ["Default Group X"],
                "relevant_eu_bodies": ["Default EU Body"],
                "potential_risks": ["Default Risk 1"]
            }
            if llm_response_str:
                try:
                    # Attempt to parse JSON, find first '{' and last '}'
                    json_start = llm_response_str.find('{')
                    json_end = llm_response_str.rfind('}')
                    if json_start != -1 and json_end != -1 and json_end > json_start:
                        json_str = llm_response_str[json_start:json_end+1]
                        analysis = json.loads(json_str)
                    else:
                        analysis["notes"] = llm_response_str # Add raw response if not JSON
                except Exception as e:
                    logger.error(f"Failed to parse LLM stakeholder analysis response: {e}. Using defaults.")
                    analysis["error"] = f"Error parsing LLM response: {llm_response_str}"
            else:
                analysis["error"] = "LLM call failed."

            result = {
                "status": "completed",
                "stakeholder_analysis": analysis
            }

        elif task_type == "validate_best_practices":
            section = task_details.get("proposal_section", "unknown section")
            section_content = task_details.get("section_content", "") # Need content to validate
            logger.info(f"{self.name} validating best practices for section: {section}")

            # Construct prompt for LLM
            prompt = (
                f"Review the following proposal section titled '{section}' for adherence to common best practices "
                f"in EU grant applications (e.g., clarity, SMART objectives, realistic planning, appropriate language). "
                f"Provide concise validation feedback.\n\nSection Content:\n{section_content}"
            )

            # Call LLM
            llm_response_str = call_llm(
                prompt,
                provider=config.LLM_PROVIDER_DEFAULT,
                model=config.LLM_MODEL_DEFAULT,
                max_tokens=300, # Consider making configurable
                temperature=0.5 # Consider making configurable
            )

            feedback = llm_response_str if llm_response_str else f"Default validation for {section}: Looks reasonable (LLM failed)."

            result = {
                "status": "completed",
                "validation_feedback": feedback
            }

        elif task_type == "assess_implementation_path":
            proposal_data = task_details.get("proposal_data", {})
            title = proposal_data.get('title', 'N/A')
            description = proposal_data.get('description', '')
            logger.info(f"{self.name} assessing implementation path for: {title}")

            # Construct prompt for LLM
            prompt = (
                f"Based on the proposal title '{title}' and description below, assess the likely feasibility "
                f"of the implementation path from a practical startup/business perspective. Consider resources, "
                f"timeline, potential roadblocks, and market adoption.\n\nDescription:\n{description}"
            )

            # Call LLM
            llm_response_str = call_llm(
                prompt,
                provider=config.LLM_PROVIDER_DEFAULT,
                model=config.LLM_MODEL_DEFAULT,
                max_tokens=400, # Consider making configurable
                temperature=0.6 # Consider making configurable
            )

            assessment = llm_response_str if llm_response_str else "Default assessment: Implementation path seems feasible (LLM failed)."

            result = {
                "status": "completed",
                "implementation_assessment": assessment
            }

        elif task_type == "improve_idea":
            # Focus on market viability, business model, implementation feasibility
            idea_data = task_details.get("idea_data", {})
            title = idea_data.get('title', 'N/A')
            description = idea_data.get('description', 'N/A')
            critique = task_details.get("critique", "") # Get previous critique for context
            logger.info(f"{self.name} improving idea: {title} from a startup/business perspective.")

            prompt = (
                f"As an experienced startup founder, review the following project idea and suggest improvements "
                f"to enhance its market viability, business model potential, and practical implementation feasibility. "
                f"Consider the previous critique:\nCritique: {critique}\n\n"
                f"Original Idea Title: {title}\nOriginal Idea Description: {description}\n\n"
                f"Rewrite the title and description incorporating improvements focused on business potential and realistic execution. "
                f"Format the output as a JSON object with 'title' and 'description' keys containing the improved versions."
            )

            llm_response_str = call_llm(
                prompt,
                provider=config.LLM_PROVIDER_DEFAULT, # Or specific override
                model=config.LLM_MODEL_DEFAULT,
                max_tokens=config.LLM_TOKENS_FOUNDER_IMPROVE, # Use specific config
                temperature=config.LLM_TEMP_FOUNDER_IMPROVE  # Use specific config
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
                        logger.info(f"Founder successfully generated improvements for idea {idea_data.get('id')}")
                    else:
                        logger.warning(f"Founder LLM response did not contain valid JSON object structure: {llm_response_str}")
                        improved_idea["description"] += f"\n\n[Founder Suggestion (non-JSON): {llm_response_str}]" # Append raw suggestion if not JSON
                except Exception as e:
                    logger.error(f"Failed to parse Founder LLM improvement response: {e}. Using previous version.")
                    improved_idea["description"] += f"\n\n[Error parsing Founder LLM improvement: {llm_response_str}]"
            else:
                logger.error(f"Founder LLM call failed for improving idea {idea_data.get('id')}")
                improved_idea["description"] += "\n\n[Founder LLM call failed during improvement.]"

            result = {
                "status": "completed",
                "improved_idea": improved_idea
            }

        else:
            logger.warning(f"{self.name} received unknown task type: {task_type}")
            # Keep default failure result from line 28

        self.log_interaction(task_details, result)
        return result

    def get_capabilities(self) -> List[str]:
        """Returns the capabilities of this agent."""
        # Based on PRD and added test
        return ["assess_stakeholders", "validate_best_practices", "assess_implementation_path", "improve_idea"] # Added improve_idea