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