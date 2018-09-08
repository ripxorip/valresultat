#!./.venv/bin/python
# import the Flask class from the flask module
from flask import Flask, render_template, Response, request, send_file
import sys
import json
import urllib.request
import zipfile

# create the betasky object
# create the application object
app = Flask(__name__)

# use decorators to link the function to a url
@app.route('/')
def index():
    return render_template('index.html')  # return a string

def downloadAndUnpack():
    URL = 'https://data.val.se/val/val2014/valnatt/valnatt.zip'
    urllib.request.urlretrieve(URL, 'tmp/valnatt.zip')
    zipFile = zipfile.ZipFile("tmp/valnatt.zip", 'r')
    zipFile.extractall("tmp/valnatt")
    zipFile.close()

# Function used to get an image of the current result
@app.route('/getResult', methods=['GET'])
def getResult():
    # Implement code that generates the result based on the latest
    # content of the zip from valmyndigheten
    # Dummy below with a static image...
    region = request.args.get('region', default='all', type=str)
    if region == 'all':
        result = 'now you get all'
        downloadAndUnpack()
    else:
        result = 'now you get ' + region         # Changed to PNG from JPG
    return send_file('tmp/currFig.png', mimetype='image/png', cache_timeout=-1)

# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, use_reloader=True)
