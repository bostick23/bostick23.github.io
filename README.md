# Claudio Bosticco — sito personale

Sito multilingue italiano/inglese, generato con **Hugo 0.167.0 Extended**.
PaperMod è un submodule fissato al commit `154d006e0182dfc7da38008323976b02e6bfab4a`.

## Sviluppo e verifica

```sh
git submodule update --init --recursive
hugo version
hugo server
```

Prima di pubblicare, eseguire la stessa build di produzione usata dalla CI:

```sh
hugo --environment production --minify --printPathWarnings --printI18nWarnings --panicOnWarning
python scripts/check_site.py public
```

Il controllo richiede Python 3 senza pacchetti aggiuntivi. Verifica XML, feed RSS,
indici di ricerca, metadati SEO e multilingue, regole di indicizzazione,
sitemap, robots.txt e l'esclusione delle bozze note. Per
confrontare URL e sintesi RSS con una build precedente:

```sh
python scripts/check_site.py public --compare /percorso/build-precedente
```

Il confronto verifica anche canonical e hreflang. Quando si modificano
intenzionalmente le descrizioni editoriali, aggiungere `--allow-summary-changes`:
le descrizioni sono usate anche nei feed RSS. Per verificare una build creata con
`hugo --environment development`, usare `--environment development` anche nello
script di controllo.

## Metadati e indicizzazione

`languages.<lingua>.params.seoTitle` imposta il titolo HTML completo della
homepage; `params.seoTitle` nel front matter consente un titolo HTML specifico
per una pagina. Il nome del sito e le intestazioni visibili restano indipendenti.
Le homepage usano la descrizione per lingua; articoli e sezioni hanno una
`description` esplicita nel front matter.

Per escludere una pagina dai motori di ricerca mantenendola accessibile:

```yaml
robotsNoIndex: true
sitemap:
  disable: true
```

In produzione queste pagine emettono `noindex, follow`; le altre emettono
`index, follow`. In sviluppo tutte le pagine emettono `noindex, nofollow`.
Privacy, ricerca e archivi tag/categorie vuoti sono esclusi dall'indicizzazione
e dalle sitemap. Quando gli archivi avranno contenuti utili, rimuovere entrambi
i parametri dai rispettivi `_index.md` in entrambe le lingue.
`enableRobotsTXT` abilita il template PaperMod, con scansione consentita in
produzione e riferimento all'indice delle sitemap multilingue.

## Tema e manutenzione

Gli override `layouts/baseof.html`, `layouts/rss.xml` e i partial head, header,
translation_list e Open Graph seguono PaperMod al commit indicato. Usano le API
Hugo `Language.Direction`, `Language.Label` e `Language.Locale`. Il cambio lingua
nell'header apre la traduzione della pagina corrente, quando esiste, altrimenti
la homepage nella lingua scelta. Quando si aggiorna il tema, confrontare questi
override con upstream e verificare i template progetti e il CSS personalizzato.

RSS e indice JSON escludono le pagine senza permalink: le schede progetto con
`build.render: never` rimangono visibili nelle griglie, senza produrre risultati
di ricerca o voci RSS con link vuoti.

Le pagine equivalenti con nomi o sezioni diversi hanno la stessa `translationKey`.
Mantenerla identica in entrambe le lingue senza cambiare gli URL esistenti.

Il workflow GitHub Actions verifica le pull request verso `master` senza
pubblicarle. Push a `master` e avvio manuale eseguono anche il deploy su GitHub
Pages. La build fallisce sui warning. Non servono Node.js o Dart Sass.

Prima di un aggiornamento di Hugo controllare homepage, articoli, progetti,
ricerca, WalletManager e contatti su mobile e desktop, in tema chiaro e scuro.
Per il modulo contatti simulare risposte di successo, errore e connessione
interrotta: i test non devono inviare messaggi reali.
