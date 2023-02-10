from flask import Flask
import flask
import time

app = Flask(__name__)

@app.route("/")
def home():
    resp = flask.Response("Foo bar baz")
    resp.headers['Access-Control-Allow-Origin'] = '*'
    time.sleep(5)
    return resp

@app.route("/cached")
def cached():
    resp = flask.Response("Foo bar baz")
    resp.headers['ETag'] = '5485fac7-ae74'
    resp.headers['Cache-Control'] = 'max-age=31536000'
    time.sleep(5)
    return resp

@app.route("/simple_cached")
def simple_cached():
    resp = flask.Response("Foo bar baz")
    resp.headers['ETag'] = '5485fac7-ae74'
    resp.headers['Cache-Control'] = 'no-cache'
    time.sleep(5)
    return resp

if __name__ == "__main__":
#    app.run(host='0.0.0.0', port=81)
    app.run(port=4243)
