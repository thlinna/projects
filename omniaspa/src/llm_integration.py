"""LLM Integration Module."""

import logging
from typing import Dict, Any, Optional
import os

# Import configuration and client libraries
from src import config
try:
    import openai
except ImportError:
    openai = None
try:
    import anthropic
except ImportError:
    anthropic = None
try:
    import google.generativeai as genai
except ImportError:
    genai = None
try:
    import ollama
except ImportError:
    ollama = None

logger = logging.getLogger(__name__)

# --- Client Initialization ---
# Initialize clients based on available keys in config
openai_client = None
if openai and config.OPENAI_API_KEY:
    try:
        openai_client = openai.OpenAI(api_key=config.OPENAI_API_KEY)
        logger.info("OpenAI client initialized.")
    except Exception as e:
        logger.error(f"Failed to initialize OpenAI client: {e}")

anthropic_client = None
if anthropic and config.ANTHROPIC_API_KEY:
    try:
        anthropic_client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)
        logger.info("Anthropic client initialized.")
    except Exception as e:
        logger.error(f"Failed to initialize Anthropic client: {e}")

google_client = None
if genai and config.GOOGLE_API_KEY:
    try:
        genai.configure(api_key=config.GOOGLE_API_KEY)
        # We'll create the model object later based on the specific model requested
        logger.info("Google GenerativeAI configured.")
        google_client = genai # Use the configured module itself as a flag/client
    except Exception as e:
        logger.error(f"Failed to configure Google GenerativeAI: {e}")

ollama_client = None
if ollama:
    logger.info("Attempting to initialize Ollama client...") # ADDED
    try:
        # The ollama library uses environment variables OLLAMA_HOST or defaults
        # Or you can specify host in client: ollama.Client(host=config.OLLAMA_BASE_URL)
        # Let's rely on environment or default for now, but check connectivity.
        # ollama.Client() will raise if it cannot connect
        logger.info(f"Creating Ollama client with host: {config.OLLAMA_BASE_URL}") # ADDED
        temp_client = ollama.Client(host=config.OLLAMA_BASE_URL) # Use temp variable
        logger.info("Ollama client object created. Attempting connection test (list)...") # ADDED
        temp_client.list() # Test connection
        logger.info("Ollama connection test successful. Assigning client.") # ADDED
        ollama_client = temp_client # Assign only if successful
        logger.info(f"Ollama client initialized and connected to {config.OLLAMA_BASE_URL}.")
    except Exception as e:
        logger.warning(f"Failed during Ollama client initialization or connection test at {config.OLLAMA_BASE_URL}: {e}. Ollama models will be unavailable.", exc_info=True) # Modified log message
        ollama_client = None # Ensure client is None if connection failed
else: # ADDED else block
   logger.warning("Ollama library not found or import failed. Ollama provider is unavailable.")
openrouter_client = None
if openai and config.OPENROUTER_API_KEY: # Use openai library for OpenRouter
    try:
        openrouter_client = openai.OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=config.OPENROUTER_API_KEY,
        )
        logger.info("OpenRouter client initialized (using OpenAI library).")
        # Optional: Add a test call here if needed, e.g., list models
        # openrouter_client.models.list()
    except Exception as e:
        logger.error(f"Failed to initialize OpenRouter client: {e}")


# --- Main LLM Call Function ---

def call_llm(
    prompt: str,
    provider: str = config.LLM_PROVIDER_DEFAULT,
    model: str = config.LLM_MODEL_DEFAULT,
    max_tokens: int = 1000,
    temperature: float = 0.7,
    system_prompt: Optional[str] = None # Added system prompt capability
) -> Optional[str]:
    """
    Calls the specified Large Language Model provider and model.
    """
    logger.info(f"--- LLM CALL ---")
    logger.info(f"Provider: {provider}, Model: {model}")
    logger.debug(f"Prompt: {prompt[:200]}...") # Log more prompt for debugging
    logger.info(f"Params: max_tokens={max_tokens}, temperature={temperature}")
    if system_prompt:
         logger.debug(f"System Prompt: {system_prompt[:100]}...")

    response_text: Optional[str] = None

    try:
        if provider == "placeholder":
            response_text = f"[Placeholder LLM Response for '{model}' based on prompt: '{prompt[:50]}...']"
            logger.info(f"Returning placeholder response.")

        elif provider == "openai":
            if not openai_client:
                logger.error("OpenAI client not initialized or API key missing.")
                return None
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})

            response = openai_client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
                # Add other relevant parameters if needed
            )
            response_text = response.choices[0].message.content

        elif provider == "anthropic":
            if not anthropic_client:
                logger.error("Anthropic client not initialized or API key missing.")
                return None
            # Anthropic API structure differs slightly
            response = anthropic_client.messages.create(
                model=model,
                max_tokens=max_tokens,
                temperature=temperature,
                system=system_prompt if system_prompt else None,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            # Handle potential list of content blocks
            if response.content and isinstance(response.content, list):
                 response_text = "".join(block.text for block in response.content if hasattr(block, 'text'))
            elif hasattr(response.content, 'text'): # Handle single block case if API changes
                 response_text = response.content.text
            else:
                 response_text = str(response.content) # Fallback

        elif provider == "google":
            if not google_client:
                logger.error("Google GenerativeAI not configured or API key missing.")
                return None
            # Instantiate the specific model
            gemini_model = google_client.GenerativeModel(model)
            # Construct content, handling system prompt if provided
            content_to_send = [prompt]
            # Note: Gemini API has specific ways to handle system instructions,
            # often via model tuning or specific parameters, not a direct 'system' role like others.
            # We might prepend it to the user prompt or use specific generation_config.
            if system_prompt:
                 logger.warning("System prompt provided for Google Gemini, prepending to user prompt (may need adjustment based on model).")
                 content_to_send = [system_prompt, prompt]

            # Configure generation parameters
            generation_config = genai.types.GenerationConfig(
                max_output_tokens=max_tokens,
                temperature=temperature
            )
            response = gemini_model.generate_content(
                content_to_send,
                generation_config=generation_config
                )
            # Safety settings might block responses, check response.text
            if response.parts:
                 response_text = "".join(part.text for part in response.parts)
            else:
                 logger.warning(f"Google Gemini response blocked or empty. Prompt feedback: {response.prompt_feedback}")
                 response_text = f"[Google Gemini response blocked or empty. Feedback: {response.prompt_feedback}]"


        elif provider == "ollama":
            if not ollama_client:
                logger.error("Ollama client not initialized or failed to connect.")
                return None
            messages = []
            if system_prompt:
                messages.append({'role': 'system', 'content': system_prompt})
            messages.append({'role': 'user', 'content': prompt})

            response = ollama_client.chat(
                model=model,
                messages=messages,
                options={ # Ollama uses 'options' for parameters
                    'temperature': temperature,
                    'num_predict': max_tokens # num_predict often controls max tokens in Ollama
                }
            )
            response_text = response['message']['content']

        elif provider == "openrouter":
            if not openrouter_client:
                logger.error("OpenRouter client not initialized or API key missing.")
                return None
            # Use the OpenAI compatible client
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})

            response = openrouter_client.chat.completions.create(
                model=model, # Model name like 'nousresearch/nous-capybara-7b'
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
            )
            response_text = response.choices[0].message.content

        else:
            logger.error(f"Unsupported LLM provider specified: {provider}")
            return None

    except Exception as e:
        logger.error(f"Error during LLM call to {provider} ({model}): {e}", exc_info=True)
        return f"[ERROR calling {provider} LLM: {e}]" # Return error message instead of None

    logger.info(f"LLM call successful. Response length: {len(response_text) if response_text else 0}")
    logger.debug(f"LLM Response: {response_text[:200] if response_text else 'None'}...")
    return response_text