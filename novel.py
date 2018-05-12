# -*- coding: utf-8 -*-
import urllib
from bs4 import BeautifulSoup
from urllib.request import urlopen
import os
import sys
from colorama import init
init(strip=not sys.stdout.isatty())
from termcolor import cprint 
from pyfiglet import figlet_format
from prettytable import PrettyTable

source = "https://m.biqudu.com"

def search():
	keywords = input("输入书名搜索:")
	keyname = urllib.parse.quote(keywords)
	result = []
	search = urlopen(source + "/SearchBook.php?keyword=" + keyname).read().decode('utf-8')
	bookinfo = BeautifulSoup(search, features='html.parser').find_all('div', class_="bookinfo")

	for items in bookinfo:
		result.append([items.find('h4', class_="bookname").get_text(), 
			items.find('h4', class_="bookname").find('a').get('href'), 
			items.find('div', class_="author").get_text(), 
			items.find('div', class_="update").find('a').get_text()])

	return result

def table(bookid):
	table = urlopen(source + "/booklist/" + bookid + ".html").read().decode('utf-8')
	output_list = BeautifulSoup(table, features='html.parser').find('ul', class_='chapter').find_all('a')
	tables = []

	for link in output_list:
		tables.append([link.get_text(), source + link.get('href')])

	return tables

def content(page):
	content = urlopen(page).read().decode('utf-8')
	out_text = BeautifulSoup(content, features='html.parser').find(id="nr1").get_text().replace("　　", '\r\n\r\n')
	print(out_text)

def turnpage(page):
	turnpage = urlopen(page).read().decode('utf-8')
	pointer = BeautifulSoup(turnpage, features='html.parser')
	pointer_p = pointer.find('td', class_="prev").find('a').get('href')
	pointer_n = pointer.find('td', class_="next").find('a').get('href')
	if pointer_p == '':
		pointer_p = 'none'
	return [pointer_p, pointer_n]

if __name__ == "__main__":
	os.system('clear')
	cprint(figlet_format('telereader', font='doom'), 'green', attrs=['bold'])
	#os.system('clear') use 'cls' for windows
	print('\x1b[6;30;42m' + 'telereader: Read the novel in your terminal' + '\x1b[0m')
	search_result_raw = search()
	search_result = PrettyTable(["Index", "Title", "Author", "Updated to"])
	search_indexof = 1
	for result_raw in search_result_raw:
		search_result.add_row([search_indexof, result_raw[0], result_raw[2].split('：')[1], result_raw[3]])
		search_indexof += 1
	print(search_result)
	search_indexof_selected = input('Select a index to continue: ')
	os.system('clear')
	print('\x1b[6;30;42m' + search_result_raw[int(search_indexof_selected) - 1][0] + '\x1b[0m')
	table_result_raw = table(search_result_raw[int(search_indexof_selected) - 1][1].split('_')[1].replace('/', ''))
	table_result = PrettyTable(["Index", "Title"])
	table_indexof = 1
	for result_raw in table_result_raw:
		table_result.add_row([table_indexof, result_raw[0]])
		table_indexof += 1
	print(table_result)
	table_indexof_selected = input('Select a index to continue: ')

	os.system('clear')
	print('\x1b[6;30;42m' + table_result_raw[int(table_indexof_selected) - 1][0] + '\x1b[0m')
	content(table_result_raw[int(table_indexof_selected) - 1][1])
	page_loc = turnpage(table_result_raw[int(table_indexof_selected) - 1][1])
	loc = int(table_indexof_selected) - 1
	var = 1
	while var == 1:
		turnpage_loc = input("\r\n\r\nType ;p<Enter> to turn to previous page\r\n\r\nType ;n<Enter> to turn to next page\r\n\r\nType ;q<Enter> to quit\r\n\r\n")
		if turnpage_loc == ';p' and page_loc[0] != '':
			os.system('clear')
			print('\x1b[6;30;42m' + table_result_raw[loc - 1][0] + '\x1b[0m')
			loc -= 1
			content(source + search_result_raw[int(search_indexof_selected) - 1][1] + page_loc[0])
		elif turnpage_loc == ';n' and page_loc[0] != '':
			os.system('clear')
			print('\x1b[6;30;42m' + table_result_raw[loc + 1][0] + '\x1b[0m')
			loc += 1
			content(source + search_result_raw[int(search_indexof_selected) - 1][1] + page_loc[1])
		elif turnpage_loc == ';q':
			os.system('clear')
			sys.exit()
