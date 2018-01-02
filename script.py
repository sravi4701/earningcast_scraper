from __future__ import print_function
from pprint import pprint
import sys
import time
from bs4 import BeautifulSoup
import requests
import re
import threading
# ajax call url
# https://earningscast.com//calls?ajax=true&ajax_render=latest&page=1


head_url = "https://earningscast.com"
store = {}

'''
Store structure
store {
	company_name:[
		{
			event_name: string,
			event_date: date,
			Act: string,
			Est: string,
			audio_download_link: string 
		}
	]
}
'''


def fetch_audio_url(item_url):
	r = requests.get(item_url)
	soup2 = BeautifulSoup(r.content, "lxml")
	d_elem = soup2.find("a", id=re.compile("^event-[0-9]*-download"))
	return d_elem["href"]


def log(message):
	print(message, file=sys.stderr)

def parse_source(soup):
	'''
	Extract Items detail and store it to the json
	'''
	tab_latest_call = soup.find(attrs={"class": "tab latest-calls"})
	table_content = tab_latest_call.div
	all_items = table_content.find_all(attrs={"class":"item"})
	for item in all_items:
		h3 = item.h3
		state = item.find("div", attrs={"class":"state"})
		date_elem = item.find("span", attrs={"class":"sub"})
		date = str(date_elem.string)
		date = date.strip() 
		name = str(h3.a.string)
		item_url = str(h3.a["href"])
		company_name = item_url.split("/")[1]
		item_url = head_url + item_url
		name = name.strip()
		act = ""
		est = ""
		if state is not None:
			for elem in state.contents:
				if "Act" in elem:
					act = elem
				if "Est" in elem:
					est = elem
			act = act.strip()
			est = est.strip()
		log("fetching audio url ..........")
		audio_url = head_url + fetch_audio_url(item_url)
		if not store.get(company_name):
			store[company_name] = []
		obj = {
			"event_name":name,
			"event_date": date,
			"Act":act,
			"Est":est,
			"audio_download_link":audio_url
			}
		store[company_name].append(obj)
		# log("company_name:" + company_name)
		# log("Name:" +  str(name))
		# log("date:" +  str(date))
		# log("Act:" + str(act))
		# log("Est:" +  str(est))
		# log("audio_url:" + str(audio_url))
		log("--"*10)

def main():
	for i in range(1, 5):
		log("page" + str(i) + " ........")
		url = head_url + "/calls?ajax=true&ajax_render=latest&page=" + str(i)
		response = requests.get(url)
		log("Making soup......")
		soup = BeautifulSoup(response.content, "lxml")
		t = threading.Thread(target=parse_source, args=(soup,))
		t.start()
	while threading.active_count() > 1:
		continue
	print(store)

if __name__ == '__main__':
	main()