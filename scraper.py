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
    scores = [format_html(score) for score in scores_html]

    return scores

def get_fixtures():
    fixtures_container = get_container().find('h2', string="Fixtures").find_next_sibling()
    fixtures_html = fixtures_container.find_all('ul')
    fixtures = [format_html(fixture) for fixture in fixtures_html]

    return fixtures

def get_today():
    today_test = get_container().find('h2', string="Today")
    if today_test:
        today_html = today_test.find_next_sibling().find('ul')
        today = format_html(today_html)

        return today

    return None

def format_html(html):
    dict = {}
    date = html.find_parent().find('h3').text
    date = format_date(date)
    dict['date'] = date

    competition = html.find_parent().find('h4').text
    dict['competition'] = competition

    home, away = html.find_all('span', class_='qa-full-team-name')
    dict['home_team'] = home.text
    dict['away_team'] = away.text

    time_test = html.find('span', class_='sp-c-fixture__number--time')
    if time_test:
        dict['time'] = time_test.text
    else:
        dict['home_score'] = home.find_next().text
        dict['away_score'] = away.find_next().text

    return dict

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
