import pandas as pd
import time
from get_companies_from_API import all_companies
from RoleScraperAPI import get_roles_for_company  

rows = []

for company in all_companies:
    orgnr = company["orgnr"]
    seleskapsnavn = company["navn"]
    stiftet = company["stiftelsesdato"]

    roles = get_roles_for_company(orgnr)

    if roles:
        for gruppe in roles:
            gruppebeskrivelse = gruppe.get("type", {}).get("beskrivelse")

            for rolle in gruppe.get("roller", []):
                person = rolle.get("person", {})
                navn_dict = person.get("navn", {})

                fullt_navn = " ".join([
                    navn_dict.get("fornavn", ""),
                    navn_dict.get("mellomnavn", ""),
                    navn_dict.get("etternavn", "")
                ]).strip()

                fodselsdato = person.get("fodselsdato")
                rollebeskrivelse = rolle.get("type", {}).get("beskrivelse")

                rows.append({
                    "Selskapsnavn": seleskapsnavn,
                    "Organisasjonsnummer": orgnr,
                    "Stiftelsesdato": stiftet,
                    "Rollegruppe": gruppebeskrivelse,
                    "Rolle": rollebeskrivelse,
                    "Navn": fullt_navn,
                    "Fødselsdato": fodselsdato
                })

    time.sleep(0.5)

df = pd.DataFrame(rows)
df.to_excel("selskaper_og_roller.xlsx", index=False)
print("fil lagret")