import requests
from datetime import datetime, timedelta
import time

all_companies = []
page = 0

last_30_days = (datetime.today() - timedelta(days=30)).date()
str_last_30_days = str(last_30_days)

    # API endpoint for enhetsregisteret
url = "https://data.brreg.no/enhetsregisteret/api/enheter"

params = {
    "page" : 0,
    "size" : 100,
    "organisasjonsform" : "AS",
    "fraRegistreringsdatoEnhetsregisteret" : str_last_30_days
}

# Start fetching data
while True:
    response = requests.get(url, params=params)
    print(f"Page: {page} status:", response.status_code)

    #if statement that breaks code if response status is something else than 200
    if response.status_code != 200:
        print("Stopping due to error", response.status_code)
        break

    #Creates data variable which contains fetched data
    data = response.json()
    enheter = data.get("_embedded", {}).get("enheter", [])

    print(f"Antall eneheter hentet: {len(enheter)}\n")

    # breaks loop when there is not anymore data to retrieve
    if not enheter:
        print("No more data to fetch, stopping")
        break
    
    #for loop that iterates through different data and uses the if statement to check for companies that are stock companies (AS)
    for enhet in enheter:
        orgform = enhet.get("organisasjonsform", {}).get("kode")
        stiftelsesdato = enhet.get("stiftelsesdato")
        registreringsdatoEnhetsregisteret = enhet.get("registreringsdatoEnhetsregisteret")


        if orgform == "AS" and stiftelsesdato:
            try:
                dato = datetime.strptime(stiftelsesdato, "%Y-%m-%d")
                if dato.year == 2025:
                    company = {
                        "navn": enhet.get("navn"),
                        "orgnr": enhet.get("organisasjonsnummer"),
                        "stiftelsesdato": stiftelsesdato,
                        "registreringsdatoEnhetsregisteret" : registreringsdatoEnhetsregisteret
                    }
                    #adds the company dict containing desired info into all companies list.
                    all_companies.append(company)
            except ValueError:
                pass
    
    next_link = data.get("_links", {}).get("next", {}).get("href")
    if not next_link:
        print("Last page reached, stopping")
        break

    # going to next page before repeating previous steps again.
    page += 1
    params["page"] = page
    time.sleep(0.2)

#prints companies and desired data about the company. temporary test.
print(f"\nFant totalt {len(all_companies)} selskaper startet i 2025:\n")
"""for c in all_companies[:10]:  # limit print
    print(f"{c['navn']} ({c['orgnr']}) – Stiftet: {c['stiftelsesdato']}")
print(type(all_companies))
print(all_companies[0])"""