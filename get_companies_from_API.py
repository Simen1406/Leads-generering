import requests
from datetime import datetime
import time

all_companies = []
page = 0

#starts the fetching of data from specified url
#while True:
for page in range(2):
    # API endpoint for enhetsregisteret
    url = "https://data.brreg.no/enhetsregisteret/api/enheter"

    params = {
        "size": 100,
        "page": page
    }

    # Start fetching data
    response = requests.get(url, params=params)
    print(f"Page: {page} status:", response.status_code)

    #if statement that breaks code if response status is something else than 200
    if response.status_code != 200:
        print("Stopping due to errer", response.status_code)
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


        if orgform == "AS" and stiftelsesdato:
            try:
                dato = datetime.strptime(stiftelsesdato, "%Y-%m-%d")
                if dato.year == 2025:
                    company = {
                        "navn": enhet.get("navn"),
                        "orgnr": enhet.get("organisasjonsnummer"),
                        "stiftelsesdato": stiftelsesdato
                    }
                    #adds the company dict containing desired info into all companies list.
                    all_companies.append(company)
            except ValueError:
                pass
    # going to next page before repeating previous steps again.
    page += 1
    time.sleep(0.2)

#prints companies and desired data about the company. temporary test.
print(f"\nFant totalt {len(all_companies)} selskaper startet i 2025:\n")
for c in all_companies[:10]:  # limit print
    print(f"{c['navn']} ({c['orgnr']}) – Stiftet: {c['stiftelsesdato']}")
print(type(all_companies))
print(all_companies[0])