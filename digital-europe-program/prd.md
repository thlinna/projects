# PRD: Digital Europe AI Funding Generator using Agno Framework

## 1. Product overview
### 1.1 Document title and version
- PRD: Digital Europe AI Funding Generator using Agno Framework
- Version: 1.0

### 1.2 Product summary
This tool is a multi-agent system built on the Agno framework designed to ideate, evaluate, and craft winning funding proposals for the Digital Europe Programme. The system leverages an event-driven, modular architecture where specialized AI agents communicate via Agno’s orchestration layer. The primary agents include:

- **Ideanikkari:** Generates diverse, funding-worthy ideas using the market’s best available AI model.
- **Arvioija:** Evaluates and refines these ideas with advanced AI, providing feedback and suggested improvements.
- **Hakija:** Transforms the best ideas into a structured and compelling funding application.
- **Rahoittaja:** Simulates a funding expert’s review, offering a final check and validation of the proposal.

This document outlines the product requirements and serves as the blueprint for developing a tool that not only improves the success rate of funding applications but also scales for future expansion into additional EU funding streams.

## 2. Goals
### 2.1 Business goals
- Increase the success rate of funding applications submitted for the Digital Europe Programme.
- Reduce the time and effort needed to produce high-quality proposals.
- Create a scalable, SaaS-based solution that can later extend to other EU funding schemes.
- Establish a competitive, market-leading product that attracts consulting firms and enterprise clients.

### 2.2 User goals
- Generate innovative, funding-ready project ideas quickly.
- Obtain expert-level feedback and iterative improvements on proposals.
- Seamlessly convert refined ideas into a fully structured funding application.
- Stay updated with the latest evaluation criteria from the Digital Europe Programme.

### 2.3 Non-goals
- Guarantee funding approval.
- Provide legal, financial, or regulatory advice.
- Completely replace human judgment or expert review.
- Cover all aspects of the funding process in the initial version.

## 3. User personas
### 3.1 Key user types
- **Aloitteleva hakija:** New applicants needing step-by-step guidance.
- **Kokenut hakija:** Experienced organizations aiming to refine their proposals.
- **Rahoituskonsultti:** Professionals managing multiple client projects.
- **Tutkija/kehittäjä:** Research institutions needing structured funding applications.
- **Oppilaitoksen kehittäjä:** Administrators managing funding for educational projects.

### 3.2 Basic persona details
- **Aloitteleva hakija:** Lacks experience with EU funding and requires detailed guidance.
- **Kokenut hakija:** Familiar with the process but seeks efficiency and validation.
- **Rahoituskonsultti:** Works on multiple projects; needs robust project management features.
- **Tutkija/kehittäjä:** Seeks automated structuring to support research funding.
- **Oppilaitoksen kehittäjä:** Requires tools to showcase project impact and compliance.

### 3.3 Role-based access
- **Peruskäyttäjä:** Can create and edit projects, access agent functionalities.
- **Tiimin jäsen:** Collaborates on shared projects with commenting and version control.
- **Konsultti/hallinnoija:** Oversees multiple projects and manages client access.
- **Järjestelmänvalvoja:** Manages technical settings, security, and user roles.

## 4. Functional requirements
- **Ideageneraattori (Ideanikkari)** (Priority: High)
  - Leverages Agno’s messaging and orchestration to invoke the best available AI model for generating funding ideas.
  - Collects input on industry, target market, and project scope.
  - Matches generated ideas against Digital Europe Programme criteria.

- **Ideoiden arviointi (Arvioija)** (Priority: High)
  - Receives ideas from Ideanikkari via Agno’s event triggers.
  - Utilizes advanced AI to score ideas on relevancy, feasibility, and impact.
  - Provides actionable improvement suggestions through iterative dialogue with the user.

- **Hakemusten valmistelu (Hakija)** (Priority: High)
  - Structures the funding proposal with required sections (objectives, plan, budget, impact) based on Agno’s modular workflows.
  - Monitors content length and format according to programme guidelines.
  - Enables dynamic edits and version tracking.

- **Hakemusten arviointi (Rahoittaja)** (Priority: High)
  - Simulates expert review by scoring the final proposal.
  - Generates a detailed “evaluation report” with strengths and areas for improvement.
  - Uses Agno’s integration capabilities to update scoring criteria as programme rules change.

- **Projektinhallinta ja yhteistyö** (Priority: Medium)
  - Supports multiple projects, role-based access, and collaborative editing.
  - Provides notifications, version history, and a progress dashboard.
  - Integrates with popular project management tools (e.g., Asana, Trello).

- **Vienti ja integraatiot** (Priority: Low)
  - Exports proposals in PDF or DOCX format.
  - (Optional future feature) Direct integration with the EU Funding & Tenders portal.

## 5. User experience
### 5.1. Entry points & first-time user flow
- User registers via email or OAuth (Google, LinkedIn).
- Introduction to the multi-agent system and Agno framework’s role in orchestrating the process.
- Guided setup of a new project with a clear visual progress indicator.

### 5.2. Core experience
- **Ideointi Ideanikkarin kanssa:** User inputs key project parameters and receives 3–5 funding idea suggestions.
- **Arviointi Arvioijalla:** Selected ideas are scored and refined via a back-and-forth conversation.
- **Hakemuksen laatiminen Hakijalla:** The refined idea is transformed into a structured funding proposal, section by section.
- **Lopullinen arviointi (Rahoittaja):** The complete proposal is reviewed, scored, and feedback is provided before final export.

### 5.3. Advanced features & edge cases
- **Tiimityö:** Collaborative editing and multi-user project management.
- **Reaaliaikainen kriteeripäivitys:** Automatic updates when programme criteria change.
- **Automatisoitu laadunarviointi:** AI-driven quality checks (e.g., content length, compliance) integrated into each phase.
- **A/B testaus:** Different AI model configurations for continuous improvement of idea generation.

### 5.4. UI/UX highlights
- Visual progress tracker indicating each agent phase.
- Intuitive chat interface for natural language interactions with agents.
- Responsive design for both desktop and mobile.
- Clear notifications and inline guidance for each step.

## 6. Narrative
Matti, pk-yrityksen perustaja, haluaa saada rahoitusta digitalisaatiohankkeelleen. Hän rekisteröityy järjestelmään, jonka Ideanikkari-agentti generoi nopeasti useita rahoituskelpoisia ideoita. Matti valitsee parhaan idean, jota Arvioija-agentti jalostaa antamalla konkreettisia parannusehdotuksia. Hakija-agentti kääntää tämän idean täydeksi hakemukseksi, jonka lopuksi Rahoittaja-agentti arvioi varmistaakseen, että hakemus täyttää kaikki Digital Europe Program -vaatimukset. Näin Matti saa käyttöönsä kilpailukykyisen hakemuksen ja parantaa mahdollisuuksiaan saada rahoitusta.

## 7. Success metrics
### 7.1. User-centric metrics
- Käyttäjien tyytyväisyys (NPS) tekoälyagenttien suhteen.
- Konversioaste ideasta valmiiksi hakemukseksi.
- Käyttäjien säästetty aika hakemusten valmistuksessa.
- Uusien ja toistuvien käyttäjien määrä.

### 7.2. Business metrics
- Uusien käyttäjätilien kasvu ja aktivoitujen projektien määrä.
- Maksullisten tilaajien osuus ja keskimääräinen tuotto.
- Asiakashankintakustannukset ja asiakassuhteen elinkaariarvo.
- Laajentuminen muihin rahoitusohjelmiin.

### 7.3. Technical metrics
- Agenttien vasteajat ja viiveet Agno-arkkitehtuurissa.
- Palvelun uptime ja suorituskyky.
- AI-mallien osumatarkkuus ja laadunarviointipisteet.
- Tietoturva-auditointien tulokset ja GDPR-yhteensopivuus.

## 8. Technical considerations
### 8.1. Integration points
- Agno-frameworkin modulaarinen viestinvälitys eri agenttien välillä.
- Rajapinnat EU Funding & Tenders -portaaliin ja muihin ulkoisiin järjestelmiin.
- Pilvipohjainen infrastruktuuri (esim. AWS, Azure) suurten kielimallien ajamiseen.
- Integraatiot projektinhallinta- ja dokumentointityökaluihin.

### 8.2. Data storage & privacy
- Kaikki projektidata tallennetaan salattuna ja GDPR-vaatimusten mukaisesti.
- Käyttäjien data säilyy yksityisenä, ja vain valtuutetut käyttäjät voivat tarkastella sitä.
- Mahdollisuus anonymisoida data tekoälymallien optimointia varten.
- Lokitus ja säännölliset tietoturva-auditoinnit.

### 8.3. Scalability & performance
- Hyödynnetään Agno-frameworkin modulaarista rakennetta, jossa jokainen agentti toimii itsenäisenä palveluna.
- Käytetään mikropalveluarkkitehtuuria, joka mahdollistaa automaattisen skaalautumisen.
- Nopeat vasteajat ja korkea käytettävyys optimoidaan pilvi-infrastruktuurilla.
- Mahdollisuus vaihtaa tekoälymallien tarjoajia joustavasti.

### 8.4. Potential challenges
- Korkeat kustannukset suurten kielimallien käytössä.
- Sisällön hallusinaatioiden riski ja tarpeellinen käyttäjävalidointi.
- Rahoitusohjelman kriteerien jatkuvat muutokset ja niiden vaikutus automaatioon.
- Integraatio- ja tietoturvariskit, erityisesti ulkoisten rajapintojen osalta.

## 9. Milestones & sequencing
### 9.1. Project estimate
- Keskikokoinen: 4–6 kuukautta MVP:n kehittämiseen ja pilotointiin.

### 9.2. Team size & composition
- Tiimi: 6–8 henkilöä
  - 1 tuoteomistaja/strategi
  - 2–3 tekoäly- ja backend-kehittäjää
  - 1–2 frontend-kehittäjää
  - 1 UX/UI-suunnittelija
  - 1 QA/tesaaja

### 9.3. Suggested phases
- **Vaihe 1:** Ideanikkari- ja Arvioija-agenttien kehitys (4 viikkoa)
  - Integrointi markkinoiden parhaiden kielimallien kanssa Agno-frameworkin avulla.
  - Peruskäyttöliittymä ja rekisteröinti.
- **Vaihe 2:** Hakija-agentin kehitys (4 viikkoa)
  - Hakemuspohjan automaattinen generointi ja tarkistustoiminnot.
  - Iteratiivinen muokkaus ja sisältövalidaatio.
- **Vaihe 3:** Rahoittaja-agentin kehitys (3 viikkoa)
  - Lopullinen arviointi ja pisteytys Digital Europe -kriteereillä.
  - Yksityiskohtainen arviointiraportti ja palaute.
- **Vaihe 4:** Pilotointi, testaus ja optimointi (3–4 viikkoa)
  - Sisäiset tietoturva- ja suorituskykytestit.
  - Käyttäjäpalautteen keruu ja jatkokehityssuunnitelma.
  - Laajennusmahdollisuuksien suunnittelu muihin rahoitusohjelmiin.

## 10. User stories
### 10.1. Kirjautuminen ja käyttäjätilin hallinta
- **ID:** US-001  
- **Description:** Käyttäjänä haluan luoda tilin (tai konsulttitilin) ja kirjautua sisään, jotta voin käyttää agenttiverkostoa ja tallentaa projektejani.  
- **Acceptance criteria:**
  - Rekisteröityminen sähköpostilla tai OAuth (Google, LinkedIn)
  - Salasanan nollaus ja tietoturvallinen tallennus
  - Profiilin päivitys (yritys, rooli)
  - Roolipohjainen kirjautuminen

### 10.2. Uuden projektin luominen
- **ID:** US-002  
- **Description:** Käyttäjänä haluan luoda uuden rahoitushakemusprojektin Digital Europe -ohjelmaa varten, jotta voin aloittaa ideointiprosessin.  
- **Acceptance criteria:**
  - Projektille nimi, kuvaus ja toimiala
  - Valinta "Digital Europe Programme" -hakutyypiksi
  - Projektin luonti tietokantaan ja ohjaus Ideanikkari-agentin käyttöön

### 10.3. Ideointi Ideanikkari-agentin kanssa
- **ID:** US-003  
- **Description:** Käyttäjänä haluan saada tekoälyn generoimia ideaehdotuksia, jotta löydän rahoituskelpoisen projektinaiheen.  
- **Acceptance criteria:**
  - Chat-näkymä, jossa käyttäjä syöttää toimialan, kohderyhmän ja teknologiatiedot
  - Vähintään 3 ideaa per kierros
  - Ideoiden tallennus projektin "Idea"-osioon
  - Mahdollisuus käynnistää uusi ideakierros

### 10.4. Ideoiden arviointi Arvioija-agentin kanssa
- **ID:** US-004  
- **Description:** Käyttäjänä haluan saada pisteytyksen ja parannusehdotuksia ideoilleni, jotta voin kehittää niistä kilpailukykyisempiä hakemuksia.  
- **Acceptance criteria:**
  - Ideoiden syöttö Arvioija-agentille
  - Pisteytys kolmella osa-alueella (relevanssi, toteutuskelpoisuus, vaikuttavuus)
  - Konkrettien kehitysehdotusten antaminen
  - Mahdollisuus hyväksyä tai hylätä ehdotukset

### 10.5. Hakemuksen laatiminen Hakija-agentin kanssa
- **ID:** US-005  
- **Description:** Käyttäjänä haluan, että Hakija-agentti muuntaa parannetun idean täydeksi hakemukseksi, jotta saan laadukkaan ja jäsennellyn hakemuksen.  
- **Acceptance criteria:**
  - Hakija-agentti generoi hakemusrungon (osiot: taustat, tavoitteet, työpaketit, budjetti, vaikutus)
  - Sisällön validointi (merkkimäärä, rakenne)
  - Mahdollisuus muokkaukseen jokaisessa osassa

### 10.6. Hakemuksen arviointi Rahoittaja-agentin kanssa
- **ID:** US-006  
- **Description:** Käyttäjänä haluan simuloida rahoittajan tarkastusta ennen hakemuksen lähettämistä, jotta voin varmistaa, että hakemus täyttää Digital Europe -vaatimukset.  
- **Acceptance criteria:**
  - Lopullinen pisteytys ja arviointiraportti
  - Selkeä palaute, joka sisältää pisteet ja kehitysehdotukset
  - Mahdollisuus tehdä parannuksia ja lähettää uudelleen arvioitavaksi

### 10.7. Projektien hallinta ja tiimityö
- **ID:** US-007  
- **Description:** Käyttäjänä haluan työskennellä yhdessä tiimini jäsenten kanssa, jotta voimme yhdessä parantaa hakemuksen laatua.  
- **Acceptance criteria:**
  - Projektikutsut sähköpostilla tai käyttäjänimellä
  - Roolien määrittely (katselija, muokkaaja, konsultti, hallinnoija)
  - Versiohistoria ja notifikaatiot

### 10.8. Vienti ja integraatiot
- **ID:** US-008  
- **Description:** Käyttäjänä haluan viedä valmiin hakemukseni PDF- tai DOCX-muotoon, jotta voin lähettää sen rahoitusportaaliin tai jakaa sen sidosryhmille.  
- **Acceptance criteria:**
  - Hakemuksen vienti PDF- tai DOCX-formaattiin
  - Automatisoitu sisältöjen yhteenveto ja metatiedot
  - Mahdollisuus tallentaa tiedosto pilvipalveluun (Google Drive, Dropbox)

### 10.9. Hakemuksen päivittäminen kriteerien muuttuessa
- **ID:** US-009  
- **Description:** Käyttäjänä haluan, että järjestelmä ilmoittaa, kun Digital Europe -kriteereissä tapahtuu muutoksia, jotta hakemukseni pysyy ajan tasalla.  
- **Acceptance criteria:**
  - Järjestelmä seuraa kriteeripäivityksiä reaaliaikaisesti
  - Ilmoitukset käyttäjälle muutoksista
  - Agentti ehdottaa muutoksia hakemuksen sisältöön

### 10.10. Tietoturva ja yksityisyys
- **ID:** US-010  
- **Description:** Käyttäjänä haluan, että kaikki syötetyt tiedot pysyvät turvassa ja GDPR-yhteensopivina.  
- **Acceptance criteria:**
  - Kaikki tiedonsiirto salataan (HTTPS/TLS)
  - Projektit ovat oletuksena yksityisiä
  - Käyttäjä voi poistaa projektin tiedot pysyvästi
  - Lokitus ja säännölliset tietoturva-auditoinnit

### 10.11. Esimerkkikäyttäjäpolku: Aloitteleva hakija
- **ID:** US-011  
- **Description:** Aloittelevana hakijana haluan askel askeleelta -opastuksen, joka kulkee idean kehittämisestä rahoittajan arviointiin, jotta prosessi on selkeä.  
- **Acceptance criteria:**
  - Selkeä opastus jokaisessa vaiheessa (ideointi, arviointi, hakemuksen laatiminen, lopullinen tarkastus)
  - Edistymispalkki ja tooltipit avustamassa käyttäjää
  - Mahdollisuus antaa palautetta jokaisesta vaiheesta