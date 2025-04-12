# Product Requirements Document: Multi-Agent Ideation System (MAIS)

**Versio:** 0.1  
**Päiväys:** 2025-04-12  
**Omistaja:** [TODO: Product Owner / Projektipäällikkö]

---

**Sisällysluettelo**
- [Product Requirements Document: Multi-Agent Ideation System (MAIS)](#product-requirements-document-multi-agent-ideation-system-mais)
  - [1. Johdanto ja Tavoitteet (MIKSI?)](#1-johdanto-ja-tavoitteet-miksi)
  - [2. Kohdeyleisö ja Käyttäjät (KENELLE?)](#2-kohdeyleisö-ja-käyttäjät-kenelle)
  - [3. Käyttäjätarinat / Käyttötapaukset (MITÄ KÄYTTÄJÄ TEKEE?)](#3-käyttäjätarinat--käyttötapaukset-mitä-käyttäjä-tekee)
  - [4. Ratkaisu ja Tekninen Toteutus (MITEN?)](#4-ratkaisu-ja-tekninen-toteutus-miten)
  - [5. Ei-funktionaaliset Vaatimukset](#5-ei-funktionaaliset-vaatimukset)
  - [6. Datanhallinta](#6-datanhallinta)
  - [7. Testausstrategia](#7-testausstrategia)
  - [8. Rajaukset (Out of Scope)](#8-rajaukset-out-of-scope)
  - [9. Julkaisukriteerit](#9-julkaisukriteerit)
  - [10. Avoimet Kysymykset](#10-avoimet-kysymykset)

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