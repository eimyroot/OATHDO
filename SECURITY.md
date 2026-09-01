# Bezpečnostní politika

## Podporovaný rozsah

Bezpečnostní opravy směřují do aktuální výchozí větve. Dokud je OATHDO před vydáním, viditelnost repozitáře ani zelené CI samy o sobě nedokládají připravenost pro produkci.

## Hlášení zranitelnosti

Nezveřejňuj zranitelnosti, přihlašovací údaje, osobní data, neveřejné URL ani detaily exploitu ve veřejném issue nebo pull requestu. Použij GitHub private vulnerability reporting, je-li zapnutý. Jinak založ pouze stručnou veřejnou žádost o soukromý kontakt bez citlivých detailů.

Uveď dotčenou revizi, komponentu, předpoklady útoku, minimální reprodukci, dopad, očekávané bezpečné chování a případný návrh opravy.

## Bezpečnostní minimum

- nikdy necommituj tajné údaje ani produkční data;
- privilegovaná rozhodnutí a autorizaci vynucuj na serveru;
- používej nejmenší oprávnění a deny-by-default;
- validuj nedůvěryhodné vstupy a omezuj spotřebu zdrojů;
- zachovej auditní důkazy bez zapisování tajných údajů;
- chybějící nebo neověřitelné důkazy nesmí znamenat úspěch;
- uniklé přihlašovací údaje vždy zneplatni nebo otoč.

V předprodukční fázi není garantována reakční ani opravná SLA.
