import requests
from bs4 import BeautifulSoup

def get_container():
    url = 'https://www.bbc.com/sport/football/teams/arsenal'
    r = requests.get(url)
    html = r.text
    soup = BeautifulSoup(html, 'html.parser')

    container = soup.find('div', class_="live-scores-index-container")

    return container

def get_scores():
    scores_container = get_container().find('h2', string="Results").find_next_sibling()
    scores_html = scores_container.find_all('ul')
    scores = [format_score(score) for score in scores_html]

    return scores

def get_fixtures():
    fixtures_container = get_container().find('h2', string="Fixtures").find_next_sibling()
    fixtures_html = fixtures_container.find_all('ul')
    fixtures = [format_fixture(fixture) for fixture in fixtures_html]

    return fixtures

def format_score(score_html):
    date = score_html.find_parent().find('h3').text
    competition = score_html.find_parent().find('h4').text
    date = format_date(date)
    home, away = score_html.find_all('span', class_='qa-full-team-name')

    score = {
            "home_team":home.text,
            "home_score":home.find_next().text,
            "away_team":away.text,
            "away_score":away.find_next().text,
            "date":date,
            "competition":competition
            }

    return score

def format_fixture(fixture_html):
    date = fixture_html.find_parent().find('h3').text
    date = format_date(date)
    competition = fixture_html.find_parent().find('h4').text
    time = fixture_html.find('span', class_='sp-c-fixture__number--time').text
    home, away = fixture_html.find_all('span', class_='qa-full-team-name')

    fixture = {
              "home_team":home.text,
              "away_team":away.text,
              "date":date,
              "time":time,
              "competition":competition
              }

    return fixture

def format_date(unf_date):
    day, date, month, year = unf_date.split()

    formed_date = {
                  "day":day,
                  "date":date,
                  "month":month,
                  "year":year
                  }

    return formed_date


if __name__ == '__main__':
    print(get_scores())
    print(get_fixtures())
