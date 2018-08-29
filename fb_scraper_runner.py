import argparse
from bs4_test import FootballScraper


argparser = argparse.ArgumentParser()
argparser.add_argument('competition')
argparser.add_argument('season')
args = argparser.parse_args()

fb_scraper = FootballScraper(args.competition, args.season)
fb_scraper.scrape()
