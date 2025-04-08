"""Implementation of the Creative Ideator Agent."""

from .base_agent import Agent
from typing import List, Dict, Any
import logging
import uuid # For generating dummy idea IDs
import json # For parsing potential LLM JSON output

# Import the placeholder LLM call function and config
from src.llm_integration import call_llm
from src import config

logger = logging.getLogger(__name__)

class CreativeIdeatorAgent(Agent):
    """
    Agent specialized in generating multiple innovative and viable
    application ideas.
    """
    DEFAULT_NAME = "Creative Ideator"

    def __init__(self, name: str = DEFAULT_NAME):
        super().__init__(name)
        logger.info(f"Initialized {self.name}")

    def execute_task(self, task_details: Dict[str, Any]) -> Dict[str, Any]:
        """Executes tasks like generating new proposal ideas."""
        task_type = task_details.get("type")
        result = {"status": "failed", "output": f"Unknown task type: {task_type}"}

        if task_type == "generate_ideas":
            topic = task_details.get("topic", "general")
            quantity = task_details.get("quantity", 1)
            logger.info(f"{self.name} generating {quantity} ideas on topic: {topic}")

            # Construct prompt for LLM
            prompt = (
                f"Generate {quantity} distinct, innovative, and viable project ideas "
                f"suitable for the EU Digital Europe Programme, focusing on the topic: '{topic}'. "
                f"For each idea, provide a unique ID (uuid), a concise title, and a brief description. "
                f"Format the output as a JSON list of objects, each with 'id', 'title', and 'description' keys."
            )

            # Call the LLM (placeholder for now)
            llm_response_str = call_llm(
                prompt,
                provider=config.LLM_PROVIDER_IDEATOR,
                model=config.LLM_MODEL_IDEATOR,
                max_tokens=config.LLM_TOKENS_IDEATOR,
                temperature=config.LLM_TEMP_IDEATOR # Use configurable temperature
            )

            generated_ideas = []
            if llm_response_str:
                logger.debug(f"Attempting to parse LLM response for JSON. Full response received:\n---\n{llm_response_str}\n---") # Log FULL response
                try:
                    # Attempt to extract JSON list (e.g., find first '[' and last ']')
                    json_start = llm_response_str.find('[')
                    json_end = llm_response_str.rfind(']')

                    if json_start != -1 and json_end != -1 and json_end > json_start:
                        json_str = llm_response_str[json_start:json_end+1]
                        logger.debug(f"Extracted potential JSON string: {json_str[:500]}...")
                        generated_ideas = json.loads(json_str)

                        # Basic validation
                        if not isinstance(generated_ideas, list):
                            logger.warning(f"Parsed JSON is not a list: {type(generated_ideas)}")
                            generated_ideas = [] # Reset if not a list
                        else:
                            # Ensure basic structure and add missing IDs
                            valid_ideas = []
                            for idea in generated_ideas:
                                if isinstance(idea, dict) and 'title' in idea and 'description' in idea:
                                     if 'id' not in idea or not idea['id']: # Add ID if missing or empty
                                         idea['id'] = str(uuid.uuid4())
                                     valid_ideas.append(idea)
                                else:
                                     logger.warning(f"Skipping invalid idea structure: {idea}")
                            generated_ideas = valid_ideas
                            logger.info(f"Successfully parsed {len(generated_ideas)} valid ideas from LLM response.")

                    else:
                        # If no '[' or ']' found, treat as non-JSON
                        logger.warning("Could not find JSON list structure ('[...]') in LLM response. Creating dummy ideas.")
                        # Create dummy ideas using the full response as context/description
                        for i in range(quantity):
                             generated_ideas.append({
                                 "id": str(uuid.uuid4()),
                                 "title": f"Placeholder Idea {i+1} for {topic} (No JSON found)",
                                 "description": llm_response_str
                             })
                except json.JSONDecodeError:
                    logger.error(f"Failed to parse LLM response as JSON: {llm_response_str}")
                    # Fallback: create dummy ideas if parsing fails
                    for i in range(quantity):
                        generated_ideas.append({
                            "id": str(uuid.uuid4()),
                            "title": f"Fallback Idea {i+1} for {topic}",
                            "description": "Could not parse LLM response."
                        })
            else:
                logger.error("LLM call failed or returned empty response.")
                # Fallback: create dummy ideas if LLM fails
                for i in range(quantity):
                    generated_ideas.append({
                        "id": str(uuid.uuid4()),
                        "title": f"Fallback Idea {i+1} for {topic} (LLM Error)",
                        "description": "LLM call failed."
                    })


            result = {
                "status": "completed",
                "generated_ideas": generated_ideas[:quantity] # Ensure we don't exceed requested quantity
            }
        else:
            logger.warning(f"{self.name} received unknown task type: {task_type}")

        self.log_interaction(task_details, result)
        return result

    def get_capabilities(self) -> List[str]:
        """Returns the capabilities of this agent."""
        return ["generate_ideas"]