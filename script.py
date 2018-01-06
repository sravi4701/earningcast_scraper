from __future__ import print_function
from pprint import pprint
import sys
import time
from bs4 import BeautifulSoup
import requests
import re
import threading
import os


# ajax call url
# https://earningscast.com//calls?ajax=true&ajax_render=latest&page=1

# global variabls

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


def save_to_file(*data):
	audio_url = data[-1]
	company_name = data[0]
	dir_path = os.path.dirname(os.path.realpath(__file__))
	os.chdir(dir_path)
	unique_hash = audio_url.split("/")[-2]
	dir_name = company_name + "/event-" + unique_hash 
	os.makedirs(dir_name)
	os.chdir(dir_name)
	with open("data-" + unique_hash + ".txt", "w") as f:
		f.write("name:" + data[1])
		f.write("\ndate:" + data[2])
		f.write("\n" + data[3] + "\n" + data[4])
		f.close()
	session = requests.Session()
	payload = {'user[login]': 'useremail', 'user[password]': 'userpass'}
	r = session.post('https://earningscast.com/users/sign_in', data=payload)
	log("logged in....")
	with open("data-" + unique_hash + ".m4a", "wb") as fhand:
		response = session.get(audio_url, stream=True)
		for block in response.iter_content(1024):
			fhand.write(block)
		fhand.close()
	log("done downloading....")
	os.chdir(dir_path)

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
		# if not store.get(company_name):
		# 	store[company_name] = []
		# obj = {
		# 	"event_name":name,
		# 	"event_date": date,
		# 	"Act":act,
		# 	"Est":est,
		# 	"audio_download_link":audio_url
		# 	}
		# store[company_name].append(obj)
		save_to_file(company_name, name, date, act, est, audio_url)
		log("company_name:" + company_name)
		log("Name:" +  str(name))
		log("date:" +  str(date))
		log("Act:" + str(act))
		log("Est:" +  str(est))
		log("audio_url:" + str(audio_url))
		log("--"*10)

def main():
	for i in range(1, 1000):
		log("page" + str(i) + " ........")
		url = head_url + "/calls?ajax=true&ajax_render=latest&page=" + str(i)
		response = requests.get(url)
		log("Making soup......")
		soup = BeautifulSoup(response.content, "lxml")
		t = threading.Thread(target=parse_source, args=(soup,))
		t.start()
	while threading.active_count() > 1:
		continue

if __name__ == '__main__':
	os.chdir(".")
	main()