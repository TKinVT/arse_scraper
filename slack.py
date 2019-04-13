from flask import jsonify
import scraper

def parser(text):
    print('hi')
    if len(text) < 1:
        print("if")
        return get_arse()
    elif text.lower() == "fixtures":
        return get_fixtures()
    elif text.lower() == "results" or text.lower() == "scores":
        return get_results()
    elif text.lower() == "articles" or text.lower() == "stories":
        return get_articles()
    elif text.lower() == "diff":
        return get_time_diff()
    else:
        return help

def get_arse():

    last_result = scraper.get_last_score()
    next_fixture = scraper.get_next_fixture()
    last_result_text = "Last: {}".format(format_result(last_result))
    next_fixture_text = "Next: {}".format(format_fixture(next_fixture))
    top_story = scraper.get_articles()[0]
    top_story_text = format_article(top_story)

    text = "{}\n{}\nTop Story: {}".format(next_fixture_text, last_result_text, top_story_text)

    today = scraper.get_today()
    if today:
        today_text = format_today(today)
        text = today_text + "\n" + text
    return text

def get_fixtures():
    fixtures = scraper.get_fixtures()
    text = "*:arsenal: Fixtures:*\n"
    for fixture in fixtures:
        text = text + format_fixture(fixture) + "\n"
    return text

def get_results():
    results = scraper.get_scores()
    text = "*:arsenal: Results:*\n"
    for result in results:
        text = text + format_result(result) + "\n"
    return text

def get_articles():
    articles = scraper.get_articles()
    text = "*Latest :arsenal:-ticles:*\n"
    for article in articles:
        text = text + format_article(article) + "\n"
    return text

def get_time_diff():
    diff = scraper.time_diff()
    text = "Time difference between {} and {}: {}".format(
                                                         diff['current_zone'],
                                                         diff['london_zone'],
                                                         diff['time_difference']
                                                         )
    return text

def format_result(result):
    r = "{} {} // {} <{}|{} - {}> {} // {}".format(
                                               result['date']['month'],
                                               result['date']['date'],
                                               result['home_team'],
                                               result['link'],
                                               result['home_score'],
                                               result['away_score'],
                                               result['away_team'],
                                               result['competition']
                                             )
    r = r.replace('Arsenal', ':arsenal:')
    return r

def format_fixture(fixture):
    r = "{} {} @ {} // {} vs {} // {}".format(
                                               fixture['date']['month'],
                                               fixture['date']['date'],
                                               fixture['time'],
                                               fixture['home_team'],
                                               fixture['away_team'],
                                               fixture['competition']
                                             )
    r = r.replace("Arsenal", ":arsenal:")
    return r

def format_today(today):
    r = "*TODAY :* "
    if 'time' in today:
        text = "{} <{}|vs> {} @ {}".format(today['home_team'],
                                      today['link'],
                                      today['away_team'],
                                      today['time'])
        r = r + text
    else:
        text = "{} <{}|{} - {}> (_{}_) {}".format(today['home_team'],
                                                  today['link'],
                                                  today['home_score'],
                                                  today['away_score'],
                                                  today['progress'],
                                                  today['away_team'])
        r = r + text
    return r

def format_article(article):
    r = "<{}|{}>".format(article['url'], article['title'])
    return r

help = """
    *Ask Arsene about :arsenal:*
    `/ars` to get basic info: Next match, last result and top story
    To see the upcoming fixtures, type `/ars fixtures` or `/ars scores`
    For the latest scores: `/ars results` or `/ars scores`
    To get the top Arsenal stories: `/ars articles`
    The time difference between here and London? `ars diff`
    """

if __name__ == '__main__':
    print(get_arse())
