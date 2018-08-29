from selenium.common.exceptions import NoSuchElementException


def scrape_team_row(driver, team_row):
	league_position = f'{team_row}/td[2]/span[1]'
	team_name = f'{team_row}/td[3]'	
	played = f'{team_row}/td[4]'
	won = f'{team_row}/td[5]'
	drawn = f'{team_row}/td[6]'
	lost = f'{team_row}/td[7]'
	goals_for = f'{team_row}/td[8]'
	goals_against = f'{team_row}/td[9]'
	goal_difference = f'{team_row}/td[10]'
	points = f'{team_row}/td[11]'
	
	#elems = [league_position, team_name, played, won, drawn, lost, goals_for, goals_against, goal_difference, points]
	#data = []
	#for elem in elems:
		#data.append(driver.find_element_by_xpath(elem).text)
	
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
	

def gather_team_stats(driver):
	team_results = []
	checking = True
	x = 1
	while checking:
		try:
			team_row = f'//*[@id="mainContent"]/div/div[1]/div[3]/div/div/div/table/tbody/tr[{x}]'
						
			stats = scrape_team_row(driver, team_row)
			team_results.append(stats)
			x += 2
		except NoSuchElementException:
			checking = False
	return team_results
