from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
#from pl_table_scraper import gather_pl_team_stats
from bs4 import BeautifulSoup
import time
import json


class FootballScraper:
	"""docstring for FootballScraper"""
	def __init__(self, competition, season):
		super(FootballScraper, self).__init__()
		self.competition = competition
		self.season = season


	@staticmethod
	def save_to_json(years):
		print('Saving to json file...')
		with open('fb_data.json', 'w') as f:
			f.write(json.dumps(years, indent=4))
		print('File saved...')

	
	def scrape_team_row(self, driver, team_row):
		x = 0
		# CHANGE DEPENDING ON COMPETITION
		if self.competition == 'pl':
			x += 1
		league_position = f'{team_row}/td[{x+1}]/span[1]'
		team_name = f'{team_row}/td[{x+2}]'	
		played = f'{team_row}/td[{x+3}]'
		won = f'{team_row}/td[{x+4}]'
		drawn = f'{team_row}/td[{x+5}]'
		lost = f'{team_row}/td[{x+6}]'
		goals_for = f'{team_row}/td[{x+7}]'
		goals_against = f'{team_row}/td[{x+8}]'
		goal_difference = f'{team_row}/td[{x+9}]'
		points = f'{team_row}/td[{x+10}]'
	
		elems = [league_position, team_name, played, won, drawn, lost, goals_for, goals_against, goal_difference, points]
		data = [driver.find_element_by_xpath(elem).text for elem in elems]
		stats = {
			'league_position': data[0],
			'team_name': data[1],
			'played': data[2],
			'won': data[3],
			'drawn': data[4],
			'lost': data[5],
			'goals_for': data[6],
			'goals_against': data[7],
			'goal_difference': data[8],
			'points': data[9],
		}
		return stats
		
	
	def gather_pl_team_stats(self, driver):
		team_results = []
		checking = True
		table = 1
		row = 1
		while checking:
			try:
				team_row = f'//*[@id="mainContent"]/div/div[1]/div[2]/div[2]/div/div[1]/div[{table}]/div/table/tbody/tr[{row}]'
				stats = self.scrape_team_row(self, driver, team_row)
				team_results.append(stats)
				x += 2
			except NoSuchElementException:
				checking = False
		return team_results
		
		
	def gather_ucl_team_stats(self, driver):
		team_results = []
		checking = True
		x = 1
		while checking:
			try:
				team_row = f'//*[@id="mainContent"]/div/div[1]/div[2]/div[2]/div/div[1]/div[1]/div/table/tbody/tr[{x}]'
				stats = self.scrape_team_row(driver, team_row)
				team_results.append(stats)
				x += 2
			except NoSuchElementException:
				checking = False


	def scrape_league_result(self, driver, season_location):
		league_finish = {}
		league_finish['season'] = driver.find_element_by_xpath(season_location).text
		driver.find_element_by_xpath(season_location).click()
		time.sleep(3)
		if self.competition == 'pl':
			league_finish['team_stats'] = self.gather_pl_team_stats(driver)
		else if self.competition == 'ucl':
			league_finish['team_stats'] = self.gather_ucl_team_stats(driver)
		return league_finish
		
		
	def scrape(self):
		print('Starting driver...')
		driver = webdriver.Chrome()
		print('Driver started...')
		driver.get('https://www.premierleague.com/tables')
		print('Page opened...')
		time.sleep(3)

		# Close cookie message
		driver.find_element_by_css_selector('body > section > div > div').click()
		time.sleep(2)

		if self.competition == 'pl':
			checking = True
			print(f'Scraping Premier League results for the following season: {self.season}...')
		else if self.competition == 'ucl':
			checking = True
			print(f'Scraping UEFA Champions League results for the following season: {self.season}...')
			# Click competition dropdown
			driver.find_element_by_css_selector('#mainContent > div > div.mainTableTab.active > section > div:nth-child(2) > div.current').click()
			time.sleep(1)
			# Select competiton
			driver.find_element_by_xpath('//*[@id="mainContent"]/div/div[1]/section/div[1]/ul/li[4]').click()
			time.sleep(1)
			# Click 'Group Stage'
			driver.find_element_by_xpath('//*[@id="mainContent"]/div/div[1]/div[2]/div[1]/ul/li[1]').click()
			time.sleep(1)
		else:
			checking = False
			print('Please select a valid competition...')
			
		if checking:	
			# Click season filter dropdown
			driver.find_element_by_css_selector('#mainContent > div > div.mainTableTab.active > section > div:nth-child(3) > div.current').click()
			time.sleep(1)
			years = []
			x = 2
			while checking:
				if self.season == 'all' and x != 2:
					# Click season filter dropdown
					driver.find_element_by_css_selector('#mainContent > div > div.mainTableTab.active > section > div:nth-child(3) > div.current').click()
					time.sleep(1)
				try:
					season_location = f'//*[@id="mainContent"]/div/div[1]/section/div[2]/ul/li[{x}]'
					season = driver.find_element_by_xpath(season_location).text
					if season == self.season or self.season == 'all':
						league_finish = self.scrape_league_result(driver, season_location)
						print(league_finish)
						years.append(league_finish)
						if self.season != 'all':	
							checking = False
					x += 1
				except NoSuchElementException:
					checking = False
					#print('ERROR: Invalid season requested')
			self.save_to_json(years)
		driver.quit()

		
		
		
