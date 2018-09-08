#!./.venv/bin/python
# import the Flask class from the flask module
from flask import Flask, render_template, Response, request, send_file
import sys
import json

# create the betasky object
# create the application object
app = Flask(__name__)

# use decorators to link the function to a url
@app.route('/')
def index():
    return render_template('index.html')  # return a string

# Function used to get an image of the current result
@app.route('/getResult', methods=['GET'])
def getResult():
    # Implement code that generates the result based on the latest
    # content of the zip from valmyndigheten
    # Dummy below with a static image...
    region = request.args.get('region', default='all', type=str)
    if region == 'all':
        result = 'now you get all'
    else:
        result = 'now you get ' + region
    return send_file('tmp/tester.jpg', mimetype='image/jpeg', cache_timeout=-1)

# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, use_reloader=True)
