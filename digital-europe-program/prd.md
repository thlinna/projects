# PRD: Digital Europe Program -rahoitushakemuksia ideoiva ja laativa tekoälyagenttiverkosto

## 1. Product overview
### 1.1 Document title and version
- PRD: Digital Europe Program -rahoitushakemuksia ideoiva ja laativa tekoälyagenttiverkosto
- Versio: 1.1 (parannettu versio, sisältää tarkennuksia ja laajennuksia)

### 1.2 Product summary
Tämä tuote on tekoälyagenttiverkosto, joka auttaa eri käyttäjäryhmiä ideoimaan, arvioimaan ja kehittämään laadukkaita rahoitushakemuksia Euroopan unionin Digital Europe Program -rahoitusohjelmaan. Työkalu hyödyntää useita erikoistuneita tekoälyagentteja, jotka työskentelevät yhteistyössä tuottaakseen innovatiivisia ideoita ja muuntaakseen ne hakemuksiksi huomioiden ohjelman arviointikriteerit (relevanssi, toteutuskelpoisuus ja vaikuttavuus).

Työkalun ytimessä on neljä keskeistä tekoälyagenttia (Ideanikkari, Arvioija, Hakija, Rahoittaja). Lisäksi järjestelmään on suunniteltu mahdollisuus laajentaa agenttiverkostoa tulevaisuudessa muiden EU-rahoitusohjelmien (esim. Horizon Europe) ja kansallisten rahoituslähteiden tukemiseen. Jokaisen agentin toiminta perustuu markkinoilla saatavilla oleviin parhaisiin kielimalleihin tai omiin hienoviritettyihin malleihin, jolloin generoidut sisällöt vastaavat rahoitusohjelmien erityistarpeita.

## 2. Goals
### 2.1 Business goals
- Tehostaa rahoituskelpoisten ideoiden generointia erityisesti Digital Europe Program -rahoitusohjelmaa varten.
- Kasvattaa rahoitushakemusten hyväksymisprosenttia tuottamalla laadukkaita, kriteerit täyttäviä hakemuksia.
- Tarjota skaalautuva, SaaS-tyyppinen tekoälyalusta, joka voi laajentua muille EU-rahoitusalueille (Horizon Europe, ym.).
- Mahdollistaa nopea käyttöönotto myös konsulttitoimistoille, tutkimuslaitoksille ja muille tahoille, jotka tuottavat hakemuksia asiakkailleen.

### 2.2 User goals
- Löytää ja kehittää rahoituskelpoisia projektiaiheita Digital Europe Programin painopisteitä vastaaviksi.
- Saada tekoälyn perusteltua palautetta ja ideoita hakemuksen parantamiseen.
- Valmistella valmiita hakemuspohjia, joita voi muokata ja rikastaa tiimin tai asiakkaiden tarpeiden mukaan.
- Pysyä ajan tasalla rahoitusohjelman päivittyvistä kriteereistä ja täyttää ne tehokkaasti.

### 2.3 Non-goals
- Taata rahoituksen saaminen (työkalu voi parantaa todennäköisyyttä, mutta ei pysty takaamaan lopputulosta).
- Antaa juridisia tai verotuksellisia neuvoja hakuprosessin laillisiin yksityiskohtiin.
- Korvata kokonaan inhimillistä arviointia tai projektin käytännönhallintaa (painotus on hakemusten valmistelussa).
- Tarjota kaikkia EU:n rahoitushakemustyökaluja kattavaa “one-stop-shop” -palvelua heti ensimmäisessä versiossa.

## 3. User personas
### 3.1 Key user types
- **Aloitteleva hakija** (esim. pienyrittäjä tai startup): Tarvitsee ohjausta alusta alkaen.
- **Kokenut hakija** (esim. PK-yritys tai julkinen toimija): Tarvitsee vahvistusta ja oikolukua hakemuksilleen.
- **Rahoituskonsultti**: Hoitaa useiden eri asiakkaiden hakemuksia ja haluaa tehokkaan tavan hallita projekteja.
- **Tutkija/kehittäjä** (esim. tutkimusorganisaatio): Etsii automatisoitua ja strukturoitua tapaa dokumentoida ja perustella hankkeitaan Digital Europe -kriteerien mukaan.
- **Oppilaitoksen kehittäjä**: Vastaa opetus- ja kehityshankkeiden rahoituksesta ja haluaa tehostaa ideointia ja hakemusten laatimista.

### 3.2 Basic persona details
- **Aloitteleva hakija**: Vailla kokemusta EU-rahoitusmaailmasta, tarvitsee kädestä pitäen -opastusta.
- **Kokenut hakija**: On aiemmin hakenut rahoitusta, tuntee prosessin mutta haluaa tehostaa tekemistä.
- **Rahoituskonsultti**: Tekee projekteja asiakkailleen, tarvitsee työkalulta moniprojekti- ja tiimihallintaa.
- **Tutkija**: Toimii tutkimuslaitoksessa, haluaa kaupallistaa idean tai laajentaa tutkimustaan EU-rahoituksella.
- **Oppilaitoksen kehittäjä**: Vastaa laajemmista digihankkeista, tarvitsee varmistusta hankkeen vaikutusten ja konkreettisten tulosten esittelyyn.

### 3.3 Role-based access
- **Peruskäyttäjä**: Kirjautuu sisään, hyödyntää agentteja, luo omia projekteja ja tallentaa hakemuksia.
- **Tiimin jäsen**: Työskentelee yhteistyöprojekteissa, kommentoi ja muokkaa jaettuja hakemuksia.
- **Konsultti/hallinnoija**: Hallinnoi useita asiakasprojekteja, jakaa oikeuksia eri asiakkaiden hakemuksiin, haluaa nähdä edistymisen koontinäkymän.
- **Järjestelmänvalvoja**: Hallinnoi koko järjestelmän teknisiä asetuksia, käyttäjärooleja ja tietoturvaa.

## 4. Functional requirements
- **Ideageneraattori (Ideanikkari)** (Prioriteetti: Korkea)
  - Käyttää tekoälymallia, joka on koulutettu tai hienoviritetty EU-innovaatiokeskusteluilla.
  - Tarjoaa ideointisession, jossa käyttäjältä kysytään toimialasta, tavoitteista ja resurssien laajuudesta.
  - Vertaa ideoita Digital Europe Program -painopistealueisiin ja generoi relevantteja ehdotuksia.

- **Ideoiden arviointi ja jalostaminen (Arvioija)** (Prioriteetti: Korkea)
  - Tekee perustasoisen analyysin ideoista (esim. vahvuudet, heikkoudet, parannusehdot).
  - Sisältää suuntaa-antavan **“virtuaalisen pisteytyksen”** Digital Europe -kriteereihin pohjautuen (relevanssi, toteutus, vaikuttavuus).
  - Tukee iteratiivista keskustelua: käyttäjä voi kysyä tarkennuksia ja perusteluja, tekoäly antaa parannusehdotuksia.

- **Hakemusten valmistelu (Hakija)** (Prioriteetti: Korkea)
  - Jäsentää hakemuksen kaikki osiot (esim. tavoitteet, projektisuunnitelma, budjetti) valmiiksi pohjaksi Digital Europe Program -standardien mukaisesti.
  - Tarjoaa tekoälyn generoimia tekstiehdotuksia kuhunkin hakemuksen osioon käyttäjän syötteiden perusteella.
  - Auttaa pitämään tekstin pituuden ja rakenteen kohdillaan (varoitukset merkkimäärän tai sivurajoitusten ylittyessä).

- **Hakemusten arviointi (Rahoittaja)** (Prioriteetti: Korkea)
  - Mallintaa rahoittajan näkökulmaa: tarjoaa lopullisen arvioinnin hakemuksen vaikuttavuudesta, selkeydestä ja kriteerien täyttämisestä.
  - Antaa “Arviointiraportin”, jossa on pisteytys ja suositukset hakemuksen vahvistamiseksi.
  - Päivittyy säännöllisesti uusia hakukierroksia varten (haun uudet painotukset, budjettikriteerit, painopisteet).

- **Projektien ja hakemusten hallinta** (Prioriteetti: Keskitaso)
  - Tuki useille rinnakkaisille projekteille ja roolipohjaiselle yhteistyölle (kommentointi, versiointi).
  - Aikajanapohjainen näkymä, jossa voi seurata projektin etenemistä (ideointi → arviointi → hakemuksen kirjoitus → loppuarviointi).
  - Mahdollisuus integroida hakemustekstit projektinhallinnan työkaluihin (Asana, Trello).

- **Käyttäjäprofiilin ja konsulttitilin hallinta** (Prioriteetti: Keskitaso)
  - Konsultti/hallinnoija voi luoda, hallinnoida ja seurata useiden eri asiakkaiden projekteja.
  - Käyttöoikeuksien valvonta ja roolien määrittely: kuka saa muokata, kuka vain kommentoida tai katsella.

- **Integraatiot ja vienti** (Prioriteetti: Matala)
  - Mahdollisuus ladata valmiit hakemukset PDF- tai DOCX-muodossa.
  - (Tulevaisuudessa) Integraatio EU Funding & Tenders -portaaliin, jos avointa rajapintaa tarjotaan.
  - Integraatio dokumentinhallintajärjestelmiin (esim. Google Drive, Dropbox).

## 5. User experience
### 5.1. Entry points & first-time user flow
- Käyttäjä rekisteröityy (perus- tai konsulttikäyttäjänä) sähköpostilla tai kolmannen osapuolen OAuth-palvelulla.
- Järjestelmä esittelee lyhyesti agenttien toiminnot (Ideanikkari, Arvioija, Hakija, Rahoittaja) ja rahoitusohjelman tavoitteet.
- Käyttäjä voi aloittaa uuden projektin valitsemalla “Digital Europe Program” -hakemustavan, jolloin järjestelmä avaa vuorovaikutteisen ideointisession Ideanikkarilla.
- Käyttäjälle näytetään, miten projekti etenee vaiheittain: idea → arviointi → hakemuksen laatiminen → lopullinen arviointi.

### 5.2. Core experience
- **Ideointi Ideanikkarin kanssa**: Tekoälymalli kysyy projektiin liittyviä avainsanoja (toimiala, kohderyhmä, teknologiat).  
  - Käyttäjä saa 3–5 rahoituskelpoista ideaehdotusta, jotka vastaavat rahoitusohjelman painopisteitä.  

- **Ideoiden jalostus Arvioijalla**: Valitut ideat siirtyvät Arvioijalle, joka tekee virtuaalisen kriteerianalyysin: relevanssi, toteutuskelpoisuus, vaikuttavuus.  
  - Käyttäjä näkee pisteytyksen ja saa kehitysehdotuksia (esim. “lisää kansainvälistä yhteistyötä”, “selvennä kestävyysnäkökulma”).  

- **Hakemuksen laatiminen Hakijalla**: Käyttäjä laatii hakemusosion kerrallaan. Hakija-agentti generoi pohjatekstin, joka sisältää pakolliset elementit (esim. projektin tavoitteet, aikataulu, budjetti).  
  - Järjestelmä varoittaa, jos teksti ylittää merkkimäärärajoitukset. Käyttäjä voi muokata pohjaa tai pyytää uutta luonnosta.  

- **Hakemuksen lopullinen arviointi (Rahoittajalla)**: Käyttäjä lähettää luonnostellun hakemuksen Rahoittajalle, joka antaa raportin ohjelman kriteerien näkökulmasta.  
  - Käyttäjä saa yhteenvedon (esim. pisteet asteikolla 1–5) jokaisesta kriteeristä ja tarkistuslistan parannuksille.  
  - Kun hakemus on valmis, sen voi ladata PDF- tai DOCX-muodossa, tai tallentaa projektin arkistoon.

### 5.3. Advanced features & edge cases
- **Tiimityöskentely**: Monen käyttäjän samanaikainen muokkaus samaa projektia konsulttitoimistojen tai tutkimuskonsortioiden tarpeisiin.
- **Vertailuanalyysi**: Työkalu voi vertailla hakemusta aiemmin rahoitettuihin hankkeisiin (anonymisoidut mallit) ja ehdottaa tarkennuksia.
- **Hakukriteerien päivitykset**: Agentti tarkkailee EU:n virallisia lähteitä ja päivittää kriteerien painotuksia (esim. uudet teema-alueet).
- **Budjetin tarkistus**: Hakija-agentti laskee suuntaa-antavat rahoitusosuudet ja varoittaa, jos budjetti ei vastaa haun rajoituksia.
- **Turvallinen arkistointi**: Käyttäjä voi poistaa kaiken projektidatan pysyvästi tai siirtää sen salattuun arkistoon GDPR-yhteensopivasti.

### 5.4. UI/UX highlights
- **Käyttäjäpolun visualisointi**: Näytetään selkeä “edistymispalkki” (Idea → Arviointi → Hakemuksen laatiminen → Loppuarvio).  
- **Luonnollisen kielen chat**: Käyttäjä keskustelee suoraan tekoälyagenttien kanssa, saa ohjeita ja voi esittää tarkentavia kysymyksiä.  
- **Responsiivinen suunnittelu**: Taulukko- ja mobiilikäyttö sujuvaa.  
- **Konsulttinäkymä**: Rooli- ja asiakaskohtainen koonti, josta näkee asiakkaiden projektit ja niiden tilanteen.

## 6. Narrative
Laura on vastikään perustetun kyberturvallisuusalan startup-yrityksen toimitusjohtaja, joka haluaa löytää uutta rahoitusta tuotekehitykseen ja Euroopan laajuisille markkinoille laajentumiseen. Hän tietää, että Digital Europe Program voi rahoittaa digitaalisia turvallisuusratkaisuja, mutta ei ole varma, miten hioa hakemus kilpailukykyiseksi. Laura rekisteröityy uuteen tekoälyagenttiverkostoon, saa Ideanikkarilta nopeasti toimialaan sopivia ideaehdotuksia, jalostaa niitä Arvioijalla ja laatii lopulta kattavan hakemuksen Hakija-agentin opastuksella. Hän pyytää lopuksi Rahoittaja-agenttia antamaan pistearvion ja viime hetken parannusehdotukset, minkä jälkeen hän on valmis jättämään hakemuksen.

## 7. Success metrics
### 7.1. User-centric metrics
- Käyttäjien tyytyväisyys (NPS) sekä palautepisteet tekoälyagenttien relevanssista.
- Ideasta valmiiksi hakemukseksi -konversioaste.
- Toistuvien käyttäjien osuus (retention): moniko jatkaa useampaan hakemukseen tai ohjelmaan.
- Käyttäjän ajan säästö verrattuna perinteiseen hakuprosessiin (esim. prosentuaalinen vähennys ajankäytössä).

### 7.2. Business metrics
- Uusien käyttäjätilien määrä (MAU).
- Palvelun maksullisten tilaajien määrä ja keskimääräinen tuotto (ARPU).
- Asiakashankintakustannukset (CAC) ja asiakassuhteen elinkaariarvo (LTV).
- Palvelun laajeneminen muihin rahoitusohjelmiin (esim. määrä, josta laajennus on tuottanut lisätuloa).

### 7.3. Technical metrics
- Agenttien vasteaika (keskimääräinen ja 95. prosenttipiste).
- Palvelun käytettävyysaste / uptime (%).
- Tekoälymallien tuottamien ideoiden “osumatarkkuus” (esim. ihmisten arvioimana).
- Tiedonsiirron ja tallennuksen turvallisuusmittarit (hyväksytyt tietoturva-auditoinnit).

## 8. Technical considerations
### 8.1. Integration points
- Rajapinta EU Funding & Tenders -portaaliin (jos/kun mahdollista).
- Automatisoitu tiedonhaku Digital Europe Program -sivustolta (kriteeripäivitykset, uudet haut).
- Pilviarkkitehtuurin kyvykkyys (esim. AWS, Azure) tukemaan suuria kielimalleja ja useita yhtäaikaisia käyttötilanteita.
- Projektinhallintajärjestelmät (Trello, Asana) ja dokumentinhallinta (Google Drive, Dropbox).

### 8.2. Data storage & privacy
- Kaikki projektidatat tallennetaan salattuna ja GDPR-vaatimusten mukaisesti.
- Käyttäjäkohtaiset projektit säilyvät yksityisinä; vain kutsutut näkevät sen.
- Mahdollisuus anonymisoida dataa tekoälymallien jatkokehitystä varten.
- Lokituksen hallinta, josta käy ilmi projektien katselu ja muokkaus.

### 8.3. Scalability & performance
- Mikropalveluarkkitehtuuri, jossa jokainen agentti toimii omana palvelunaan ja kommunikaatio on reititetty orchestrator-luokan kautta.
- Dynamo-tyyppiset NoSQL-tietokannat tai perinteiset relaatiotietokannat (riippuen rakenteen tarpeista).
- Palvelukomponenttien auto-skaalaus ruuhka-aikoina (hakuajan loppumetreillä).
- Mahdollisuus vaihtaa tai päivittää LLM-mallien tarjoajaa (esim. GPT-4 → GPT-5) kustannusten tai suorituskyvyn mukaan.

### 8.4. Potential challenges
- Kustannukset: suurten kielimallien käyttö on kallista, erityisesti korkealla käyttöasteella.
- Sisällön laatu: mallit saattavat tuottaa hallusinaatioita, joten käyttäjän vahvistus on tärkeää.
- Rahoituskriteerien jatkuva muutos: järjestelmän tulee pysyä ajan tasalla, jotta se ei ohjaa hakijaa vanhentuneilla tiedoilla.
- Tietosuoja: käyttäjät syöttävät liikesalaisuuksia ja luottamuksellista dataa, joka täytyy säilyttää erittäin turvallisesti.

## 9. Milestones & sequencing
### 9.1. Project estimate
- Keskikokoinen: 3–5 kuukautta perusagenttien tuotantovalmiiksi saamiseksi (mukaan lukien pilotointivaihe).

### 9.2. Team size & composition
- Keskikokoinen tiimi: 5–7 henkilöä
  - 1 tuoteomistaja (liiketoiminta & rahoitusasiat)
  - 2–3 tekoäly- ja backend-kehittäjää
  - 1–2 frontend-kehittäjää
  - 1 UX/UI-suunnittelija
  - 1 testaaja/laadunvarmistaja

### 9.3. Suggested phases
- **Vaihe 1**: Ideanikkari- ja Arvioija-agenttien kehitys (4 viikkoa)
  - Ensimmäinen integrointi suurten kielimallien kanssa
  - Yksinkertainen käyttöliittymä ja perusrekisteröinti
  - Perustoiminnot ideageneroinnista ja arvioinnista

- **Vaihe 2**: Hakija-agentin kehitys (4 viikkoa)
  - Hakemuspohjan automaattinen generoiminen
  - Merkkimäärä-/rakennetarkistukset
  - Projektinhallintaominaisuudet (perustason tiimityö)

- **Vaihe 3**: Rahoittaja-agentin kehitys (3 viikkoa)
  - Arviointi- ja pisteytysominaisuus kriteerien perusteella
  - Edistyneet integraatiot (dokumentinhallinta)
  - Julkinen betatestaus

- **Vaihe 4**: Laajennukset, testaus ja optimointi (2–3 viikkoa)
  - Sisäiset tietoturva-auditoinnit
  - Skaalaus- ja suorituskykytestit
  - Tuotantojulkaisu ja jatkokehityssuunnitelma (laajennus muihin rahoitusohjelmiin)

## 10. User stories
### 10.1. Kirjautuminen ja käyttäjätilin hallinta
- **ID**: US-001
- **Description**: Käyttäjänä haluan luoda tilin (tai konsulttitilin) ja kirjautua järjestelmään, jotta voin käyttää agenttiverkostoa ja tallentaa projektejani.
- **Acceptance criteria**:
  - Rekisteröityminen sähköpostilla + salasanalla tai OAuth:lla (Google, LinkedIn)
  - Salasanan nollaus & tietoturvallinen tallennus
  - Profiilinäkymä, jossa voi päivittää perustietojaan (yritys, rooli)
  - Roolipohjainen kirjautuminen: peruskäyttäjä tai konsultti/hallinnoija

### 10.2. Uuden projektin luominen
- **ID**: US-002
- **Description**: Käyttäjänä haluan luoda uuden rahoitushakemusprojektin, jotta voin aloittaa ideointiprosessin Digital Europe Programiin.
- **Acceptance criteria**:
  - Projektille annetaan nimi, lyhyt kuvaus ja toimiala
  - Mahdollisuus valita “Digital Europe Program” hakutyyppinä
  - Projektin ID:n ja perustietojen luonti tietokantaan
  - Käyttäjän ohjaaminen Ideanikkari-agentin kanssa keskusteluun

### 10.3. Ideointi Ideanikkari-agentin kanssa
- **ID**: US-003
- **Description**: Käyttäjänä haluan saada tekoälyn generoimia ideaehdotuksia ja kehittää niitä, jotta voin löytää rahoituskelpoisen projektinaiheen.
- **Acceptance criteria**:
  - Chat-näkymä, jossa käyttäjä antaa toimiala-/teknologiatietoja
  - Vähintään 3 ideaehdotusta kerrallaan
  - Ideoiden tallennus projektin “Idea”-osioon
  - Uusi ideakierros pyynnöstä, jos käyttäjä ei pidä ehdotuksista
  - Huomio Digital Europe Programin ajankohtaiset painopisteet (esim. tekoälyn etiikka, digiturvallisuus)

### 10.4. Ideoiden arviointi Arvioija-agentin kanssa
- **ID**: US-004
- **Description**: Käyttäjänä haluan saada pisteytyksen ja parannusehdotuksia ideoilleni, jotta voin kehittää niistä kilpailukykyisempiä hakemuksia.
- **Acceptance criteria**:
  - Ideoiden syöttäminen Arvioija-agentille
  - Agentti pisteyttää idean kolmella osa-alueella (relevanssi, toteutuskelpoisuus, vaikuttavuus)
  - Agentti antaa vähintään yhden konkreettisen kehitysehdotuksen idean parantamiseksi
  - Käyttäjä voi tallentaa tai hylätä muokatun idean

### 10.5. Hakemuksen laatiminen Hakija-agentin kanssa
- **ID**: US-005
- **Description**: Käyttäjänä haluan ohjatun prosessin, joka tuottaa valmiin hakemuksen rungon, jotta saan hakemuksen rakenteen nopeasti kuntoon.
- **Acceptance criteria**:
  - Hakija-agentti generoi hakemusrungon (otsikot: taustat, tavoitteet, työpaketit, budjetti, vaikutus)
  - Käyttäjä muokkaa tai hyväksyy ehdotetun tekstin jokaiselle osiolle
  - Järjestelmä varoittaa, jos tekstin pituus tai merkkimäärä on ylittymässä
  - Käyttäjä voi siirtyä osioiden välillä ja tallentaa edistymisen

### 10.6. Hakemuksen arviointi Rahoittaja-agentin kanssa
- **ID**: US-006
- **Description**: Käyttäjänä haluan simuloida rahoittajan näkökulmaa ennen hakemuksen lähettämistä, jotta tiedän täyttääkö hakemus kriteerit.
- **Acceptance criteria**:
  - Käyttäjä voi pyytää lopullisen pisteytyksen ja raportin valmiista hakemuksesta
  - Agentti näyttää, missä kohtaa hakemusta on vielä puutteita tai heikkouksia
  - Käyttäjä saa selkeän palautteen (esim. pisteet asteikolla 1–5 ja sanallinen selite)
  - Hakemusta voi muokata ja lähettää uudelleen arvioitavaksi ennen vientiä

### 10.7. Projektien hallinta ja tiimityö
- **ID**: US-007
- **Description**: Käyttäjänä haluan työskennellä yhdessä tiimini jäsenten tai asiakkaiden kanssa samassa projektissa, jotta voimme hyödyntää erilaisia osaamisalueita.
- **Acceptance criteria**:
  - Projektikutsu sähköpostilla tai käyttäjänimellä
  - Roolien (katselija, muokkaaja, konsultti, hallinnoija) määrittäminen
  - Versiohistoria: kenellä oli muokkausoikeus ja mitä muutoksia on tehty
  - Notifikaatiot tiimin jäsenille merkittävistä muutoksista

### 10.8. Vienti ja integraatiot
- **ID**: US-008
- **Description**: Käyttäjänä haluan viedä valmiin hakemukseni PDF- tai DOCX-muotoon, jotta voin lähettää sen rahoitusportaaliin tai jakaa sen sidosryhmille.
- **Acceptance criteria**:
  - Käyttäjä voi ladata hakemuksen PDF- tai DOCX-formaatissa
  - Hakemuksen vientiin sisältyy automaattinen sisältöjen yhteenveto ja metatiedot (projektin nimi, päivämäärä)
  - Mahdollisuus tallentaa hakemus suoraan Google Driveen tai Dropboxiin
  - Tulevaisuudessa (optio) suora siirto EU Funding & Tenders -portaaliin, jos tekninen rajapinta avautuu

### 10.9. Hakemuksen päivittäminen rahoituskriteerien muuttuessa
- **ID**: US-009
- **Description**: Käyttäjänä haluan varmistaa, että hakemukseni täyttää uusimmat Digital Europe -kriteerit, jotta en lähettäisi vanhentunutta hakemusta.
- **Acceptance criteria**:
  - Järjestelmä seuraa EU:n virallisia kanavia kriteeripäivityksistä
  - Käyttäjä saa ilmoituksen, jos hakemusta tulisi päivittää (esim. uudet teema-alueet)
  - Agentti ehdottaa kohtia, joihin päivitykset vaikuttavat (esim. “Lisää tietoa saavutettavuudesta”)
  - Käyttäjä voi soveltaa automaattisia ehdotuksia tai muokata tekstiä käsin

### 10.10. Tietoturva ja yksityisyys
- **ID**: US-010
- **Description**: Käyttäjänä haluan, että ideani ja hakemukseni pysyvät luottamuksellisina ja EU:n tietosuoja-asetusten mukaisina.
- **Acceptance criteria**:
  - Kaikki tiedonsiirto salataan (HTTPS/TLS)
  - Projekti on oletuksena yksityinen; vain kutsutut näkevät sen
  - Käyttäjä voi poistaa kaiken dataan liittyvän projektin pysyvästi
  - Lokitus kaikista muokkauksista ja tietoturva-auditoinnit säännöllisesti

### 10.11. Esimerkkikäyttäjäpolku: Aloitteleva hakija
- **ID**: US-011
- **Description**: Aloittelevana hakijana haluan askel askeleelta -opastuksen, joka kulkee idean kehittämisestä rahoittajan virtuaaliseen arviointiin, jotta prosessin jokainen vaihe on selkeä.
- **Acceptance criteria**:
  - Käyttäjä saa “opastetun polun”, jossa jokainen agentti esitellään vuorollaan
  - Sivun yläreunassa on edistymispalkki (vaihe 1/4, 2/4 jne.)
  - Järjestelmä antaa vihjeitä (tooltipit) päävaiheiden kohdalla (“Nyt siirryt ideoinnista arviointiin”)
  - Käyttäjä voi antaa palautetta jokaisesta vaiheesta (esim. “Tämä oli selvää / Epäselvää”)
  - Hakemusta voi lopuksi tarkastella yhtenä kokonaisuutena tai ladata sen tiedostona