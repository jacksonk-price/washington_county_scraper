import requests
from bs4 import BeautifulSoup
from lib.detainee import Detainee

URL = "https://sheriff.washingtoncountyar.gov/res/DAlphaRoster.aspx"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

last_updated = soup.find(id="LblLastUpdated").text
table_container = soup.find(id="Results")
table = table_container.find('table')
# headers for the table
# Name Last, First | Age | Race | Sex | Prior Bookings | Intake Date

print(last_updated)