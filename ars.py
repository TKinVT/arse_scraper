from flask import Flask, request
import requests
from zappa.async import task
import slack
import json

app = Flask(__name__)

@task
def get_data(response_url, request_text):
    text = slack.parser(request_text)
    response = {"text":text}
    r = requests.post(response_url, json=response)
    return "ok"

@app.route('/', methods=['POST'])
def ars():
    response_url = request.form['response_url']
    request_text = request.form['text']
    get_data(response_url, request_text)
    return ""

if __name__ == '__main__':
    app.run(debug=True)
