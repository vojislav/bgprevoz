import urllib.request
from bs4 import BeautifulSoup
import os
import sys
import re
from datetime import datetime
import bisect

class Time:
	def __init__(self, hour, minute):
		self.hour = hour
		self.minute = minute

	def __str__(self):
		return f'{self.hour}:{self.minute}'
	
	def __repr__(self):
		return self.__str__()
	
	def __eq__(self, other):
		return self.hour == other.hour and self.minute == other.minute

	def __neq__(self, other):
		return self.hour != other.hour or self.minute != other.minute
	
	def __lt__(self, other):
		return self.hour < other.hour or (self.hour == other.hour and self.minute < other.minute)

	def __gt__(self, other):
		return self.hour > other.hour or (self.hour == other.hour and self.minute > other.minute)
	
class Route:
	def __init__(self, start, departure_times):
		self.start = start
		self.departure_times = departure_times

if len(sys.argv) != 2:
	sys.exit("Not a number")

linija = sys.argv[1]
try:
	linija = int(linija)
except ValueError:
	sys.exit("Not a number")

url = f'https://www.bgprevoz.rs/linije/red-voznje/linija/{linija}/prikaz'

if not os.path.exists(f"{linija}.html"):
	urllib.request.urlretrieve(url, f"{linija}.html")

with open(f"{linija}.html") as f:
	soup = BeautifulSoup(f, "lxml")


current_date = datetime.now()

day_number = current_date.weekday()
column = 0

if day_number < 5:
	column = 1
elif day_number == 5:
	column = 2
else:
	column = 3

current_time = Time(str(current_date.hour), str(current_date.minute))
next_departure_hour, next_depature_min = 0, 0

routes = {}

starting_stations = soup.find('h2').text.split(' - ')

index = 0
for table in soup.find_all('table'):
	for table_body in table.find_all('tbody'):
		departure_times = []
		for row in table_body.find_all('tr')[:-1]:
			cols = row.find_all('td')
			hour = cols[0].text
			col_text = cols[column].text
			col_text = re.sub("\s+", " ", col_text).strip()
			minutes = col_text.split(' ')
			for minute in minutes:
				departure_times.append(Time(str(hour), str(minute)))
		routes[index] = Route(starting_stations[index], departure_times)
		index += 1

route_a_next_depart = bisect.bisect_left(routes[0].departure_times, current_time)
print(routes[0].start, routes[0].departure_times[route_a_next_depart])

route_b_next_depart = bisect.bisect_left(routes[1].departure_times, current_time)
print(routes[1].start, routes[1].departure_times[route_b_next_depart])