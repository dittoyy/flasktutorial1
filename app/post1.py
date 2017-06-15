#coding:utf-8
#p70
##json:12b2817fbec86915a6e9b4dbbd3d9036
import feedparser,os
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
@app.route("/", methods=['GET','POST'])
def get_news():
    query = request.form.get("publication")
    if not query or query.lower() not in RSS_FEEDS:
        publication = "bbc"
    else:
        publication = query.lower()
    feed = feedparser.parse(RSS_FEEDS[publication])
    return render_template("home.html",
        articles=feed['entries'])


if __name__ == "__main__":
    app.run(port=5000, debug=True)
