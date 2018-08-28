from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from pl_table_scraper import gather_team_stats
from bs4 import BeautifulSoup
import time

	
print('Starting driver...')
driver = webdriver.Chrome()
print('Driver started...')

driver.get('https://www.premierleague.com/tables')
print('Page opened...')

time.sleep(3)

driver.find_element_by_css_selector('body > section > div > div').click()
time.sleep(2)

years = []
checking = True
x = 2
while checking:
	driver.find_element_by_css_selector('#mainContent > div > div.mainTableTab.active > section > div:nth-child(3) > div.current').click()
	try:
		season = f'//*[@id="mainContent"]/div/div[1]/section/div[2]/ul/li[{x}]'
		league_finish = {}
		league_finish['season'] = driver.find_element_by_xpath(season).text
		driver.find_element_by_xpath(season).click()
		time.sleep(3)
		league_finish['team_stats'] = gather_team_stats(driver)
		years.append(league_finish)
		x += 1
	except NoSuchElementException:
		checking = False

print(years)


driver.find_element_by_css_selector('#mainContent > div > div.mainTableTab.active > section > div:nth-child(2) > div.current').click()





soup = BeautifulSoup(driver.page_source, "html.parser")

#print(soup.prettify())

driver.quit()
