"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie

author: Roman Brixí
email: roman.brixi@seznam.cz
"""

import csv
import sys
from typing import List, Dict, Tuple
import requests
from bs4 import BeautifulSoup

# Skript pro stažení a zpracování volebních výsledků z webu volby.cz
# Vstupní parametry:
# 1. URL územního celku
# 2. Název CSV souboru pro uložení výsledků
# Příklad spuštění:
# python main.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=1&xnumnuts=1100" "vysledky_praha.csv"
# TEST: prohození argumentů
# python main.py  "vysledky_praha.csv" "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=1&xnumnuts=1100"

def get_soup(url: str) -> BeautifulSoup:
    """
    Funkce načte stránku z URL a vrátí BeautifulSoup objekt pro webscraping HTML.

    :param url: URL stránky, kterou chceme stáhnout.
    :return: BeautifulSoup objekt pro analýzu HTML.
    """
    response = requests.get(url, timeout=10)
    if response.status_code != 200:
        raise requests.exceptions.HTTPError(f"Chyba při načítání stránky: {url} (kód {response.status_code})")
    return BeautifulSoup(response.text, "html.parser")


def get_municipality_data(main_soup: BeautifulSoup, base_url: str) -> List[Tuple[str, str, str]]:
    """
    Funkce extrahuje kódy a názvy obcí + plný odkaz na detailní stránky hlasování každé obce
    a vrací je jako seznam.

    :param main_soup: BeautifulSoup objekt hlavní stránky.
    :param base_url: Základní URL, které bude připojeno k relativním odkazům.
    :return: Seznam tuple obsahující (kód obce, název obce, URL detailu obce).
    """
    # proměnná pro uložení dat z hlavní stránky
    main_page = []
    # proměnná pro řádkování výpisu zpracovaných obcí
    counter = 0
    # Pomocný flag, zda byl nalezen alespoň jeden "Kraj:" nebo "Okres:"
    region_found = False

    # Najdi a vytiskni všechny h3, které začínají "Kraj:" nebo "Okres:"
    # Jen pro grafické zobrazení ačítaného kraje a okresu
    for h3 in main_soup.find_all("h3"):
        main_title = h3.get_text(strip=True)
        if main_title.startswith("Kraj:") or main_title.startswith("Okres:"):
            print(main_title)
            region_found = True

    # kontrola zda byl nalezen nějaký kraj/okres, pravděpodobně stránka není platná
    if not region_found:
        print("❌ Nebyl nalezen žádný kraj nebo okres. Pravděpodobně jde o neplatnou URL.")
        return []

    for row in main_soup.find_all("tr"):
        # Najdi všechny řádky s číslem obce a názvem obce
        td_code = row.find("td", class_="cislo")
        td_name = row.find("td", class_="overflow_name")
        # Pokud existují obě buňky, extrahuj data
        if td_code and td_name:
            # získání odkaza na detailní hlasování obce
            link_tag = td_code.find("a")
            if link_tag and link_tag['href']:
                # web využívá jen relativní cesty pro odkazy
                # proto je nutné připojit základní URL
                # k relativnímu odkazu
                full_url = base_url + link_tag['href']
                # extrakce kódu a názvu obce
                # a jejich vyčištění od HTML tagů
                code = td_code.get_text(strip=True)
                location = td_name.get_text(strip=True)
                # výpis průběhu načátní obcí
                print(location + " | ", end="")
                counter += 1
                # po výpisu 10 obcích se zalomí řádek
                if counter % 10 == 0:
                    print()
                # přidání dat do seznamu, kerý bude vrácen
                main_page.append((code, location, full_url))

    # pokud není 10 obcí, tak se zalomí řádek
    if counter % 10 != 0:
        print()

    # kontrola na prázdný seznam
    if not main_page:
        print("❌ Nebyly nalezeny žádné obce. Pravděpodobně jde o chybnou nebo prázdnou stránku.")
        return []

    return main_page


def get_municipal_vote(code: str, location: str, url: str) -> Tuple[List[str], Dict[str, str]]:
    """
    Funkce načte detailní stránku hlasování obce, extrahuje volební údaje
    a hlasy pro jednotlivé strany.

    :param code: Kód obce.
    :param location: Název obce.
    :param url: URL detailní stránky hlasování obce.
    :return: Tuple obsahující seznam volebních údajů a slovník s hlasy pro strany.
    """
    soup = get_soup(url)

    # Základní volební údaje
    td_registered = soup.find("td", headers="sa2")
    td_envelopes = soup.find("td", headers="sa3")
    td_valid = soup.find("td", headers="sa6")
    # Získání textu z buněk a odstranění HTML tagů
    # a nežádoucích znaků (např. &nbsp; které se po načtení změní na '\xa0')
    # pokud není nalezeno, tak se nastaví na "N/A"
    registered = td_registered.get_text(strip=True).replace('\xa0', '')if td_registered else ""
    envelopes = td_envelopes.get_text(strip=True).replace('\xa0', '') if td_envelopes else ""
    valid = td_valid.get_text(strip=True).replace('\xa0', '') if td_valid else ""

    # Hlasy pro jednotlivé strany, budou uloženy do slovníku
    # s názvem strany jako klíčem a počtem hlasů jako hodnotou
    party_votes = {}
    for row in soup.find_all("tr"):
        td_party = row.find("td", class_="overflow_name")
        td_votes = row.find("td", headers=lambda h: h and "sa2" in h and "sb3" in h)
        if td_party and td_votes:
            party = td_party.get_text(strip=True)
            # počty hlasů se musí zase vyčistit od HTML tagů
            # a nežádoucích znaků (např. &nbsp; které se po načtení změní na '\xa0')
            votes = td_votes.get_text(strip=True).replace('\xa0', '') if td_votes else ""
            # přidání do slovníku -> volební strana : počet hlasů
            party_votes[party] = votes

    return [code, location, registered, envelopes, valid], party_votes


def main() -> None:
    """
    Hlavní funkce skriptu, která načítá a zpracovává data
    podle zadané URL a ukládá je do CSV souboru.
    """
    if len(sys.argv) != 3:
        print("❌ Chyba při spuštění programu. Nebyly zadány správně spouštěcí parametry.")
        print("⚠️  python main.py <URL_územního_celku> <název_souboru.csv>")
        sys.exit(1)

    start_url = sys.argv[1]
    output_csv = sys.argv[2]

    # Detekce možného prohození argumentů
    if (output_csv.startswith("http://") or output_csv.startswith("https://")) and start_url.lower().endswith(".csv"):
        print("⚠️  Zdá se, že jste zadali argumenty ve špatném pořadí.")
        print(f"    ➜  Zadaná URL: '{start_url}'")
        print(f"    ➜  Název souboru: '{output_csv}'")
        answer = input("🔄 Chcete argumenty prohodit? (stiskněte Enter pro ANO, cokoliv jiného pro NE): ")
        if answer.strip() == "":
            start_url, output_csv = output_csv, start_url
            print("✅ Argumenty byly prohozeny.")
        else:
            print("❌ Program byl ukončen. Zkuste spustit program znovu s opravenými argumenty.")
            sys.exit(1)

    # proměnná na doplnění relativní URL o základní část URL
    base_url = "https://www.volby.cz/pls/ps2017nss/"

    try:
        main_soup = get_soup(start_url)
        print("🔴 Nahrávám data ze zadané URL:", start_url)

        # kontrola zda je stránka dostupná
        selected_municipalities = get_municipality_data(main_soup, base_url)
        if not selected_municipalities:
            print(f"❌ Program '{sys.argv[0]}' byl ukončen s chybou.")
            sys.exit(1)

        all_data = []
        all_parties = []

        # pomocí získáných dat z hlavní stránky, získáme i data ze stránek obce
        for code, location, detail_url in selected_municipalities:
            basic_data, party_votes = get_municipal_vote(code, location, detail_url)
            all_data.append((basic_data, party_votes))

            # přidání názvu strany do seznamu volebních stran, pokud ještě není
            for party in party_votes:
                if party not in all_parties:
                    all_parties.append(party)

        # prvních 5 nadpisů pro CSV soubor se musí přidat manuálně
        # kód, název obce, registrovaní voliči, vydané obálky, platné hlasy
        # a pak se již automaticky přidají názvy stran
        header = ["code", "location", "registered", "envelopes", "valid"] + all_parties

        with open(output_csv, mode="w", newline='', encoding="utf-8-sig") as file:
            writer = csv.writer(file, delimiter=';')
            # zapišeme hlavičku do CSV souboru
            writer.writerow(header)
            # cyklem se zapíšou samostatné řádky s výsledky jednotlivých obcí
            for basic_data, party_votes in all_data:
                # základní data obce + hlasy pro jednotlivé strany
                # (pokud strana s hlasy v proměnné all_parties existuje,
                # tak se zapíše počet hlasů, jinak se zapíše prázdný řetězec)
                row = basic_data + [party_votes.get(party, "") for party in all_parties]
                writer.writerow(row)

        print(f"💾 Data byla uložena do souboru '{output_csv}'.")
        print(f"✅ Hotovo! Program '{sys.argv[0]}' byl úspěšně ukončen.")
    # Ošetření výjimek
    except (requests.exceptions.MissingSchema, requests.exceptions.InvalidURL):
        print("❌ Zadaná URL není platná. Zkontrolujte prosím zadanou adresu.")
    except requests.exceptions.HTTPError as e:
        print(f"❌ Zadaná URL není dostupná nebo je chybná: {e}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Chyba při stahování dat: {e}")
    except csv.Error as e:
        print(f"❌ Chyba při zápisu do CSV: {e}")
    except KeyboardInterrupt:
        print("❌ Program byl přerušen uživatelem.")

if __name__ == "__main__":
    main()
