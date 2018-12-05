import random
import time
import requests
from bs4 import BeautifulSoup
import re
import sqlite3

def get_content_apt(postcode, page=1,url='https://www.domain.com.au/sold-listings/?ptype=apartment&excludepricewithheld=1&ssubs=1'):
	url=url+'&postcode='+str(postcode)+'&page='+str(page)
	content=requests.get(url)
	soup=BeautifulSoup(content.text, 'html.parser')
	return soup

def get_content_house(postcode, page=1,url='https://www.domain.com.au/sold-listings/?ptype=duplex,free-standing,new-home-designs,new-house-land,semi-detached,terrace,town-house,villa&excludepricewithheld=1&ssubs=1'):
	url=url+'&postcode='+str(postcode)+'&page='+str(page)
	content=requests.get(url)
	soup=BeautifulSoup(content.text, 'html.parser')
	return soup

# def connect_db(file,table_name):
# 	conn=sqlite3.connect(file)
# 	c=conn.cursor()
# 	query_create='CREATE TABLE '+table_name+' (price TEXT ,address_line_1 TEXT ,address_line_2 TEXT ,sold_date TEXT ,beds TEXT ,baths TEXT ,carpark TEXT ,space TEXT ,link TEXT);'
# 	c.execute(query_create)

def extract_data(content): # extract link, address, price, Sold_date, beds, baths, carpark, type, postcode, space
	list=content.find_all(class_="search-results__listing")
	current_page_result=[]
	for d in list:
		if d.find(class_="listing-result__price"):
			if d.find(class_="listing-result__price"):
				price=d.find(class_="listing-result__price").get_text()
			if d.find(class_="address-line1"):
				address_line_1=d.find(class_="address-line1").get_text()
			if d.find(class_="address-line2"):
				address_line_2=d.find(class_="address-line2").get_text()
			if d.find(class_="listing-result__tag is-sold"):
				sold_date=d.find(class_="listing-result__tag is-sold").get_text()
			bbcs=d.find_all(class_="property-feature__feature-text-container")
			if bbcs:
				beds=bbcs[0].get_text()
				baths=bbcs[1].get_text()
				carpark=bbcs[2].get_text()
				if len(bbcs)==4:
					space=bbcs[3].get_text()
				else:
					space="null"
				# url=d.find(class_="listing-result__carousel-lazy")["href"]
			else:
				pass
			link=d.find("a")["href"]
			current_page_result.append([price,address_line_1,address_line_2,sold_date,beds,baths,carpark,space,link])
		else:
			pass
	return current_page_result
def main():
	conn=sqlite3.connect('test.db')
	c=conn.cursor()
	#query_create='CREATE TABLE data (price TEXT, address_line_1 TEXT, address_line_2 TEXT, Sold_date TEXT, beds TEXT, baths TEXT, carpark TEXT, space TEXT, link TEXT);'
	#c.execute(query_create)
	postcode_range=[2121]
	query_insert='INSERT INTO data VALUES (?,?,?,?,?,?,?,?,?);'
	for p in postcode_range:
		for page in range(1,30):
			page_result=extract_data(get_content_apt(p,page))
			#verify duplicate#
			c.executemany(query_insert,page_result)
			print(page)
			time.sleep(random.randint(1,2))
	conn.commit()
	conn.close()

if __name__ == '__main__':
    main()
