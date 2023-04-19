import sys
import os
import csv
current_dir = os.path.dirname(os.path.abspath(__file__))
lib_dir = os.path.join(current_dir, '../lib')
sys.path.append(lib_dir)
import requests
from bs4 import BeautifulSoup
from detainee import Detainee

URL = "https://sheriff.washingtoncountyar.gov/res/DAlphaRoster.aspx"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

last_updated = soup.find(id="LblLastUpdated").text
table_container = soup.find(id="Results")

def collect_detainees(table):
    rows = table.find_all('tr')
    detainees = []
    for i in range(len(rows)):
        if i == 0: 
            continue
        row_data = rows[i].find_all('td')
        detainee_data = []
        for j in range(len(row_data)):
            detainee_data.append(row_data[j].text.strip())

        #                   Name              | Age             | Race            | Sex             | Prior Bookings  | Intake Date
        detainee = Detainee(detainee_data[0], detainee_data[1], detainee_data[2], detainee_data[3], detainee_data[4], detainee_data[5])
        detainees.append(detainee)
    return detainees

def send_to_csv(detainees):
    with open('../output/detainees.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        
        writer.writerow(['name', 'age', 'race', 'sex', 'prior_bookings', 'intake_date'])
        
        for detainee in detainees:
            writer.writerow([detainee.name, detainee.age, detainee.race, detainee.sex, detainee.prior_bookings, detainee.intake_date])


table = table_container.find('table')

detainees = collect_detainees(table)

send_to_csv(detainees)