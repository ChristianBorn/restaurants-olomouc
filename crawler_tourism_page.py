#!/usr/bin/python
# -*- coding: utf-8 -*-

import universal_functions as uf
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
from urllib.parse import urlparse
from urllib.error import HTTPError
import json

def gather_links(pages_to_crawl={}):
    location_dict = {}
    if pages_to_crawl:
        for page in pages_to_crawl:
            soup = uf.turn_into_soup(uf.open_website(pages_to_crawl[page]))
            links = soup.find('ul', class_='dalsi_odkazy_3rdLevel')
            links = links.find_all('a')

            not_found_count = 0
            for location in links:
                soup = uf.turn_into_soup(uf.open_website('http:'+location['href']))
                try:
                    email = soup.find('strong', string='E-mail:').find_next_sibling('a')['href']
                    email = email.strip(' ')
                    email = email.replace(' ', '')
                    email = email.replace('mailto:', '')
                    location_dict[location.string] = email
                except:
                    not_found_count += 1
            print(location_dict)
            print('No Mailaddress %d out of %d' % (not_found_count, len(links)))
    with open('errors.txt', 'w') as errorlog:
        errorlog.write('')

#todo: Method to create CSV from dict of mailaddresses



def main():
    gather_links({'Restaurants': 'http://tourism.olomouc.eu/services/food-and-drink/restaurants/hanacka-hospoda/cs'})



if __name__ == '__main__':
    main()