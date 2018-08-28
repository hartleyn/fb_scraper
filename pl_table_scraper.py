from selenium.common.exceptions import NoSuchElementException


def gather_team_stats(driver):
	team_results = []
	checking = True
	x = 1
	while checking:
		try:
			team_row = f'//*[@id="mainContent"]/div/div[1]/div[3]/div/div/div/table/tbody/tr[{x}]'
			team_name = f'{team_row}/td[3]'
			played = f'{team_row}/td[4]'
			won = f'{team_row}/td[5]'
			drawn = f'{team_row}/td[6]'
			lost = f'{team_row}/td[7]'
			goals_for = f'{team_row}/td[8]'
			goals_against = f'{team_row}/td[9]'
			goal_difference = f'{team_row}/td[10]'
			points = f'{team_row}/td[11]'
			
			elems = [team_name, played, won, drawn, lost, goals_for, goals_against, goal_difference, points]
			data = []
			for elem in elems:
				data.append(driver.find_element_by_xpath(elem).text)
			
			stats = {
				'team_name': data[0],
				'played': data[1],
				'won': data[2],
				'drawn': data[3],
				'lost': data[4],
				'goals_for': data[5],
				'goals_against': data[6],
				'goal_difference': data[7],
				'points': data[8],
			}
			team_results.append(stats)
			x += 2
		except NoSuchElementException:
			checking = False
	return team_results
