#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib.request
from http.cookiejar import CookieJar
from bs4 import BeautifulSoup

def open_website(link):
    website = urllib.request.Request(link, headers={'User-Agent' : "Magic Browser"})
    cj = CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    website = opener.open(website)
    return website

def turn_into_soup(website):
    return BeautifulSoup(website, 'html.parser')
