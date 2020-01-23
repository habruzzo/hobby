#!bin/python3
from selenium import webdriver
import requests
from lxml.html import fromstring
import sys
from traceback import print_stack
from time import sleep

#return driver with proxy
def proxy_driver(proxy_name):
	proxy = webdriver.Proxy()
	proxy.sslProxy = proxy_name
	print(proxy.ssl_proxy)
	driver = webdriver.Firefox(proxy=proxy)
	return driver

def check_page_connection(driver, domain):
	if domain in driver.current_url:
		print(domain + " connected")
		return True
	else:
		return False

#get proxy list
def get_proxies():
    url = 'https://us-proxy.org/'
    response = requests.get(url)
    parser = fromstring(response.text)
    proxies = []
    for i in parser.xpath('//tbody/tr')[:10]:
        if i.xpath('.//td[7][contains(text(),"yes")]') and not i.xpath('.//td[5][contains(text(),"transparent")]'):
            #Grabbing IP and corresponding PORT
            proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            proxies.append(proxy)
    return proxies

#connect to proxy
def test_proxies(proxies):
	for i in proxies:
		driver = proxy_driver(i)
		driver.start_client()
		driver.get('https://google.com')
		if check_page_connection(driver, 'google'):
			driver.close()
			print(i + " connected")
			return i
	print("no proxies available at this time")

def click(item, timesleep=1):
	item.click()
	sleep(timesleep)

def click_arrow(driver):
	arrow = driver.find_element_by_css_selector('.slick-next')
	click(arrow)

def fill_out_form(driver):
	vote_now = driver.find_element_by_class_name("vote-intro--btn")
	click(vote_now)
	for i in range(1, 4):
		click_arrow(driver)
	contra = driver.find_element_by_xpath("/html/body/div[4]/div[7]/div/div[3]/div/div/div[2]/div/div[4]/article/div/div/div/div/div/div[4]")
	click(contra)
	for i in range(1,11):
		click_arrow(driver)
	greta = driver.find_elements_by_id('rebelltitem1')[-1]
	click(greta)
	if not check_page_connection(driver, 'Voting_Result'):
		print_stack(limit=5)
		exit(1)
	category_winners = driver.find_elements_by_class_name('category-winner')
	contra_found = False
	for i in category_winners:
		if 'CONTRAPOINTS' in i.text:
			contra_found = True
			break
		else:
			continue
	if not contra_found:
		print("failed to find contrapoints")
		print_stack(limit=5)
		exit(1)

#go to paper and vote
def connect_and_vote(proxy):
	driver = proxy_driver(proxy)
	driver.start_client()
	driver.get('https://www.papermag.com/st/Break_The_Internet_2019')
	if not check_page_connection(driver, 'papermag'):
		print_stack(limit=5)
		exit(1)
	fill_out_form(driver)
	driver.close()
	driver.quit()

#main
def main():
	proxy_list = get_proxies()
	good_proxy = test_proxies(proxy_list)
	connect_and_vote(good_proxy)


if __name__ == '__main__':
	main()
