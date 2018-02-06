#!/usr/bin/env python


"""
find_emails.py:

This script finds all email addresses in a given webpage. It finds email addresses in <p>, <href>, and <center> tags. 
It also uses regular expression to find email addresses in many different forms.

Use: python find_emails.py [url]
"""
#__author__ = "Abdul Azeez Omar"
#__email__ = "aoa8363@rit.edu"
#__date__ = "Feb 2018"



import re
import sys
import urllib.request
from bs4 import BeautifulSoup

def find_emails(url):
	emails = set()
	hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
	req = urllib.request.Request(url, headers=hdr)
	content = urllib.request.urlopen(req)
	soup = BeautifulSoup(content, "html.parser")
	email_regexp = r'[a-zA-Z0-9_\-\.]+@[a-zA-Z0-9_\-\.]+\.[a-zA-Z]{2,5}'
	email_regexp1 = r'([a-zA-Z0-9_\-]+\s*\[\s*dot\s*\]\s*)*[a-zA-Z0-9_\-]+\s*\[\s*at\s*\]\s*([a-zA-Z0-9_\-]+\s*\[\s*dot\s*\]\s*)+[a-zA-Z]{2,5}'
	email_regexp2 = r'[a-zA-Z0-9_\-\.]+\s*<\s*at\s*>\s*[a-zA-Z0-9_\-\.]+\.[a-zA-Z]{2,5}'
	# get email address in <href> tag
	mailtos = soup.select('a[href^=mailto]')
	e_iter = re.finditer(email_regexp, str(mailtos))
	for i in e_iter:
		emails.add(i.group())

	# get email address in <p> tag
	p_tag = soup.select('p')
	for tag in p_tag:
		text = tag.get_text().strip()
		e_iter = re.finditer(email_regexp, text)
		for i in e_iter:
			emails.add(i.group())
		e_iter = re.finditer(email_regexp1, text)
		for i in e_iter:
			emails.add(i.group())

	# get email address in <center> tag
	p_tag = soup.select('center')
	for tag in p_tag:
		text = tag.get_text().strip()
		e_iter = re.finditer(email_regexp, text)
		for i in e_iter:
			emails.add(i.group())
		e_iter = re.finditer(email_regexp1, text)
		for i in e_iter:
			emails.add(i.group())
		e_iter = re.finditer(email_regexp2, text)
		for i in e_iter:
			emails.add(i.group())
	
	for e in emails:
		print(e)

if __name__ == '__main__':
	if len(sys.argv) < 2:
		print('Usage: find_emails url')
		sys.exit(-1)

	find_emails(sys.argv[1])

