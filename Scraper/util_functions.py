import config as configs
from http import client
import gspread
import config as configs
from datetime import date
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

def connect_sheets():
	"""
	Connects to google service account, exits program if failed
	Return: Successfully connected service account
	"""
	try:
		sa = gspread.service_account(filename = configs.path_google_cred)
	except:
		print('Failed to connect with service account. Please check credentials in config.py file.')
		exit()
	print('Service account connected successfully')
	return (sa)

def open_datasheet(service_acc):
	"""
	Opens data sheet from service account, exits if failed
	Parameter 'service_acc': the connected google service account instance
	Return: Successfully opened data worksheet
	"""
	try:
		sheet = service_acc.open(configs.sheet_name).worksheet(configs.sheet_data)
	except:
		print('Failed to open sheet. Please check sheet name in config.py file.')
		exit()
	print('Data-Worksheet opened successfully')
	return (sheet)

def init_selenium():
	"""
	Initializes the selenium chromium headless driver instance for webscraping, exits if failed
	Return: Successfully initialized instance of selenium chromium headless driver 
	"""
	try:
		chrome_options = webdriver.ChromeOptions()
		chrome_options.add_argument('--headless')
		chrome_options.add_argument('--no-sandbox')
		chrome_options.add_argument('--disable-dev-shm-usage')
		chrome_options.add_argument("--incognito")
		driver = webdriver.Chrome(ChromeDriverManager().install(),options=chrome_options)
	except Exception as ex:
		print(ex)
		exit()
	print('Driver loaded successfully')
	return (driver)

def open_apply_admin(driver):
	"""
	Opens 42 Apply Admin website in chromium headless, exits if failed
	Parameter 'driver': Instance of Selenium Driver
	Return: No Return Value
	"""
	try:
		driver.get(configs.link_admin_login)
		WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.NAME, "commit")))
	except TimeoutError:
		print("Timeout Error, Apply Website did not load correctly.")
		driver.close()
		exit()
	print("Website login screen loaded Successfully")

def login_apply(driver):
	"""
	Logs in to Apply Platform as Admin using config.py file, exits if failed
	Parameter 'driver': Instance of Selenium Driver
	Return: No Return Value
	"""
	#Log in to Apply Platform as Admin using config.py file
	#Use ActionChains as element.send_keys is buggy
	driver.find_element(By.NAME, "user[login]")
	action = ActionChains(driver)
	element = driver.find_element(By.NAME, "user[login]")
	action.send_keys_to_element(element, configs.username)
	action.perform()
	element = driver.find_element(By.NAME, "user[password]")
	action = ActionChains(driver)
	action.send_keys_to_element(element, configs.password)
	action.perform()
	driver.find_element(By.NAME, "commit").click()
	
	#Give Website time to load and check if screen with Api-Confirmation loaded
	time.sleep(5)
	try:
		WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/main/div[2]/form[1]/input[8]')))
	except:
		print("Timeout Error, Website did not load correctly, could not authenticate")
		driver.close()
		exit()
	#confirm usage of 42 apply API with account
	driver.find_element(By.NAME, "commit").click()
	print("Logged in Successfully")

def scrape_data(driver, data_url):
	"""
	Scrapes data from website using given datalink
	Parameter 'driver': Instance of Selenium Driver
	Parameter 'data_url': Data link of Apply Admin site with applied filters
	Return: Scraped data from site (number of applicants within the filter)
	"""
	
	driver.get(data_url)
	f_loaded_element = True
	f_single_value = False
	print(driver.current_url)
	try:
		WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="page-content"]/div[4]/div/div/div[1]/span/b[2]')))
	except Exception as e:
		f_single_value = True
		try:
			WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="page-content"]/div[4]/div/div/div[1]/span/b')))
		except Exception as e:
			print("Timeout Error, Could not find element to scrape")
			f_loaded_element = False
	if f_loaded_element:
		if f_single_value != True:
			element = driver.find_element_by_xpath('//*[@id="page-content"]/div[4]/div/div/div[1]/span/b[2]')
			ele_text = element.text
		else:
			element = driver.find_element_by_xpath('//*[@id="page-content"]/div[4]/div/div/div[1]/span/b')
			ele_text = element.text.replace('all ', '')
		print('Successfully scraped data!')
		return (ele_text)

def get_num_cols(sheet):
	link_cell = sheet.find('Data Link ⇨')
	maxColumns = sheet.col_count
	for cell_data in sheet.row_values(5, maxColumns):
		print(cell_data)
