import requests
from bs4 import BeautifulSoup

import re

def get_container():
    url = 'https://www.bbc.com/sport/football/teams/arsenal'
    r = requests.get(url)
    html = r.text
    soup = BeautifulSoup(html, "lxml")

    container = soup.find('div', class_="live-scores-index-container")

    return container

def get_scores():
    scores_container = get_container().find('h2', string="Results").find_next_sibling()
    scores_html = scores_container.find_all('ul')
    scores = [format_score(score) for score in scores_html]
    return scores

def format_score(score_html):
    date = score_html.find_parent().find('h3').text
    home, away = score_html.find_all('span', class_='qa-full-team-name')
    home_team = home.text
    home_score = home.find_next().text
    away_team = away.text
    away_score = away.find_next().text
    score = "{}: {} {} - {} {}".format(date, home_team, home_score, away_score, away_team)

    return score

def get_fixtures():
    fixtures_container = get_container().find('h2', string="Fixtures").find_next_sibling()
    fixtures_html = fixtures_container.find_all('ul')
    fixtures = [format_fixture(fixture) for fixture in fixtures_html]
    return fixtures

def format_fixture(fixture_html):
    date = fixture_html.find_parent().find('h3').text
    time = fixture_html.find('span', class_='sp-c-fixture__number--time').text
    home, away = fixture_html.find_all('span', class_='qa-full-team-name')
    home_team = home.text
    away_team = away.text
    fixture = "{} @{} GMT: {} - {}".format(date, time, home_team, away_team)

    return fixture

if __name__ == '__main__':
    # for s in score.find_all(True):
    #     print("{}: {}".format(s.name, s.text))
    #     print(s.attrs)
    #     print("---")
    print(get_fixtures())
