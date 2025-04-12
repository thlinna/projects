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
```

## Osallistuminen (Contributing)
[TODO: Lisää ohjeet siitä, miten muut voivat osallistua projektiin, esim. bugiraportit, ominaisuuspyynnöt, koodikontribuutiot.]

## Lisenssi
[TODO: Määritä projektin lisenssi, esim. MIT, Apache 2.0.]

---