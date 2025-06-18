import requests
from datetime import datetime
import time

all_companies = []
page = 0

#while True:
for page in range(2):
    # API endpoint for enhetsregisteret
    url = "https://data.brreg.no/enhetsregisteret/api/enheter"

    params = {
        "size": 100,
        "page": page
    }

    # Fetch the data
    response = requests.get(url, params=params)
    print(f"Page: {page} status:", response.status_code)

    if response.status_code != 200:
        print("Stopping due to errer", response.status_code)
        break

    data = response.json()
    enheter = data.get("_embedded", {}).get("enheter", [])

    print(f"Antall eneheter hentet: {len(enheter)}\n")

    if not enheter:
        print("No more data to fetch, stopping")
        break

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
                    all_companies.append(company)
            except ValueError:
                pass
    page += 1
    time.sleep(0.2)
            
print(f"\nFant totalt {len(all_companies)} selskaper startet i 2025:\n")
for c in all_companies[:10]:  # limit print
    print(f"{c['navn']} ({c['orgnr']}) – Stiftet: {c['stiftelsesdato']}")
print(type(all_companies))
print(all_companies[0])