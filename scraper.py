import requests
from bs4 import BeautifulSoup
import datetime

def make_soup():
    url = 'https://www.bbc.com/sport/football/teams/arsenal'
    r = requests.get(url)
    html = r.text
    soup = BeautifulSoup(html, 'html.parser')

    return soup

def get_scores_fixtures_container():
    soup = make_soup()
    container = soup.find('div', class_="live-scores-index-container")

    return container

def get_scores():
    scores_container = get_scores_fixtures_container().find('h2', string="Results").find_next_sibling()
    scores_html = scores_container.find_all('ul')
    scores = [format_html(score) for score in scores_html]

    return scores

def get_last_score():
    score_container = get_scores_fixtures_container().find('h2', string="Results").find_next_sibling()
    score_html = score_container.find('ul')
    score = format_html(score_html)

    return score

def get_fixtures():
    fixtures_container = get_scores_fixtures_container().find('h2', string="Fixtures").find_next_sibling()
    fixtures_html = fixtures_container.find_all('ul')
    fixtures = [format_html(fixture) for fixture in fixtures_html]

    return fixtures

def get_next_fixture():
    fixture_container = get_scores_fixtures_container().find('h2', string="Fixtures").find_next_sibling()
    fixture_html = fixture_container.find('ul')
    next_fixture = format_html(fixture_html)

    return next_fixture

def get_today():
    today_test = get_scores_fixtures_container().find('h2', string="Today")
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

    in_prog_test = html.find('span', class_='sp-c-fixture__status')
    if in_prog_test:
        dict['progress'] = in_prog_test.text

    link_test = html.find('a')
    if link_test:
        dict['link'] = "https://www.bbc.com" + link_test['href']

    return dict

def format_date(unf_date, resp="obj"):
    day, date, month, year = unf_date.split()
    date = filter(lambda x: x.isnumeric(), date)

    formed_date = {
                  "day":day,
                  "date":date,
                  "month":month,
                  "year":year
                  }

    return formed_date

def date_obj(unf_date):
    _date = format_date(unf_date)
    year = int(_date['year'])
    month = datetime.datetime.strptime(_date['month'], '%B').month
    day = int(_date['date'])

    date_object = datetime.date(year, month, day)

    return date_object

def get_articles():
    soup = make_soup()
    container = soup.find('h2', id="top-stories-title").find_next_sibling()
    articles_html = container.find_all('h3')
    articles = [format_article(x) for x in articles_html]

    return articles

def format_article(article_html):
    article = {
              "url":"https://www.bbc.com" + article_html.a['href'],
              "title":article_html.a.text
              }

    return article

def time_diff():
    current_mod = requests.get('http://worldtimeapi.org/api/ip').json()
    london_mod = requests.get('http://worldtimeapi.org/api/timezone/Europe/London').json()

    current_zone = current_mod['timezone']
    london_zone = london_mod['timezone']
    diff = int(current_mod['utc_offset'][:3]) - int(london_mod['utc_offset'][:3])

    time_info = {
                'current_zone':current_zone,
                'london_zone':london_zone,
                'time_difference':diff
                }

    return time_info

if __name__ == '__main__':
    print(time_diff())
