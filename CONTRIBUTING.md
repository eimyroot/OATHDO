# Jak přispívat do OATHDO

Změny musí být malé, přezkoumatelné, otestované a vratné.

## Postup

1. U významné změny založ nebo uveď související issue.
2. Vytvoř úzce zaměřenou větev z výchozí větve repozitáře.
3. Implementuj nejmenší úplnou změnu řešící deklarovaný problém.
4. Doplň testy a dokumentaci.
5. Spusť ověřovací příkazy uvedené v repozitáři.
6. Otevři pull request s riziky, důkazy a rollbackem.

## Standard pull requestu

Pull request musí uvést:

- co a proč se změnilo;
- co zůstalo vědomě mimo rozsah;
- ověřovací příkazy a výsledky;
- bezpečnostní, kompatibilitní, datová a provozní rizika;
- způsob návratu nebo bezpečného vypnutí.

Nikdy necommituj tajné údaje, osobní data, lokální databáze, runtime stav ani neověřené výroky. Zelený check dokládá jen rozsah, který daný check skutečně testoval.
