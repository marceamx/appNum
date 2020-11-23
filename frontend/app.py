from flask import Flask, abort, request
import json
import socket
import urllib.request
import os

app = Flask(__name__)


@app.route('/')
def index():
    return json.dumps({
        'hostname': socket.gethostname()
        })


@app.route('/healtz')
def healtz():
    return "OK"


@app.route('/getwinner', methods = ['GET', 'POST'])
def httpgetwinner():
    try:
        url = "localhost:8080"
        # Can receive data like: 
        # curl -X POST localhost:8081/api/getwinner -H "Content-Type: application/json"  -d '{"url":"localhost:8080"}'
        content = request.json
        if content and 'url' in content:
            url = content['url']
        winner = getwinnernumber(url)
        return app.response_class(
                response='<html><body style="background-color:grey;"><p>The winner is:<strong>'+winner+'</strong></p></body></html>',
            mimetype='text/html'
        )
    except Exception as e:
        print("[ERROR]: {}".format(e))
        abort(503)


@app.route('/api/getwinner', methods = ['GET', 'POST'])
def apigetwinner():
    try:
        url = "localhost:8080"
        # Can receive data like: 
        # curl -X POST localhost:8081/api/getwinner -H "Content-Type: application/json"  -d '{"url":"localhost:8080"}'
        content = request.json
        if content and 'url' in content:
            url = content['url']
        winner = getwinnernumber(url)
        contents = {"the-winner-is":winner}
        return app.response_class(
            response=json.dumps(contents),
            mimetype='application/json'
        )
    except Exception as e:
        print("[ERROR]: {}".format(e))
        abort(503)


def getwinnernumber(url="localhost:8080"):
    try:
        protocol='http://'
        uri='/random'
        contents = urllib.request.urlopen(protocol+url+uri).read()
        contents = contents.decode('utf8')
        return str(contents)
    except Exception as e:
        Ex = ValueError()
        Ex.strerror = "[ERROR]: {}".format(e)
        raise Ex


@app.errorhandler(503)
def page_not_found(e):
    return app.response_class(
        response=json.dumps('{"code":"503","message":"internal error"'),
        mimetype='application/json'
    )


@app.errorhandler(404)
def page_not_found(e):
    return app.response_class(
        response=json.dumps('{"code":"404","message":"page not found"'),
        mimetype='application/json'
    )


if __name__ == '__main__':
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
    port = 80
    tmpport = os.getenv('PORT')
    if tmpport is not None:
        port = tmpport
    app.run(host='0.0.0.0', port=port, debug=True)

