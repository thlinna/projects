Selvä asia! Luodaan nyt ehdotetun tiedostorakenteen mukaiset Markdown-tiedostot esitäytettyinä projektille mais ("Multi-Agent Ideation System"). Saat nämä kopiointivalmiina pohjina, joita voit sitten itse tarkentaa ja viimeistellä.

Tiedosto: mais/README.md

Markdown

# Multi-Agent Ideation System (MAIS) for Roo Code

Tämä projekti toteuttaa moniagenttijärjestelmän (MAS) ideointiin ja yhteiskehittelyyn SPARC-mallin (System for Promoting Agent-based Reasoning and Collaboration) mukaisesti. Järjestelmä on suunniteltu integroitavaksi Roo Code -ympäristöön hyödyntäen sen tiloja (`.roomodes`) ja automaattista tilanvaihtoa (Boomerang).

## Projektin kuvaus

MAIS käyttää useita erikoistuneita tekoälyagentteja (Ideation, Elaboration, Critic, Guardian, Summarizer) vuorovaikutuksessa keskenään (ensisijaisesti Blackboard-arkkitehtuurilla) tuottaakseen, jalostaakseen, kritisoidakseen ja tiivistääkseen ideoita iteratiivisesti. Tavoitteena on luoda dynaaminen ja tehokas ympäristö luovalle ongelmanratkaisulle ja "vibe-coding"-tyyppiselle kehitykselle.

Lisätietoja arkkitehtuurista ja vaatimuksista löytyy `docs/`-kansiosta, erityisesti `docs/PRD.md`.

## Asennus

Tarkemmat asennusohjeet löytyvät tiedostosta `docs/setup_guide.md`. Lyhyesti:

1.  Kloonaa repositorio: `git clone [repositorion osoite]`
2.  Siirry projektihakemistoon: `cd mais`
3.  Luo ja aktivoi virtuaaliympäristö (suositeltavaa):
    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/macOS
    # venv\Scripts\activate  # Windows
    ```
4.  Asenna riippuvuudet: `pip install -r requirements.txt`
5.  Määritä ympäristömuuttujat: Kopioi `config/.env.example` tiedostoksi `config/.env` ja täytä tarvittavat arvot (esim. API-avaimet).
6.  (Docker) Rakenna Docker-image: `docker build -t mais-app .`

## Käyttö

[TODO: Lisää tähän lyhyt esimerkki tai ohjeistus järjestelmän käynnistämisestä ja peruskäytöstä Roo Coden sisällä tai erillisenä skriptinä, viitaten tarvittaessa tarkempaan dokumentaatioon.]

Esimerkki (konseptuaalinen):
Roo Code -ympäristössä
/load_mais_system topic="Kestävä energia tulevaisuudessa"

Järjestelmä aloittaa iteroinnin...

## Testaus

Testien ajaminen:

```bash
# Varmista, että olet aktivoinut virtuaaliympäristön ja asentanut riippuvuudet

# Aja kaikki testit
pytest tests/

# Aja vain yksikkötestit
pytest tests/unit/

# Aja vain integraatiotestit
pytest tests/integration/

# Aja testit ja näytä kattavuusraportti (vaatii pytest-cov)
pytest --cov=src tests/
Osallistuminen (Contributing)
[TODO: Lisää ohjeet siitä, miten muut voivat osallistua projektiin, esim. bugiraportit, ominaisuuspyynnöt, koodikontribuutiot.]

Lisenssi
[TODO: Määritä projektin lisenssi, esim. MIT, Apache 2.0.]


---

**Tiedosto: `mais/docs/PRD.md`**

```markdown
# Product Requirements Document: Multi-Agent Ideation System (MAIS)

**Versio:** 0.1
**Päiväys:** 2025-04-12
**Omistaja:** [TODO: Product Owner / Projektipäällikkö]

---

**Sisällysluettelo**
1.  [Johdanto ja Tavoitteet](#1-johdanto-ja-tavoitteet-miksi)
2.  [Kohdeyleisö ja Käyttäjät](#2-kohdeyleisö-ja-käyttäjät-kenelle)
3.  [Käyttäjätarinat / Käyttötapaukset](#3-käyttäjätarinat--käyttötapaukset-mitä-käyttäjä-tekee)
4.  [Ratkaisu ja Tekninen Toteutus](#4-ratkaisu-ja-tekninen-toteutus-miten)
5.  [Ei-funktionaaliset Vaatimukset](#5-ei-funktionaaliset-vaatimukset)
6.  [Datanhallinta](#6-datanhallinta)
7.  [Testausstrategia](#7-testausstrategia)
8.  [Rajaukset (Out of Scope)](#8-rajaukset-out-of-scope)
9.  [Julkaisukriteerit](#9-julkaisukriteerit)
10. [Avoimet Kysymykset](#10-avoimet-kysymykset)

---

## 1. Johdanto ja Tavoitteet (MIKSI?)

* **Ongelma:** [TODO: Kuvaa selkeästi ongelma, jonka MAIS ratkaisee. Esim. perinteisten ideointimenetelmien hitaus, ryhmäajattelun riskit, faktapohjan puute luovissa prosesseissa.]
* **Visio:** [TODO: Kuvaa lyhyesti järjestelmän päätarkoitus ja tulevaisuuden tavoitetila. Esim. "Luoda Roo Codeen integroitu älykäs assistentti, joka kiihdyttää ja parantaa ideointiprosessien laatua agenttipohjaisen yhteistyön avulla."]
* **Liiketoiminnalliset tavoitteet:** [TODO: Listaa konkreettisia hyötyjä. Esim. "Lyhentää ideointiin kuluvaa aikaa 20%", "Parantaa kehitettyjen ratkaisujen innovatiivisuutta", "Vähentää manuaalista tiedonhakua ja faktantarkistusta".]
* **Onnistumisen mittarit:** [TODO: Miten menestystä mitataan? Esim. "Käyttäjätyytyväisyyskyselyn tulos > 4/5", "Generoitujen ja jatkokehitykseen valittujen ideoiden määrä", "Prosessin läpimenoaika verrattuna manuaaliseen prosessiin".]

## 2. Kohdeyleisö ja Käyttäjät (KENELLE?)

* **Ensisijaiset käyttäjät:** [TODO: Määrittele tarkemmin, ketkä ovat pääkäyttäjiä. Esim. Ohjelmistokehittäjät, data scientistit, tutkijat, tuotepäälliköt, UX-suunnittelijat, jotka käyttävät Roo Codea.]
* **Käyttäjäpersoonat (valinnainen):**
    * **Persoona 1:** [TODO: Nimi, rooli, tavoitteet, turhautumiset liittyen ideointiin.]
    * **Persoona 2:** [TODO: ...]

## 3. Käyttäjätarinat / Käyttötapaukset (MITÄ KÄYTTÄJÄ TEKEE?)

* **Epic 1:** Järjestelmän käyttöönotto ja ideointisession aloitus.
    * **Story 1.1:** Käyttäjänä haluan käynnistää MAIS-järjestelmän Roo Codesta komennolla `/mais_start` ja antaa sille aiheen X, jotta voin aloittaa ideoinnin.
    * **Story 1.2:** Käyttäjänä haluan nähdä vahvistuksen, että järjestelmä on käynnistynyt ja IdeationAgent on aloittanut toimintansa.
* **Epic 2:** Ideoiden generointi ja jalostus.
    * **Story 2.1:** Käyttäjänä haluan IdeationAgentin tuottavan vähintään [N] erilaista alkuperäistä ideaa annettuun aiheeseen liittyen.
    * **Story 2.2:** Käyttäjänä haluan ElaborationAgentin laajentavan automaattisesti jokaista uutta ideaa lisätiedoilla ja mahdollisilla käyttötapauksilla.
* **Epic 3:** Ideoiden arviointi ja laadunvarmistus.
    * **Story 3.1:** Käyttäjänä haluan CriticAgentin arvioivan esitettyjä ideoita ja nostavan esiin potentiaalisia heikkouksia tai riskejä.
    * **Story 3.2:** Käyttäjänä haluan GuardianAgentin tarkistavan faktaväittämiä keskustelussa ja ilmoittavan tai korjaavan havaitsemansa virheet.
* **Epic 4:** Prosessin seuranta ja yhteenveto.
    * **Story 4.1:** Käyttäjänä haluan SummarizerAgentin luovan automaattisesti yhteenvedon keskustelun edistymisestä [X] minuutin välein tai [Y] viestin jälkeen.
    * **Story 4.2:** Käyttäjänä haluan voida pyytää yhteenvedon manuaalisesti komennolla `/mais_summarize`.
* **Epic 5:** Tilojen automaattinen hallinta (Boomerang).
    * **Story 5.1:** Järjestelmänvalvojana haluan Boomerang-toiminnon automaattisesti vaihtavan järjestelmän tilaa `[Mode: Brainstorming]` -> `[Mode: Evaluation]`, kun IdeationAgent on tuottanut riittävän määrän ideoita.
    * **Story 5.2:** Käyttäjänä haluan nähdä ilmoituksen, kun järjestelmän tila vaihtuu automaattisesti.
* [TODO: Lisää muita relevantteja käyttäjätarinoita.]

## 4. Ratkaisu ja Tekninen Toteutus (MITEN?)

* **Yleiskatsaus:** Järjestelmä toteutetaan Pythonilla moniagenttijärjestelmänä, joka hyödyntää [Valittu arkkitehtuuri: Blackboard / Orchestrator] -mallia ja integroidaan Roo Codeen. Agentit ovat modulaarisia komponentteja, jotka kommunikoivat keskenään ja reagoivat järjestelmän tilaan.
* **Arkkitehtuuri:**
    * **SPARC-malli:** Järjestelmä noudattaa SPARC-mallin periaatteita: erikoistuneet agentit, iteratiivinen yhteiskehittely, faktapohjaisuus ja jatkuva parantaminen. [TODO: Tähän voi lisätä lyhyen viittauksen alkuperäiseen SPARC-kuvaukseen tai liittää sen osaksi dokumenttia.]
    * **Valittu Arkkitehtuuri:** [TODO: Vahvista valinta: Blackboard / Orchestrator. Perustele lyhyesti valinta.]
    * **Arkkitehtuurikaaviot:**
        * Ks. `docs/architecture/blackboard_arch.mermaid`
        * Ks. `docs/architecture/orchestrator_arch.mermaid` (vaihtoehtoinen)
* **Agentit:**
    * **Roolit ja Vastuut:** (Kuten aiemmin määritelty: Ideation, Elaboration, Critic, Guardian, Summarizer).
    * **Tarkemmat funktionaaliset vaatimukset / Pseudokoodi:**
        * Ks. `docs/pseudocode/agent_logic.md`
* **Roo Code Integraatio:**
    * **`.roomodes` (Tilat):** Järjestelmä käyttää seuraavia tiloja: `[Mode: Idle]`, `[Mode: Brainstorming]`, `[Mode: Elaboration]`, `[Mode: Evaluation]`, `[Mode: FactChecking]`, `[Mode: Synthesis]`. [TODO: Vahvista tai muokkaa tiloja tarpeen mukaan.] Tilat ohjaavat, mitkä agentit ovat aktiivisia tai priorisoituja.
    * **Boomerang (Automaattinen Tilanvaihto):** Tilanvaihto tapahtuu automaattisesti ennalta määriteltyjen sääntöjen perusteella.
        * **Tarkemmat säännöt / Pseudokoodi:** Ks. `docs/pseudocode/boomerang_logic.md`
* **Käyttöliittymä / Interaktio:** Käyttäjä kommunikoi järjestelmän kanssa Roo Coden komentojen (esim. `/mais_start`, `/mais_stop`, `/mais_summarize`) ja järjestelmän tuottamien viestien kautta. [TODO: Tarkenna tätä tarvittaessa.]
* **Sekvenssikaaviot:**
    * Ks. `docs/architecture/sequence_diagrams/ideation_cycle.mermaid` (Esimerkki)
    * Ks. `docs/architecture/sequence_diagrams/boomerang_switch.mermaid` (Esimerkki)
    * [TODO: Luo lisää tarvittavia sekvenssikaavioita kuvaamaan keskeisiä prosesseja.]

## 5. Ei-funktionaaliset Vaatimukset

* **Suorituskyky:**
    * Agentin reaktioaika (inputista outputtiin): Tavoite < [X] sekuntia keskimäärin.
    * Yhteenvedon generointiaika: Tavoite < [Y] sekuntia.
    * [TODO: Lisää muita suorituskykyvaatimuksia.]
* **Skaalautuvuus:**
    * Järjestelmän tulee pystyä käsittelemään [Z] samanaikaista ideointisessiota (jos relevantti).
    * Blackboardin tulee pystyä käsittelemään [W] määrä tietoa ilman merkittävää hidastumista.
* **Luotettavuus:**
    * Järjestelmän tulee olla vikasietoinen agenttien yksittäisten virheiden varalta (esim. LLM-kutsun epäonnistuminen).
    * Tavoiteltu käytettävyys: [esim. 99.5%].
* **Tietoturva:**
    * API-avaimet ja muut salaisuudet tulee hallita turvallisesti (ei kovakoodata, käyttää ympäristömuuttujia / konfiguraatiotiedostoja).
    * [TODO: Muita tietoturvavaatimuksia?]
* **Ylläpidettävyys:**
    * Koodin tulee noudattaa [esim. PEP 8] -tyyliohjeita.
    * Koodi tulee olla modulaarista ja kommentoitua tarvittavilta osin.
    * Lokituksen tulee olla riittävää ongelmien diagnosointiin.

## 6. Datanhallinta

* **Blackboardin Tila:** [TODO: Määrittele, miten Blackboardin tila tallennetaan ajon aikana (esim. Python-olio muistissa, väliaikainen tiedosto) ja tarvitaanko pysyväistallennusta sessioiden välillä.]
* **Lokitus:** Lokit kirjoitetaan [esim. standard outputtiin / tiedostoon (`data/app.log`)]. Lokitustaso on konfiguroitavissa.

## 7. Testausstrategia

* **Yksikkötestit:** Kattavat agenttien ydinlogiikan, apufunktiot ja core-komponentit (Blackboard/Orchestrator). Käytetään `pytest` ja `unittest.mock`.
* **Integraatiotestit:** Varmistavat komponenttien välisen yhteistoiminnan (agenttien ketjutus, Boomerang-logiikka). Käytetään `pytest`.
* **E2E-testit:** Testataan koko järjestelmän toimintaa simuloidussa ympäristössä, ajetaan Docker-kontissa.
* **Kattavuus:** Tavoitteena [esim. > 80%] testikattavuus kriittisille moduuleille.
* **CI/CD:** Testit integroidaan osaksi CI/CD-putkea.

## 8. Rajaukset (Out of Scope)

* [TODO: Listaa ominaisuudet, joita EI toteuteta tässä versiossa. Esimerkkejä:]
    * Graafinen käyttöliittymä.
    * Usean käyttäjän samanaikainen reaaliaikainen editointi.
    * Edistynyt luonnollisen kielen komentojen tulkinta (käytetään ennalta määriteltyjä komentoja).
    * Useiden eri LLM-mallien tuki ajon aikana vaihdettavaksi (tuetaan yhtä konfiguroitua mallia per ajo).

## 9. Julkaisukriteerit

* **MVP (Minimum Viable Product):**
    * [TODO: Listaa MVP:hen kuuluvat ydintoiminnallisuudet. Esim:]
        * Käynnistys ja aiheen anto Roo Codesta.
        * Ideation, Elaboration ja Critic -agenttien perustoiminnallisuus Blackboardilla.
        * Manuaalisesti käynnistettävä Summarizer.
        * Peruslokitus.
        * Toimiva Docker-paketointi.
* **Hyväksymiskriteerit:**
    * Kaikki MVP-käyttäjätarinat on toteutettu ja testattu.
    * Ei kriittisiä tai blokkaavia bugeja.
    * Dokumentaatio (README, setup) on ajan tasalla.
    * Testikattavuus täyttää tavoitteen.

## 10. Avoimet Kysymykset

* [TODO: Listaa kysymyksiä, jotka vaativat vielä selvitystä tai päätöksiä. Esim:]
    * Miten GuardianAgentin ulkoiset tietolähteet toteutetaan (API, paikallinen tietokanta)?
    * Tarkat suorituskykytavoitteet ja miten niitä mitataan?
    * Tarvitaanko käyttäjäkohtaista konfiguraatiota agenteille?
    * Lisensointimalli?

Tiedosto: mais/docs/architecture/index.md

Markdown

# Arkkitehtuuridokumentaatio

Tämä osio sisältää MAIS-järjestelmän arkkitehtuurikuvaukset ja kaaviot.

## Pääarkkitehtuurit

* **[Blackboard-arkkitehtuuri (Suositeltu)](blackboard_arch.mermaid)**: Kuvaa järjestelmän toiminnan jaetun tietovaraston (Blackboard) kautta.
* **[Orchestrator-arkkitehtuuri (Vaihtoehtoinen)](orchestrator_arch.mermaid)**: Kuvaa järjestelmän toiminnan keskitetyn ohjaajan (Orchestrator) kautta.

## Sekvenssikaaviot

Sekvenssikaaviot kuvaavat tarkemmin komponenttien välistä vuorovaikutusta eri prosesseissa.

* **[Esimerkki: Ideointisykli](sequence_diagrams/ideation_cycle.mermaid)**: Kuvaa tyypillisen vuorovaikutusketjun idean generoinnista sen jalostukseen ja kritisointiin.
* **[Esimerkki: Boomerang-tilanvaihto](sequence_diagrams/boomerang_switch.mermaid)**: Kuvaa, miten järjestelmän tila voi vaihtua automaattisesti agentin toiminnan seurauksena.
* [TODO: Lisää linkkejä muihin tarvittaviin sekvenssikaavioihin.]

Tiedosto: mais/docs/architecture/blackboard_arch.mermaid

Code snippet

graph TD
    subgraph SPARC Multi-Agent System (Blackboard Architecture)
        User -- Input/Query --> Blackboard[/<font size=5>📝</font><br/><b>Blackboard</b><br/>Shared Knowledge State/]
        Blackboard -- Reads Data & Writes Ideas --> Ideation(💡<br/>Ideation Agent)
        Blackboard -- Reads Ideas & Writes Details --> Elaboration(🧩<br/>Elaboration Agent)
        Blackboard -- Reads Ideas/Details & Writes Critique --> Critic(🤔<br/>Critic Agent)
        Blackboard -- Reads Claims & Writes Corrections --> Guardian(🛡️<br/>Guardian Agent)
        Guardian -- Checks Facts --> ExternalKB[(🌐<br/>External Knowledge / API)]
        Blackboard -- Reads Conversation & Writes Summary --> Summarizer(📜<br/>Summarizer Agent)

        Ideation -- Writes Ideas --> Blackboard
        Elaboration -- Writes Details --> Blackboard
        Critic -- Writes Critique --> Blackboard
        Guardian -- Writes Corrections --> Blackboard
        Summarizer -- Writes Summary --> Blackboard

        %% Roo Code Specifics
        RC[(<font size=5>⚙️</font><br/>Roo Code Environment)] -- Manages Modes & Boomerang --> AgentActivationLogic{Agent Activation Logic}
        AgentActivationLogic -- Activates/Deactivates --> Ideation
        AgentActivationLogic -- Activates/Deactivates --> Elaboration
        AgentActivationLogic -- Activates/Deactivates --> Critic
        AgentActivationLogic -- Activates/Deactivates --> Guardian
        AgentActivationLogic -- Activates/Deactivates --> Summarizer
        Blackboard -- Triggers Mode Change via Boomerang --> RC
    end

    style Blackboard fill:#fdfd96,stroke:#333,stroke-width:2px
    style RC fill:#add8e6,stroke:#333,stroke-width:2px
Tiedosto: mais/docs/architecture/orchestrator_arch.mermaid

Code snippet

graph TD
    subgraph SPARC Multi-Agent System (Orchestrator Architecture)
        User -- Input/Query --> Orchestrator{<font size=5> orchestrator </font><br/><b>Orchestrator Agent</b><br/>Controls Flow & State};

        Orchestrator -- Task: Generate Ideas --> Ideation(💡<br/>Ideation Agent);
        Ideation -- Results: Ideas --> Orchestrator;

        Orchestrator -- Task: Elaborate Idea --> Elaboration(🧩<br/>Elaboration Agent);
        Elaboration -- Results: Details --> Orchestrator;

        Orchestrator -- Task: Critique Idea --> Critic(🤔<br/>Critic Agent);
        Critic -- Results: Critique --> Orchestrator;

        Orchestrator -- Task: Verify Claim --> Guardian(🛡️<br/>Guardian Agent);
        Guardian -- Checks Facts --> ExternalKB[(🌐<br/>External Knowledge / API)];
        Guardian -- Results: Verification/Correction --> Orchestrator;

        Orchestrator -- Task: Summarize --> Summarizer(📜<br/>Summarizer Agent);
        Summarizer -- Results: Summary --> Orchestrator;

        Orchestrator -- Output/Update --> User;

        %% Roo Code Specifics
        RC[(<font size=5>⚙️</font><br/>Roo Code Environment)] -- Manages Modes & Boomerang --> Orchestrator
        Orchestrator -- Applies Mode Logic --> Orchestrator
        Orchestrator -- Triggers Mode Change via Boomerang --> RC
    end

    style Orchestrator fill:#cfe2f3,stroke:#333,stroke-width:2px
    style RC fill:#add8e6,stroke:#333,stroke-width:2px
Tiedosto: mais/docs/architecture/sequence_diagrams/ideation_cycle.mermaid

Code snippet

sequenceDiagram
    participant User
    participant RooCode as Roo Code Env
    participant Blackboard
    participant IdeationAgent as Ideation Agent
    participant ElaborationAgent as Elaboration Agent
    participant CriticAgent as Critic Agent

    Note over User, CriticAgent: Example Ideation Cycle (Simplified)

    User->>RooCode: /mais_start topic="New Feature X"
    RooCode->>Blackboard: Initialize(topic="New Feature X")
    RooCode->>IdeationAgent: Activate (Mode: Brainstorming)

    IdeationAgent->>Blackboard: Read Topic
    Note over IdeationAgent: Generating ideas...
    IdeationAgent->>Blackboard: Write Idea 1, Idea 2

    Blackboard->>RooCode: Notify Update (New Ideas)
    RooCode->>ElaborationAgent: Activate

    ElaborationAgent->>Blackboard: Read Idea 1, Idea 2
    Note over ElaborationAgent: Elaborating...
    ElaborationAgent->>Blackboard: Write Details for Idea 1
    ElaborationAgent->>Blackboard: Write Details for Idea 2

    Blackboard->>RooCode: Notify Update (Elaborations)
    RooCode->>CriticAgent: Activate

    CriticAgent->>Blackboard: Read Idea 1 + Details
    Note over CriticAgent: Critiquing Idea 1...
    CriticAgent->>Blackboard: Write Critique for Idea 1

    CriticAgent->>Blackboard: Read Idea 2 + Details
    Note over CriticAgent: Critiquing Idea 2...
    CriticAgent->>Blackboard: Write Critique for Idea 2

    Blackboard->>RooCode: Notify Update (Critiques)
    RooCode->>User: Display Updated Ideas/Critiques

    Note over User, CriticAgent: Cycle continues or mode changes...
Tiedosto: mais/docs/architecture/sequence_diagrams/boomerang_switch.mermaid

Code snippet

sequenceDiagram
    participant AgentX as Triggering Agent (e.g., Ideation)
    participant Blackboard
    participant RooInterface as Roo Interface/Mode Controller
    participant AgentY as Next Agent (e.g., Critic)

    Note over AgentX, AgentY: Example Boomerang Mode Switch

    AgentX->>Blackboard: Write Output (e.g., N new ideas)

    Blackboard->>RooInterface: Notify Update (trigger condition met)

    RooInterface->>RooInterface: Evaluate Boomerang Rules
    Note right of RooInterface: Rule: "IF Mode=Brainstorming AND NewIdeas > 3 THEN SwitchMode(Evaluation)" matches.

    RooInterface->>RooInterface: Change Internal State: Mode = Evaluation

    RooInterface->>AgentX: Deactivate / Lower Priority
    RooInterface->>AgentY: Activate / Raise Priority (Now in Evaluation mode)

    Note over AgentY: AgentY is now active due to mode change.
    AgentY->>Blackboard: Read Data relevant to Evaluation mode

Tiedosto: mais/docs/pseudocode/index.md

Markdown

# Pseudokoodit

Tämä osio sisältää pseudokoodia keskeisille MAIS-järjestelmän toiminnoille.

* **[Agenttien Logiikka](agent_logic.md)**: Kuvaa kunkin agenttityypin perustoimintalogiikan.
* **[Boomerang Tilanvaihtologiikka](boomerang_logic.md)**: Kuvaa säännöt ja logiikan automaattisille tilanvaihdoille.

Tiedosto: mais/docs/pseudocode/agent_logic.md

Markdown

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

IdeationAgent
Code snippet

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
ElaborationAgent
Code snippet

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
CriticAgent
Code snippet

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
GuardianAgent
Code snippet

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
SummarizerAgent
Code snippet

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
Tiedosto: mais/docs/pseudocode/boomerang_logic.md

Markdown

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

Tiedosto: mais/docs/setup_guide.md

Markdown

# Asennusohjeet - MAIS

Tämä opas neuvoo, miten otat Multi-Agent Ideation System (MAIS) -projektin käyttöön kehitysympäristössäsi.

## Esivaatimukset

* Python ([Määritä versio, esim. 3.9+])
* pip (Python package installer)
* Git
* Docker (jos aiot käyttää Docker-kontteja)
* Roo Code -ympäristö (jos aiot integroida järjestelmän siihen)
* [TODO: Mahdolliset muut vaatimukset, esim. API-avaimet LLM-palveluihin]

## Asennusvaiheet

1.  **Kloonaa repositorio:**
    Avaa terminaali tai komentokehote ja suorita komento:
    ```bash
    git clone [projektin Git-repositorion URL]
    cd mais
    ```

2.  **Luo ja aktivoi virtuaaliympäristö:**
    On erittäin suositeltavaa käyttää virtuaaliympäristöä projektin riippuvuuksien eristämiseksi.
    ```bash
    # Luo virtuaaliympäristö nimeltä 'venv'
    python -m venv venv

    # Aktivoi virtuaaliympäristö
    # Linux / macOS:
    source venv/bin/activate
    # Windows (cmd.exe):
    # venv\Scripts\activate.bat
    # Windows (PowerShell):
    # venv\Scripts\Activate.ps1
    ```
    Aktiivisen ympäristön tunnistaa komentokehotteen alussa olevasta `(venv)`-merkinnästä.

3.  **Asenna riippuvuudet:**
    Asenna kaikki projektin vaatimat Python-paketit:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Määritä ympäristömuuttujat:**
    Projektin konfiguraatio (erityisesti API-avaimet) hallitaan ympäristömuuttujien avulla.
    * Kopioi esimerkitiedosto:
        ```bash
        cp config/.env.example config/.env
        ```
    * Avaa `config/.env`-tiedosto tekstieditorilla.
    * Täytä vaaditut arvot (esim. `OPENAI_API_KEY=sk-xxxxxxxx...`). **Älä koskaan lisää `.env`-tiedostoa Git-versionhallintaan!** `.gitignore`-tiedoston tulisi estää tämä.

5.  **Tarkista asennus (Valinnainen):**
    Voit ajaa testit varmistaaksesi, että kaikki on asennettu oikein:
    ```bash
    pytest tests/
    ```

## Docker-asennus

Jos haluat ajaa sovellusta Docker-kontissa:

1.  **Varmista Dockerin asennus:** Varmista, että Docker Desktop tai Docker Engine on asennettu ja käynnissä.

2.  **Rakenna Docker-image:**
    Suorita tämä komento projektin juurihakemistossa (`mais/`):
    ```bash
    docker build -t mais-app .
    ```
    Tämä komento lukee `Dockerfile`-tiedoston ja rakentaa sen ohjeiden mukaisesti imagen nimeltä `mais-app`.

3.  **Aja Docker-kontti:**
    [TODO: Lisää tähän komento, jolla sovellus käynnistetään kontissa. Huomioi ympäristömuuttujien välittäminen ja mahdollisten porttien tai volyymien liittäminen.]
    Esimerkki (voi vaatia tarkennusta):
    ```bash
    # Välittää .env-tiedoston muuttujat kontille
    docker run --rm --env-file ./config/.env -p [HOST_PORT]:[CONTAINER_PORT] mais-app
    ```
    * `--rm`: Poistaa kontin automaattisesti sen sammuttua.
    * `--env-file`: Lukee ympäristömuuttujat annetusta tiedostosta.
    * `-p [HOST_PORT]:[CONTAINER_PORT]`: (Tarvittaessa) Mappaa portin host-koneesta kontin sisälle.

## Seuraavat vaiheet

* Tutustu `README.md`-tiedostoon peruskäytöstä.
* Selaa `docs/`-kansiota saadaksesi syvemmän ymmärryksen arkkitehtuurista ja vaatimuksista.
* [TODO: Lisää linkki tai ohjeistus Roo Code -integraation käyttöönottoon, jos se vaatii erillisiä toimenpiteitä.]

Muista, että nämä ovat pohjia. Sinun tulee käydä ne läpi ja täyttää [TODO: ...] -kohdat sekä muut projektisi yksityiskohtia vaativat osiot. Erityisesti PRD vaatii paljon sisältöä liittyen projektin tavoitteisiin ja vaatimuksiin. Onnea projektiin!
