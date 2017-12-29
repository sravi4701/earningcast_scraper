from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from fake_useragent import UserAgent

# ajax call url
# https://earningscast.com//calls?ajax=true&ajax_render=latest&page=1

ua = UserAgent()
header = {"user-agent", ua.chrome}

driver = webdriver.Chrome("/home/ravi/chromedriver")

driver.get("https://earningscast.com//calls?ajax=true&ajax_render=latest&page=1")

