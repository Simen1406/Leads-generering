from get_companies_from_API import all_companies
import requests
import time



def retrieve_orgnr():
    return [company['orgnr'] for company in all_companies]

org_lst = retrieve_orgnr()

def get_roles_for_company(orgnr):
    url = f"https://data.brreg.no/enhetsregisteret/api/enheter/{orgnr}/roller"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data.get("rollegrupper", [])
    else:
        print(f"feil ved henting av roller for org: {orgnr}: {response.status_code}")
        return None
    
for orgnr in org_lst[:5]:
    print(f"\nRoller for {orgnr}:")
    roles = get_roles_for_company(orgnr)

    if roles:
        for gruppe in roles:
            gruppebeskrivelse = gruppe.get("typeBeskrivelse")
            for rolle in gruppe.get("roller", []):
                navn = rolle.get("person", {}).get("navn")
                fodselsdato = rolle.get("person", {}).get("fodselsdato")
                rollebeskrivelse = rolle.get("type", {}).get("beskrivelse")
                
                print(f" - {rollebeskrivelse}: {navn} (født {fodselsdato})")
    time.sleep(1.5)