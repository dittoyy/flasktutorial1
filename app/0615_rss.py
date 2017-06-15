#coding:utf-8
#p77
##json:12b2817fbec86915a6e9b4dbbd3d9036
import feedparser,os
import json
import urllib2
import urllib
from flask import Flask,render_template,request

from flask import send_from_directory


app = Flask(__name__)

RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
'cnn': 'http://rss.cnn.com/rss/edition.rss',
'fox': 'http://feeds.foxnews.com/foxnews/latest',
'iol': 'http://www.iol.co.za/cmlink/1.640'}
#this is your favico.ico prensent in links
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')
DEFAULTS = {'publication':'bbc',
'city': 'London,UK'}
@app.route("/")
def home():
    # get customized headlines, based on user input or default
    publication = request.args.get('publication')
    if not publication:
        publication = DEFAULTS['publication']
    articles = get_news(publication)
    # get customized weather based on user input or default
    city = request.args.get('city')
    if not city:
        city = DEFAULTS['city']
    weather = get_weather(city)
    return render_template("home.html", articles=articles,
    weather=weather)

def get_news(query):
    # query = request.args.get("publication")
    if not query or query.lower() not in RSS_FEEDS:
        publication = DEFAULTS["publication"]
    else:
        publication = query.lower()
    feed = feedparser.parse(RSS_FEEDS[publication])
    # weather = get_weather("London,UK")#weather
    return feed['entries']
# @app.route("/")
def get_weather(query):
    WEATHER_URL='http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=12b2817fbec86915a6e9b4dbbd3d9036'
    query = urllib.quote(query)
    url = WEATHER_URL.format(query)
    data = urllib2.urlopen(url).read()
    parsed = json.loads(data)
    weather = None
    if parsed.get('weather'):
        weather ={'description':parsed['weather'][0]['description'],
        'temperature':parsed['main']['temp'],
        'city':parsed['name'],
        'country': parsed['sys']['country']
        }
    return weather


if __name__ == "__main__":
    app.run(port=5000, debug=True)
