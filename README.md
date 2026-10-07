# BPE – stiskanje sintetičnih bančnih transakcij

## O projektu

Projekt je nastal kot nadgradnja domače naloge pri predmetu **Teorija informacijskih sistemov**.

Pri projektu sem algoritem **BPE (Byte Pair Encoding)** uporabila za brezizgubno stiskanje sintetičnih podatkov o bančnih transakcijah. Podatki so namenoma sintetični in ne vsebujejo pravih bančnih podatkov.

## Motivacija

Projekt sem razvila iz zanimanja za uporabo informatike v bančništvu. Banke obdelujejo in hranijo velike količine transakcijskih podatkov, zato je učinkovito shranjevanje pomembno tako z vidika prostora kot tudi obdelave podatkov. Z BPE sem želela raziskati, kako lahko podatke brez izgube informacij stisnemo in zmanjšamo količino prostora, ki ga zavzamejo.

Pri tem sem preverila tudi, kako na učinkovitost stiskanja vpliva ponavljanje vzorcev v transakcijskih podatkih.

## Podatki

Vsaka transakcija je zapisana v obliki:

```text
datum,opis,znesek
```

Primer:

```text
2026-01-04,MERCATOR,-33.40
2026-01-08,PLACILO_PLACE,+1650.20
```

Uporabljeni sta dve podatkovni zbirki:

* `nakljucne_transakcije.txt` – vsebuje raznolike in naključno generirane transakcije,
* `ponavljajoce_transakcije.txt` – vsebuje več ponavljajočih se vzorcev transakcij.

## BPE

**BPE (Byte Pair Encoding)** je brezizgubni postopek stiskanja podatkov. Pri kodiranju išče najpogosteje ponavljajoče se pare simbolov in jih nadomešča z novimi indeksi v slovarju. Postopek se ponavlja, dokler v podatkih ni več dovolj pogosto ponavljajočih se parov ali dokler ni dosežena omejitev slovarja.

Pri dekodiranju se pari ponovno razširijo v prvotne simbole, zato lahko rekonstruiramo originalne podatke brez izgube informacij.

V implementaciji je slovar omejen na **4096 vnosov**, zato lahko indekse predstavimo z **12 biti**, saj velja:

```text
2^12 = 4096
```

## Zagon programa

Program se zažene z ukazom:

```bash
python naloga1.py
```

Program prebere izbrano vhodno datoteko s transakcijami, izvede BPE kodiranje, shrani kodirane podatke v datoteko JSON, izračuna kompresijsko razmerje in preveri pravilnost dekodiranja.

Vhodno datoteko lahko določimo v funkciji `main`.

## Kompresijsko razmerje

Kompresijsko razmerje računam po formuli:

$$
R = \frac{|vhod| \cdot 8}{|izhod| \cdot 12}
$$

Pri tem:

* `|vhod|` predstavlja število simbolov pred stiskanjem,
* `|izhod|` predstavlja število simbolov po stiskanju,
* originalni ASCII znak je predstavljen z 8 biti,
* kodirani BPE indeks je predstavljen z 12 biti.

Pri testiranju sem dobila:

| Podatki                  | Originalna dolžina | Stisnjena dolžina | Kompresijsko razmerje |
| ------------------------ | -----------------: | ----------------: | --------------------: |
| Naključne transakcije    |             27.327 |             3.985 |                 4,57× |
| Ponavljajoče transakcije |             26.761 |             1.665 |                10,72× |

Rezultati pokažejo vpliv ponavljajočih se vzorcev na učinkovitost BPE. Pri podatkih z več ponavljanja je doseženo večje kompresijsko razmerje.

## Preverjanje dekodiranja

Po kodiranju podatke tudi dekodiram in preverim, ali so enaki originalnim podatkom:

```python
assert dekodirano == vhod
```

S tem preverim, da je stiskanje brezizgubno in da se lahko originalni podatki popolnoma rekonstruirajo.

## Struktura projekta

```text
BPE-transakcije/
├── naloga1.py
├── nakljucne_transakcije.txt
├── ponavljajoce_transakcije.txt
├── stisnjene_nakjucne_transakcije.json
├── stisnjene_ponavljajoce_transakcije.json
└── README.md
```

## Uporabljene tehnologije

* Python 3
* BPE (Byte Pair Encoding)
* JSON
* sintetični podatki o bančnih transakcijah

