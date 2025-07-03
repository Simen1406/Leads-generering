# Lead-generering – Norwegian AS Leads Generator

A Python script that collects **recently registered Norwegian AS companies** from BRREG API´s For each company, it fetches:

- Selskapsnavn (Company Name)
- Organisasjonsnummer (Organization number)
- Stiftelsesdato (Founding Date)
- Daglig leder / Styrets leder (CEO / Chairperson)
- Fødselsdato og navn



---

## 🚀 Features

- Scrapes new AS companies
- Extracts company and role data from each profile
- Saves structured results to excel
- Designed for BRREG API´s
- Uses collected data to scrape for a phone number and then adds the number to the correct index in the excel file.


### TechStack
- Python
- Selenium
- Pandas
- webdriver


#### Cloning repo
1. clone the repo with git clone https://github.com/...
   and move to correct folder with cd leads-generering
2. Create a virtual environment and activate it
3. install requirements.txt for dependencies. 
