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

def get_fixtures():
    fixtures_container = get_scores_fixtures_container().find('h2', string="Fixtures").find_next_sibling()
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
              "url":article_html.a['href'],
              "title":article_html.a.text
              }

    return article

if __name__ == '__main__':
    print(get_scores())
