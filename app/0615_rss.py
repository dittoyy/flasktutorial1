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
def get_news():
    query = request.args.get("publication")
    if not query or query.lower() not in RSS_FEEDS:
        publication = "bbc"
    else:
        publication = query.lower()
    feed = feedparser.parse(RSS_FEEDS[publication])
    weather = get_weather("London,UK")#weather
    return render_template("home.html",
        articles=feed['entries'],
        weather=weather)
# @app.route("/")
def get_weather(query):
    api_url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=12b2817fbec86915a6e9b4dbbd3d9036'
    query = urllib.quote(query)
    url = api_url.format(query)
    data = urllib2.urlopen(url).read()
    parsed = json.loads(data)
    # weather=None
    weather = {'description': parsed['weather'][0]['description'],
                'temperature': parsed['main']['temp'],
                'city': parsed['name'],
                'country': parsed['sys']['country']
                }
    # WEATHER_URL ="http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&APPID=12b2817fbec86915a6e9b4dbbd3d9036"
    # CURRENCY_URL ="https://openexchangerates.org//api/latest.json?app_id=12b2817fbec86915a6e9b4dbbd3d9036"
    if parsed.get("weather"):
        weather = {"description":
            parsed["weather"][0]["description"],
            "temperature":parsed["main"]["temp"],
            "city":parsed["name"]
            }
    return weather
# def get_rate(frm, to):
#     all_currency = urllib2.urlopen(CURRENCY_URL).read()
#     parsed = json.loads(all_currency).get('rates')
#     frm_rate = parsed.get(frm.upper())
#     to_rate = parsed.get(to.upper())
#     return to_rate/frm_rate
if __name__ == "__main__":
    app.run(port=5000, debug=True)
