from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
import time
from bs4 import BeautifulSoup

ua = UserAgent()

# ajax call url
# https://earningscast.com//calls?ajax=true&ajax_render=latest&page=1

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
		print("Name:", name)
		print("date:", date)
		print("Act:",act)
		print("Est:", est)
		print("item_url:",item_url)
		print("--"*10)

if __name__ == '__main__':
	opts = Options()
	opts.add_argument("user-agent="+ua.chrome)
	driver = webdriver.Chrome("/home/ravi/chromedriver")
	driver.get("https://earningscast.com//calls?ajax=true&ajax_render=latest&page=1")
	time.sleep(2)
	html_source = driver.page_source
	soup = BeautifulSoup(html_source, "lxml")
	parse_source(soup)
	time.sleep(2)
	driver.close()