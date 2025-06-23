from get_companies_from_API import all_companies
import requests
import time


#used the all_companies list and returns orgnr for each item in the list
def retrieve_orgnr():
    return [company['orgnr'] for company in all_companies]
#saves the orgnrs in a new list
org_lst = retrieve_orgnr()

# function for getting the roles in a company based on orgnr. 
def get_roles_for_company(orgnr):
    url = f"https://data.brreg.no/enhetsregisteret/api/enheter/{orgnr}/roller"
    response = requests.get(url)

    #ensures that http response was successful before continuing 
    if response.status_code == 200:
        data = response.json()
        return data.get("rollegrupper", [])
    else:
        print(f"feil ved henting av roller for org: {orgnr}: {response.status_code}")
        return None

#uses above function to get the roles then the loop iterates through each companies roles and retrieves data like, name, role and description
"""for orgnr in org_lst[:100]:
    print(f"\nRoller for {orgnr}:")
    roles = get_roles_for_company(orgnr)

    if roles:
        for gruppe in roles:
            gruppebeskrivelse = gruppe.get("type", {}.get("beskrivelse"))
            #print(f"gruppebeskrivelse: {gruppebeskrivelse}")
            if gruppebeskrivelse["beskrivelse"] == "Daglig leder":
                for rolle in gruppe.get("roller", []):
                    navn = rolle.get("person", {}).get("navn")
                    fodselsdato = rolle.get("person", {}).get("fodselsdato")
                    rollebeskrivelse = rolle.get("type", {}).get("beskrivelse")
                    
                    print(f" - {rollebeskrivelse}: {navn} (født {fodselsdato})")
            else:
                print(f"Ingen daglig leder rolle funnet for {orgnr}")
    time.sleep(1.5)"""