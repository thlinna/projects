# Boomerang Tilanvaihtologiikka (Pseudokoodi)

Tämä dokumentti kuvaa esimerkkisääntöjä ja logiikkaa automaattisille tilanvaihdoille Roo Code -ympäristössä. Logiikka ajetaan tyypillisesti jokaisen merkittävän Blackboard-päivityksen jälkeen.

```pseudocode
FUNCTION check_and_apply_boomerang_rules(current_mode, blackboard_state):
    new_mode = current_mode // Oletuksena tila ei vaihdu

    // Sääntö 1: Ideoinnista elaboraatioon/arviointiin
    IF current_mode == "[Mode: Brainstorming]":
        new_ideas_count = blackboard_state.count_new_ideas_since_last_check()
        IF new_ideas_count >= [CONFIG.boomerang_idea_threshold]:
            // Vaihtoehto 1: Siirry aina elaboraatioon ensin
            // new_mode = "[Mode: Elaboration]"
            // Vaihtoehto 2: Siirry arviointiin, jos ideoita on tarpeeksi
            new_mode = "[Mode: Evaluation]"
            Log("Boomerang: Switching to Evaluation mode (sufficient ideas generated).")

    // Sääntö 2: Elaboraatiosta arviointiin
    IF current_mode == "[Mode: Elaboration]":
        unelaborated_ideas = blackboard_state.count_unelaborated_ideas()
        IF unelaborated_ideas == 0:
             new_mode = "[Mode: Evaluation]"
             Log("Boomerang: Switching to Evaluation mode (all ideas elaborated).")

    // Sääntö 3: Arvioinnista faktantarkistukseen tai synteesiin
    IF current_mode == "[Mode: Evaluation]":
        uncritiqued_ideas = blackboard_state.count_uncritiqued_ideas()
        unverified_claims = blackboard_state.count_unverified_claims()
        IF uncritiqued_ideas == 0:
            IF unverified_claims > 0:
                new_mode = "[Mode: FactChecking]"
                Log("Boomerang: Switching to FactChecking mode (critiques done, claims need verification).")
            ELSE:
                // Kaikki arvioitu ja tarkistettu (tai ei ollut tarkistettavaa) -> Synteesi
                new_mode = "[Mode: Synthesis]"
                Log("Boomerang: Switching to Synthesis mode (evaluation complete).")

    // Sääntö 4: Faktantarkistuksesta synteesiin
    IF current_mode == "[Mode: FactChecking]":
        unverified_claims = blackboard_state.count_unverified_claims()
        IF unverified_claims == 0:
            new_mode = "[Mode: Synthesis]"
            Log("Boomerang: Switching to Synthesis mode (fact checking complete).")

    // Sääntö 5: Synteesistä takaisin ideointiin tai odotustilaan
    IF current_mode == "[Mode: Synthesis]":
        IF blackboard_state.summary_just_generated():
            // Vaihtoehto: Palataanko aina ideointiin?
            // new_mode = "[Mode: Brainstorming]"
            // Vaihtoehto: Siirrytäänkö odottamaan käyttäjän komentoa?
            new_mode = "[Mode: Idle]"
            Log("Boomerang: Switching to Idle mode after summarization.")

    // [TODO: Lisää muita sääntöjä tarpeen mukaan, esim. ajastettuja vaihtoja]

    // Jos tila on muuttunut, päivitä se Roo Code -rajapinnan kautta
    IF new_mode != current_mode:
        RooInterface.set_mode(new_mode)
        RETURN new_mode // Palauta uusi tila
    ELSE:
        RETURN current_mode // Palauta alkuperäinen tila