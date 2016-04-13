# Source: http://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask
import json
import urllib
import urllib2
import urlparse

from flask import Flask, jsonify, abort, make_response

app = Flask(__name__)
from customParser import parseText

from flask import request

@app.route('/rest/parse', methods=['POST'])
def parse():

    log = urlparse.parse_qs(request.json)
    txt = log['log'][0]
    # return jsonify({'res': 'res'})
    res = parseText(txt)

    print res

    return jsonify({'res': res})
    # return jsonify({'task': task}), 201

if __name__ == '__main__':
    app.run(debug=True)