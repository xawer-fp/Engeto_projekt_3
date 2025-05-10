# Projekt : Elections Scraper

## 📊 Zadání projektu
Napsat scraper parlamentních volebních výsledků z roku 2017 v jazyce PYTHON :snake:, který vytáhne data přímo z webu.
Skript vybere jakýkoliv územní celek z této webové stránky: https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ.
Např. **X** u Benešov odkazuje sem: https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2101.
Z tohoto odkazu je potřeba vyscrapovat výsledky hlasování pro všechny obce.
<br><br>
Výsledky hlasování lze stahovat **pomocí odkazů ve sloupci číslo**, např. `529303`, nebo **pomocí odkazů ve sloupci Výběr okrsku**,
tedy sloupec se `symbolem X`. Nezáleží na vybrané variantě, jen musí prezentovat správná data.


## 📖 Důležité podmínky projektu
- skript bude spouštěn pomocí **2 argumentů**
  - `první` bude obsahovat odkaz na vybraný územní celek, který se bude scrapovat
  - `druhý` bude určovat název souboru CSV, do kterého se zpracovaný výstup uloží
  - zároveň bude implementována kontrola vložení správného počtu a pořadí argumentů
  - nalezené chyby budou uživateli oznámeny
- skript bude využívat **virtuální prostředí** vytvořené speciálně pro tento projekt
  - do virtuálního prostředí se nahrají knihovny třetích stran, potřebné pro tento projekt
  - `automaticky` se vygeneruje soubor **requirements.txt** se soupisem všech knihoven a jejich verzí
- v Github repozitáři s vypracovaným projektem bude soubor **README.md** s informacemi o projektu, spuštění apod.
  - mimo README souboru a souboru **main.py** s hotovým programem , bude na Githubu i
    - seznam relevantnch knihoven **requirements.txt**
    - **soubor CSV** s vygenerovaným souborem    - 
- vygenerovaný **CSV soubor** bude mít
  - kód obce, název obce, voliči v seznamu, vydané obálky, platné hlasy
  - \+ kandidující strany (co sloupec, to počet hlasů pro stranu pro všechny strany).
  - ukázka výstupního .csv souboru je níže
<img src="https://learn.engeto.com/api/doc-asset/gI8nxeZvRzOnWn7ua0Pumg/48_output_csv.png">


# Vypracovaný projekt

## 📦 Instalace / přenositelnost
V repozitáři je uložen soubor **requirements.txt**, který obsahuje automaticky vygenerovaný seznam knihoven třetích stran pro tento projekt. Před přesunem či spuštěním v jiném prostředí lze potřebné knihovny jednoduše nainstalovat.

Generování souboru **requirements.txt** (např. zadáním do terminálu VSC). Soubor requirements.txt se automaticky objeví v projektu s výpisem všech knihoven (včetně verzí).

```bash
pip freeze > requirements.txt
```
nebo
```bash
python -m pip freeze > requirements.txt
```

Vygenerovaný soubor **requirements.txt**

```bash
beautifulsoup4==4.13.4
certifi==2025.4.26
charset-normalizer==3.4.2
idna==3.10
requests==2.32.3
soupsieve==2.7
typing_extensions==4.13.2
urllib3==2.4.0
```

Instalace použitých knihoven v novém prostředí

```bash
pip install -r requirements.txt
```



## 🔧 Spuštění programu

Skript se spouští z příkazové řádky:

```bash
python main.py <URL_požadované_obce> <výstupní_soubor.csv>
```

#### 🛠️ Příklad:

```bash
python main.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=1&xnumnuts=1100" "vysledky_praha.csv"
```

Tímto příkazem stáhnete výsledky voleb pro Prahu a uložíte je do souboru `vysledky_praha.csv`.

## 📁 Výstup CSV

CSV soubor obsahuje:

* kód obce
* název obce
* počet registrovaných voličů v seznamu
* počet vydaných obálek
* počet platných hlasů
* a výsledky všech politických stran kandidujících v územním celku

Ukázka řádku s nadpisy:
```
code;location;registered;envelopes;valid;Občanská demokratická strana;Řád národa - Vlastenecká unie;CESTA ODPOVĚDNÉ SPOLEČNOSTI;Česká str.sociálně demokrat.;Volte Pr.Blok www.cibulka.net;Radostné Česko;STAROSTOVÉ A NEZÁVISLÍ;Komunistická str.Čech a Moravy;Strana zelených;ROZUMNÍ-stop migraci,diktát.EU;Společ.proti výst.v Prok.údolí;Strana svobodných občanů;Blok proti islam.-Obran.domova;Občanská demokratická aliance;Česká pirátská strana;OBČANÉ 2011-SPRAVEDL. PRO LIDI;Unie H.A.V.E.L.;Referendum o Evropské unii;TOP 09;ANO 2011;Dobrá volba 2016;SPR-Republ.str.Čsl. M.Sládka;Křesť.demokr.unie-Čs.str.lid.;Česká strana národně sociální;REALISTÉ;SPORTOVCI;Dělnic.str.sociální spravedl.;Svob.a př.dem.-T.Okamura (SPD);Strana Práv Občanů
```
Ukázka řádku:
```
500054;Praha 1;21556;14167;14036;2770;9;13;657;12;1;774;392;514;41;6;241;14;44;2332;5;0;12;2783;1654;1;7;954;3;133;11;2;617;34
```

## 🧑‍💻 Autor

Roman Brixí
📧 [roman.brixi@seznam.cz](mailto:roman.brixi@seznam.cz)



## ⚠️ Upozornění

Tento projekt slouží jako cvičení v rámci **ENGETO Online Python Akademie** a není určen pro produkční použití. Stránky [volby.cz](https://www.volby.cz) nenabízejí API a proto při používání skriptu berte ohledy na přetěžování serveru.
