#coding:utf-8
#p36
import feedparser,os
from flask import Flask,render_template

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
@app.route("/")
@app.route("/<publication>")
def get_news(publication='bbc'):
    feed = feedparser.parse(RSS_FEEDS[publication])
    # first_article = feed['entries'][0]
    return render_template("home.html", articles=feed['entries'])



if __name__ == "__main__":
    app.run(port=5000, debug=True)
