#!/usr/bin/python
# -*- coding: utf-8 -*-

import universal_functions as uf
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
from urllib.parse import urlparse
from urllib.error import HTTPError
import json
import csv

def gather_links(pages_to_crawl={}):
    location_list = []
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
                    location_list.append({'Name': location.string, 'Email': email, 'Type': page})
                except:
                    not_found_count += 1
            print(location_list)
            print('No Mailaddress %d out of %d' % (not_found_count, len(links)))
    return location_list



def create_csv_from_dict(mail_list):
    if mail_list:
        with open('Locations.csv', 'w', newline='', encoding='utf-8') as file:
            fieldnames = [*mail_list[0]]
            writer = csv.DictWriter(file, fieldnames=fieldnames, restval='')
            writer.writeheader()
            for location in mail_list:
                writer.writerow(location)

def create_mailing_list(mail_list):
    if mail_list:
        string_to_write = ''
        with open('mailing_list.txt', 'w') as file:
            for location in mail_list:
                string_to_write = string_to_write + ';' + location['Email']
                string_to_write = string_to_write.strip(';')
            file.write(string_to_write)

def main():
    mail_list = gather_links({'Restaurant': 'http://tourism.olomouc.eu/services/food-and-drink/restaurants/hanacka-hospoda/cs',
                  'Brewery': 'http://tourism.olomouc.eu/services/food-and-drink/breweries/cs',
                  'Cafe': 'http://tourism.olomouc.eu/services/food-and-drink/cafes/beauty-kafe/cs',
                  'Teahouse': 'http://tourism.olomouc.eu/services/food-and-drink/tearooms/cajovna-assamica/cs',
                  'Vinery': 'http://tourism.olomouc.eu/services/food-and-drink/wine-bars/na-brehu-rhony/cs'})
    create_csv_from_dict(mail_list)
    create_mailing_list(mail_list)



if __name__ == '__main__':
    main()