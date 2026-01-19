# Manifest: Morphological Learning as Principled Argument (2026 Edition)

## Visjon

Dette prosjektet er en revitalisering og modernisering av rammeverket presentert i *Johnsen (2006)*. Målet er å skape en "lettvekts språkmodul" som ikke bare gjenkjenner mønstre, men som evaluerer morfologisk struktur gjennom **logisk bevisførsel** basert på distribusjonelle fakta.

## Kjernekonsepter (Arven fra 2006)

* **Morfologi som argument**: En morfologisk analyse er en påstand som krever bevis. Vi evaluerer evidens som støtter at en streng er en meningsbærende enhet.


* 
**Evidens for mening**: Vi følger prinsippet om at hvis en stamme () også opptrer som et selvstendig ord i ordlisten (), er det et sterkt bevis for at  bærer mening.


* 
**Seleksjonsrestriksjoner ()**: Vi koder forholdet mellom stammer og affikser for å avgjøre hvilke par som kan kombineres til velformede ord.


* 
**Paradigmegruppering**: Vi søker å identifisere komplette paradigmer ved å kartlegge distribusjonen , altså det totale settet av suffikser en stamme kan ta.



## Moderniseringen (2026-oppgradering)

For å "cut the beef" i et moderne landskap, har vi oppgradert arkitekturen:

1. **Fra Heuristikk til Bayesiansk Inferens (Pyro)**:
* Vi erstatter manuelle straffefunksjoner med en probabilistisk modell i **Pyro**.


* Vi bruker **Beta-distribusjoner** () for å modellere usikkerhet.




2. **Kontekstualisering via Trigrammer**:
* Der 2006-modellen var begrenset til ordet isolert, bruker vi nå **trigrammer med ordet i midten** som "vitner".


* Dette løser klassiske tvetydigheter (som *fisker*) og hindrer logiske feilskjær.


3. **Aktiv Paradigmestøtte**:
* Vi bruker SQLite-indekser for å gruppere stammer som deler de samme suffiksene.
* Dette lar oss identifisere bøyingsmønstre (paradigmer) på tvers av hele ordlisten, noe som styrker beviset for hver enkelt analyse.


4. **Skalerbarhet (SQLite & uv)**:
* Effektiv håndtering av 200 000 ord og ca. 1,6 millioner splitt-hypoteser.


* Prosjektet styres med `uv` for maksimal reproduserbarhet.



## Implementasjonsmål

* 
**Prinsippfasthet**: Modellen skal kunne forklare *hvorfor* en splitt er valgt ved å peke på distribusjonelle bevis i korpuset.


* **Paradigmatisk innsikt**: Modellen skal kunne samle alle former av en stamme (f.eks. *fisk, fisken, fisker, fiskene*) og behandle dem som et sammenhengende argument.
* **Gjennomsiktighet**: Ved å bruke interaktiv evaluering skal vi kunne intervjue modellen om dens morfologiske beslutninger.

---

*Basert på "Morphological learning as principled argument", Lars G. Johnsen (2006).*

---


Lykke til med rugdetrekket i koden og de 1,6 millionene med rader! Vi snakkes når du er klar for neste fase.
