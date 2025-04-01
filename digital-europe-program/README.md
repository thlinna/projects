# Digital Europe Program -rahoitushakemuksia ideoiva agenttiverkosto

Tämä projekti on tekoälyagenttipohjainen työkalu, joka auttaa käyttäjiä ideoimaan, arvioimaan ja kehittämään kilpailukykyisiä rahoitushakemuksia Euroopan unionin Digital Europe Program -rahoitusohjelmaan.

## Yleiskatsaus

Työkalun ytimessä on neljä erikoistunutta tekoälyagenttia:
- **Ideanikkari**: Generoi innovatiivisia ideoita rahoituksen hakemiseen.
- **Arvioija**: Analysoi ideoiden vahvuuksia, heikkouksia ja antaa parannusehdotuksia.
- **Hakija**: Muotoilee ideat rakenteellisiksi hakemuksiksi rahoitusohjelman kriteerien mukaisesti.
- **Rahoittaja**: Arvioi hakemuksen laadun ja kilpailukyvyn rahoitusohjelman näkökulmasta.

## Projektin rakenne

```
/
├── backend/           # Node.js/Express API
├── frontend/          # React/Next.js käyttöliittymä
├── docs/              # Dokumentaatio
├── docker/            # Docker konfiguraatiot
├── .env               # Ympäristömuuttujat (ei versionhallinnassa)
├── docker-compose.yml # Docker Compose määrittelyt
└── README.md          # Projektin dokumentaatio
```

## Kehitysympäristö

### Vaatimukset
- Node.js (v16 tai uudempi)
- Docker ja Docker Compose
- MongoDB

### Asennus ja käynnistys

1. Kloonaa repositorio:
   ```
   git clone [repository-url]
   cd digital-europe-program
   ```

2. Asenna riippuvuudet:
   ```
   # Backend
   cd backend
   npm install

   # Frontend
   cd ../frontend
   npm install
   ```

3. Käynnistä kehitysympäristö:
   ```
   # Juurihakemistossa
   docker-compose up -d
   ```

4. Avaa sovellus selaimessa:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:5000
   - API dokumentaatio: http://localhost:5000/api-docs

## Lisenssi

Tämä projekti on lisensoitu [MIT-lisenssin](LICENSE) alla.

# Project Guidelines and Rules

This directory contains comprehensive rules, guidelines, and best practices to ensure consistent, high-quality, secure, and maintainable code and workflows across the project.

---

## 📌 Contents Overview

| File                               | Description                                                |
|------------------------------------|------------------------------------------------------------|
| [`agent-behavior-rules.mdc`](agent-behavior-rules.mdc) | Defines behavior guidelines for AI agents, structured task handling, incremental development, and clear commit conventions. |
| [`coding-standards.mdc`](coding-standards.mdc)         | Specifies coding styles, naming conventions, database coding standards, recommended frameworks, and project coding best practices. |
| [`core.mdc`](core.mdc)                                 | Outlines core architectural principles, project strategy, technology selection criteria, quality assurance, and continuous improvement practices. |
| [`database-best-practices.mdc`](database-best-practices.mdc) | Provides detailed guidelines on database schema design, naming conventions, query optimization, migrations, and PostgreSQL-specific recommendations. |
| [`general-development-guidelines.mdc`](general-development-guidelines.mdc) | Covers general development conventions, maintainability tips, and structured methods for issue diagnosis and troubleshooting. |
| [`libraries-to-avoid.mdc`](libraries-to-avoid.mdc)     | Lists frameworks or libraries explicitly discouraged due to quality, maintainability, or security concerns. |
| [`security-best-practices.mdc`](security-best-practices.mdc) | Defines comprehensive security guidelines including secure coding practices, sensitive data management, authentication, and database security standards. |
| [`supabase-best-practices.mdc`](supabase-best-practices.mdc) | Provides best practices specific to Supabase services, including authentication, Row-Level Security, storage management, and security for realtime features. |
| [`testing-strategies.mdc`](testing-strategies.mdc)     | Describes clear testing strategies, requirements for automated testing, integration and database testing, security, and load testing best practices. |

---

## 📚 How to use these rules:

- Familiarize yourself with these guidelines thoroughly before contributing.
- Regularly consult relevant files when implementing new features or debugging.
- Suggest changes or improvements through PRs or team discussions to ensure guidelines remain accurate and valuable.

---

**Keep these files up-to-date** to reflect current practices, ensuring long-term project maintainability, quality, and security.
