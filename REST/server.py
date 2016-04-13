# Source: http://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask
import json
import urllib
import urllib2
import urlparse

from flask import Flask, jsonify, abort, make_response, request
from customParser import parseText

app = Flask(__name__)

@app.route('/rest/parse', methods=['POST'])
def parse():
    log = urlparse.parse_qs(request.json)
    txt = log['log'][0]
    # print txt
    # return jsonify({'res': 'res'})

    #membaca semua file di folder log
    res = parseText(txt)

    return jsonify({'res': res})
    # return jsonify({'task': task}), 201

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(debug=True)