import pandas as pd
import os
import time
from datetime import datetime, timedelta
from get_companies_from_API import all_companies
from RoleScraperAPI import get_roles_for_company  

last_30_days = (datetime.today() - timedelta(days=30)).date()
last_30_days_str = str(last_30_days)

#Creates a list variable that will be used for storing data before turning it into a df and then into excel
daglig_leder_rows = []
other_roles_rows = []


#goes through each item and links datavalues to a variable
for company in all_companies[:50]:
    orgnr = company["orgnr"]
    seleskapsnavn = company["navn"]
    stiftet = company["stiftelsesdato"]
    registreringsdatoEnhetsregisteret = company["registreringsdatoEnhetsregisteret"]
    kommune = company["kommune"]

    #using the function for getting roles and storing them in roles variable.
    roles = get_roles_for_company(orgnr)

    #Checks roles and then iterates through each group data stored in roles.
    if roles:
        for gruppe in roles:
            gruppebeskrivelse = gruppe.get("type", {}).get("beskrivelse")
            
            #checks if role is "daglig leder" if not store it for a seperate file. at this moment i only want companies with "daglig leder"
            if gruppebeskrivelse == "Daglig leder":

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
                    daglig_leder_rows.append({
                        "selskapsnavn": seleskapsnavn,
                        "organisasjonsnummer": orgnr,
                        "registreringsdatoEnhetsregisteret" : registreringsdatoEnhetsregisteret,
                        "kommune" : kommune,
                        "rolle": rollebeskrivelse,
                        "navn": fullt_navn,
                        "fødselsdato": fodselsdato
                    })
            """#collecting companies were daglig leder role does not exist. not going to use at this moment.
            else:
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
                    other_roles_rows.append({
                        "Selskapsnavn": seleskapsnavn,
                        "Organisasjonsnummer": orgnr,
                        "Stiftelsesdato": stiftet,
                        "Rollegruppe": gruppebeskrivelse,
                        "Rolle": rollebeskrivelse,
                        "Navn": fullt_navn,
                        "Fødselsdato": fodselsdato
                    })"""
                

    #time.sleep(0.1)

base_filename = f"selskaper_ {last_30_days_str}"
counter = 1
filename = f"{base_filename}.xlsx"

while os.path.exists(filename):
    filename = f"{base_filename}_{counter}.xlsx"
    counter += 1

#turns rows into a dataframe and uses the dataframe to write all retrieved data into an excel file. split into to different files.
daglig_leder_df = pd.DataFrame(daglig_leder_rows)
daglig_leder_df.to_excel(filename, index=False, engine="xlsxwriter")
print("daglig leder fil lagret som:", filename)

"""other_roles_df = pd.DataFrame(other_roles_rows)
other_roles_df.to_excel("selskaper_og_andre_roller.xlsx", index=False)
print("andre roller fil lagret")"""