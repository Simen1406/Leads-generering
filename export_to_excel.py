import pandas as pd
import time
from get_companies_from_API import all_companies
from RoleScraperAPI import get_roles_for_company  

#Creates a list variable that will be used for storing data before turning it into a df and then into excel
rows = []

#goes through each item and links datavalues to a variable
for company in all_companies:
    orgnr = company["orgnr"]
    seleskapsnavn = company["navn"]
    stiftet = company["stiftelsesdato"]

    #using the function for getting roles and storing them in roles variable.
    roles = get_roles_for_company(orgnr)

    #Checks roles and then iterates through each group data stored in roles.
    if roles:
        for gruppe in roles:
            gruppebeskrivelse = gruppe.get("type", {}).get("beskrivelse")

            #name is split into first, middle and last name this fixes it and joins them into a single string. 
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

                #adds retrieved data into a dict that will be used to create a structured excel file.
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

#turns rows into a dataframe and uses the dataframe to write all retrieved data into an excel file. 
df = pd.DataFrame(rows)
df.to_excel("selskaper_og_roller.xlsx", index=False)
print("fil lagret")