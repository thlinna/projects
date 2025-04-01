# Digital Europe Program -rahoitushakemuksia ideoiva agenttiverkosto - Dokumentaatio

Tämä hakemisto sisältää Digital Europe Program -rahoitushakemusten ideointiin, arviointiin ja kehittämiseen tarkoitetun tekoälyagenttipohjaisen työkalun dokumentaation.

## Sisällysluettelo

1. [Arkkitehtuuri](./architecture.md)
2. [API-dokumentaatio](./api.md)
3. [Käyttöohjeet](./user-guide.md)
4. [Kehittäjäohjeet](./developer-guide.md)
5. [Tietokantarakenne](./database.md)

## Projektin yleiskatsaus

Tämä projekti kehittää tekoälyagenttipohjaisen työkalun, joka auttaa käyttäjiä ideoimaan, arvioimaan ja kehittämään kilpailukykyisiä rahoitushakemuksia Euroopan unionin Digital Europe Program -rahoitusohjelmaan.

Työkalun ytimessä on neljä erikoistunutta tekoälyagenttia:
- **Ideanikkari**: Generoi innovatiivisia ideoita rahoituksen hakemiseen.
- **Arvioija**: Analysoi ideoiden vahvuuksia, heikkouksia ja antaa parannusehdotuksia.
- **Hakija**: Muotoilee ideat rakenteellisiksi hakemuksiksi rahoitusohjelman kriteerien mukaisesti.
- **Rahoittaja**: Arvioi hakemuksen laadun ja kilpailukyvyn rahoitusohjelman näkökulmasta.

## Teknologiapino

- **Backend**: Node.js, Express, MongoDB, mongoose
- **Frontend**: React, Material-UI
- **Tekoäly**: OpenAI API, LangChain
- **Infra**: Docker, Docker Compose

## Agenttiverkoston toimintaperiaate

1. **Ideointivaihe**: Käyttäjä määrittelee kiinnostuksen kohteensa ja toimialansa, joiden perusteella Ideanikkari-agentti generoi innovatiivisia rahoitusideaehdotuksia.

2. **Arviointivaihe**: Arvioija-agentti analysoi ideat ja käy vuoropuhelua käyttäjän kanssa tunnistaakseen ideoiden vahvuudet, heikkoudet ja parannusmahdollisuudet.

3. **Hakemusvaihe**: Hakija-agentti muotoilee jalostetut ideat rakenteellisiksi hakemuksiksi, jotka vastaavat Digital Europe Program -rahoitusohjelman vaatimuksia.

4. **Arviointivaihe**: Rahoittaja-agentti arvioi hakemuksen kilpailukyvyn ja antaa parannusehdotuksia ennen varsinaista hakemuksen jättämistä.

## Dokumentaation ylläpito

Tämä dokumentaatio päivitetään jokaisen merkittävän versiopäivityksen yhteydessä. Dokumentaatio on saatavilla myös järjestelmän sisäisessä käyttöliittymässä. 