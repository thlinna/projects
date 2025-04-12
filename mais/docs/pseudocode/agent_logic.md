# Agenttien Logiikka (Pseudokoodi)

Tämä dokumentti kuvaa kunkin agentin ylätason toimintalogiikan.

## Yleinen Agentin Rakenne (Konseptuaalinen)

```pseudocode
CLASS BaseAgent:
    FUNCTION __init__(config, blackboard_adapter, llm_client):
        this.config = config
        this.blackboard = blackboard_adapter
        this.llm = llm_client

    FUNCTION can_activate(current_mode, blackboard_state):
        // Palauttaa True, jos agentti voi aktivoitua nykyisessä tilassa ja Blackboardin tilassa
        // Esim. tarkistaa, onko relevanttia uutta dataa tai onko oikea moodi päällä
        RETURN [TODO: Agenttikohtainen logiikka]

    FUNCTION process(blackboard_state):
        // Agentin päälogiikka: lukee Blackboardilta, prosessoi (mahd. LLM-kutsut), tuottaa tuloksen
        // Palauttaa datan, joka kirjoitetaan Blackboardille
        input_data = this.blackboard.read_relevant_data(this.config.relevant_keys)
        prompt = this.generate_prompt(input_data) // Luo LLM-promptin
        llm_response = this.llm.generate(prompt)
        output_data = this.parse_response(llm_response)
        RETURN output_data

    FUNCTION execute():
        IF this.can_activate(getCurrentMode(), this.blackboard.get_state()):
            result = this.process(this.blackboard.get_state())
            this.blackboard.write_data(this.config.output_key, result)
            Log("Agent " + this.name + " executed.")
        ELSE:
            Log("Agent " + this.name + " did not activate.")
```

---

### IdeationAgent

```pseudocode
CLASS IdeationAgent INHERITS BaseAgent:
    FUNCTION can_activate(mode, state):
        RETURN mode == "[Mode: Brainstorming]" AND state.contains_new_topic_or_request()

    FUNCTION generate_prompt(input_data):
        topic = input_data.get_topic()
        existing_ideas = input_data.get_ideas()
        prompt = "Given the topic '" + topic + "' and existing ideas: " + existing_ideas + ". Generate [N] new, distinct ideas."
        RETURN prompt

    FUNCTION parse_response(llm_response):
        // Poimi ideat LLM:n vastauksesta
        new_ideas = [TODO: Parse ideas from llm_response]
        RETURN { "new_ideas": new_ideas }
```

---

### ElaborationAgent

```pseudocode
CLASS ElaborationAgent INHERITS BaseAgent:
    FUNCTION can_activate(mode, state):
        RETURN (mode == "[Mode: Brainstorming]" OR mode == "[Mode: Elaboration]") AND state.contains_ideas_needing_elaboration()

    FUNCTION generate_prompt(input_data):
        idea_to_elaborate = input_data.get_next_unelaborated_idea()
        prompt = "Elaborate on the following idea: '" + idea_to_elaborate + "'. Provide details, potential benefits, and drawbacks."
        RETURN prompt

    FUNCTION parse_response(llm_response):
        elaboration_details = [TODO: Parse details from llm_response]
        RETURN { "idea_id": idea_to_elaborate.id, "elaboration": elaboration_details }
```

---

### CriticAgent

```pseudocode
CLASS CriticAgent INHERITS BaseAgent:
    FUNCTION can_activate(mode, state):
        RETURN mode == "[Mode: Evaluation]" AND state.contains_ideas_needing_critique()

    FUNCTION generate_prompt(input_data):
        idea_to_critique = input_data.get_next_uncritiqued_idea()
        prompt = "Provide constructive criticism for the idea: '" + idea_to_critique.text + "'. Identify potential flaws, risks, or ambiguities. Suggest improvements if possible."
        RETURN prompt

    FUNCTION parse_response(llm_response):
        critique = [TODO: Parse critique from llm_response]
        RETURN { "idea_id": idea_to_critique.id, "critique": critique }
```

---

### GuardianAgent

```pseudocode
CLASS GuardianAgent INHERITS BaseAgent:
    FUNCTION can_activate(mode, state):
        RETURN (mode == "[Mode: Evaluation]" OR mode == "[Mode: FactChecking]") AND state.contains_new_claims_to_verify()

    FUNCTION process(blackboard_state):
        claims = blackboard_state.get_new_claims()
        verified_results = []
        FOR claim IN claims:
            is_accurate, correction = this.verify_fact(claim) // Voi sisältää API-kutsun
            verified_results.append({ "claim_id": claim.id, "is_accurate": is_accurate, "correction": correction })
        RETURN { "verifications": verified_results }

    FUNCTION verify_fact(claim):
        // [TODO: Toteuta faktantarkistuslogiikka, esim. API-kutsu ulkoiseen palveluun]
        // Palauttaa (True/False, mahdollinen korjaus tai selitys)
        RETURN (True, None) // Placeholder
```

---

### SummarizerAgent

```pseudocode
CLASS SummarizerAgent INHERITS BaseAgent:
    FUNCTION can_activate(mode, state):
        // Aktivoituu omassa tilassaan tai jos tietty aika/viestimäärä ylittyy
        RETURN mode == "[Mode: Synthesis]" OR state.summary_needed_based_on_time_or_count()

    FUNCTION generate_prompt(input_data):
        conversation_history = input_data.get_recent_history()
        prompt = "Summarize the key points, decisions, and open questions from the following conversation history:\n" + conversation_history
        RETURN prompt

    FUNCTION parse_response(llm_response):
        summary = [TODO: Parse summary from llm_response]
        RETURN { "summary": summary }