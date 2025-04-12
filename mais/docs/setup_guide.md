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