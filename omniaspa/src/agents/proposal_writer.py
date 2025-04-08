# [MermaidChart: 44247d65-ee46-420e-a33a-5bc18cd653bc]
"""Implementation of the Proposal Writer Agent."""

from .base_agent import Agent
from typing import List, Dict, Any
import logging
import json # For parsing potential LLM JSON output

# Import the placeholder LLM call function and config
from src.llm_integration import call_llm
from src import config

logger = logging.getLogger(__name__)

class ProposalWriterAgent(Agent):
    """
    Agent specialized in crafting the final, polished, and winning
    application documents.
    """
    DEFAULT_NAME = "Proposal Writer"

    def __init__(self, name: str = DEFAULT_NAME):
        super().__init__(name)
        logger.info(f"Initialized {self.name}")

    def execute_task(self, task_details: Dict[str, Any]) -> Dict[str, Any]:
        """Executes tasks like writing sections or compiling the final proposal."""
        task_type = task_details.get("type")
        result = {"status": "failed", "output": f"Unknown task type: {task_type}"}

        if task_type == "write_section":
            section_name = task_details.get("section_name", "Unknown Section")
            input_data = task_details.get("input_data", {}) # e.g., key points, related ideas/evals
            logger.info(f"{self.name} writing section: {section_name}")

            # Construct prompt for LLM
            # Enhance prompt with more context if available in input_data
            prompt = (
                f"Write a compelling and well-structured proposal section titled '{section_name}' "
                f"for an EU Digital Europe Programme application. Use the following key points/data:\n"
                f"{input_data}\n\n" # Convert dict/list to string representation
                f"Ensure the language is formal, persuasive, and aligns with typical EU grant requirements."
            )

            # Call LLM (placeholder)
            llm_response_str = call_llm(
                prompt,
                provider=config.LLM_PROVIDER_WRITER, # Specific config for writer
                model=config.LLM_MODEL_WRITER,
                max_tokens=config.LLM_TOKENS_WRITER_SECTION, # Use configurable tokens
                temperature=config.LLM_TEMP_WRITER_SECTION # Use configurable temperature
            )

            # Use response or default
            section_content = llm_response_str if llm_response_str else f"## {section_name}\n\n[Default content for {section_name} - LLM failed]"

            result = {
                "status": "completed",
                "section_content": section_content
            }

        elif task_type == "compile_final_proposal":
            sections = task_details.get("sections", {}) # Dict of section_name: content
            logger.info(f"{self.name} compiling final proposal from {len(sections)} sections.")

            # --- Deduplicate Sections ---
            unique_sections: Dict[str, str] = {}
            seen_content_hashes = set()
            # Sort to process WPs numerically if possible, ensuring the first instance is kept
            sorted_section_items = sorted(sections.items())

            for name, content in sorted_section_items:
                # Simple content hash (consider more robust hashing if needed)
                content_hash = hash(content.strip())
                if content_hash not in seen_content_hashes:
                    unique_sections[name] = content
                    seen_content_hashes.add(content_hash)
                    logger.debug(f"Keeping unique section: {name}")
                else:
                    logger.warning(f"Skipping duplicate content found for section: {name}")

            if len(unique_sections) < len(sections):
                 logger.info(f"Consolidated {len(sections)} sections down to {len(unique_sections)} unique sections.")

            # --- Construct Prompt with Unique Sections ---
            sections_text = ""
            for name, content in unique_sections.items():
                 # Assume content might already have markdown headings
                 sections_text += f"## Section: {name}\n\n{content}\n\n---\n\n"

            prompt = (
                f"You are an expert proposal writer. Your task is to compile the following unique proposal sections into a single, coherent Markdown document. "
                f"Add a brief overall introduction that sets the stage. Ensure logical flow and consistent Markdown formatting between sections.\n\n"
                f"Finally, write a strong, specific conclusion that summarizes the project's main objectives, expected impact (referencing details from the provided sections), and explicitly states its alignment with the Digital Europe Programme's goals.\n\n" # Enhanced conclusion instruction
                f"=== BEGIN UNIQUE SECTIONS TO COMPILE ===\n\n"
                f"{sections_text}" # Use deduplicated sections
                f"=== END UNIQUE SECTIONS TO COMPILE ===\n\n"
                f"The final compiled document should be approximately {config.TARGET_PROPOSAL_LENGTH_DESC} long.\n"
                f"Now, generate the complete, compiled proposal document in Markdown format based *only* on the unique sections provided above."
            )

            # Call LLM (placeholder) - Or just do simple concatenation
            llm_response_str = call_llm(
                prompt,
                provider=config.LLM_PROVIDER_WRITER,
                model=config.LLM_MODEL_WRITER,
                max_tokens=config.MAX_PROPOSAL_LENGTH_TOKENS, # Use configurable target proposal length
                temperature=config.LLM_TEMP_WRITER_COMPILE # Use configurable temperature
            )

            # Simulate compilation or use LLM response
            if llm_response_str:
                    final_md = llm_response_str
            else:
                # Fallback: Simple concatenation
                logger.warning("LLM compilation failed, using simple concatenation.")
                final_md = f"# Final Proposal Document (Compiled by {self.name})\n\n"
                # A real implementation might order sections logically
                for name, content in sections.items():
                    # Assume content already includes heading if generated by write_section
                    final_md += f"{content}\n\n"
                final_md += "---\n*Compiled by Proposal Writer Agent (Fallback)*"


            result = {
                "status": "completed",
                "final_proposal_md": final_md
            }

        else:
            logger.warning(f"{self.name} received unknown task type: {task_type}")

        self.log_interaction(task_details, result)
        return result

    def get_capabilities(self) -> List[str]:
        """Returns the capabilities of this agent."""
        return ["write_section", "compile_final_proposal"]