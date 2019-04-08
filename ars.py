from flask import Flask, request
import requests
from zappa.async import task
import scraper
import json

app = Flask(__name__)

@task
def get_data(response_url):
    print("cool")
    url = response_url
    text = """
        *Last 3*\n{}\n{}\n{}\n\n*Next Game*\n{}
    """.format(scraper.get_scores()[0],scraper.get_scores()[1],scraper.get_scores()[2],scraper.get_fixtures()[0])
    response = {"text":text}
    r = requests.post(url, json=response)
    print(r.reason)
    return "ok"

@app.route('/', methods=['POST'])
def ars():
    get_data(request.form['response_url'])
    return ""

if __name__ == '__main__':
    app.run(debug=True)
