from curses import color_content
from termios import OLCUC
from xml.etree.ElementTree import tostring
import gspread
import util_functions as utils
from datetime import date
import time

#Connect google service account and data sheet
service_account = utils.connect_sheets()
sheet_data = utils.open_datasheet(service_account)

#initialize Selenium
selenium_driver = utils.init_selenium()

#Get current date in correct format
today = date.today()
today = today.strftime("%d.%m.%Y")

#Open Apply Admin login screen and log into admin account
utils.open_apply_admin(selenium_driver)
utils.login_apply(selenium_driver)

#######Loop through data-sheet, scrape data from links and input into worksheet########
link_cell = sheet_data.find('Data Link ⇨')
if (link_cell == None):
	print("No link cells found. Make sure a row with 'Data Link ⇨' exists. Terminating...")
	exit()

#get last empty row
data = sheet_data.get_all_values()
last_row = 0
for i, r in reversed(list(enumerate(data))):
	if all([c == '' for c in r]) is False:
		last_row = i + 2
		break

col_count = 0
for url in sheet_data.row_values(link_cell.row):
	col_count += 1
	#Add current date in first cell
	if (col_count == 1):
		sheet_data.update_cell(last_row, 1, today)
		continue
	#check if url is empty. If yes, skip cell and continue
	if (url == '' or url == None):
		print('Empty cell skipped')
		continue
	#check if url is just a number. If yes, use this number and do not scrape
	if (url[0].isdigit()):
		sheet_data.update_cell(last_row, col_count, url)
		continue
	#scrape data
	data = utils.scrape_data(selenium_driver, url)
	sheet_data.update_cell(last_row, col_count, data)
selenium_driver.close
