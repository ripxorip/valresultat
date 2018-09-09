#!./.venv/bin/python
# import the Flask class from the flask module
from flask import Flask, render_template, Response, request, send_file
import sys
import json
import urllib.request
import zipfile
import xml.etree.ElementTree as ET
import tkinter as tk
import matplotlib
matplotlib.use('Agg') #Agg backend seems to be neccessary
import matplotlib.pyplot as plt
import random

# create the betasky object
# create the application object
app = Flask(__name__)

# use decorators to link the function to a url
@app.route('/')
def index():
    return render_template('index.html')  # return a string

# Function to download and unpack data from valmyndigheten
def downloadAndUnpack():
    URL = 'https://data.val.se/val/val2014/valnatt/valnatt.zip'
    urllib.request.urlretrieve(URL, 'tmp/valnatt.zip')
    zipFile = zipfile.ZipFile("tmp/valnatt.zip", 'r')
    zipFile.extractall("tmp/valnatt")
    zipFile.close()

def getDataRiksdag():
    tree = ET.parse('tmp/valnatt/valnatt_00R.xml')
    root = tree.getroot()
    nation = root.find('NATION')
    # Lists to store data being parsed
    short = []
    procent = []
    for child in nation:
        if child.tag == "GILTIGA":
            procent.append(child.attrib['PROCENT'])
            short.append(child.attrib['PARTI'])
    return procent, short

def getDataRiksdagSturk():
    tree = ET.parse('tmp/valnatt/valnatt_1080R.xml')
    root = tree.getroot()
    sturk = root.findall('./KOMMUN/KRETS_KOMMUN/VALDISTRIKT[@KOD="10801107"]')[0]
    short = []
    procent = []
    for child in sturk:
        if child.tag == "GILTIGA":
            procent.append(child.attrib['PROCENT'])
            short.append(child.attrib['PARTI'])
    return procent, short
    
def getDataKommSturk():
    tree = ET.parse('tmp/valnatt/valnatt_1080K.xml')
    root = tree.getroot()
    sturk = root.findall('./KOMMUN/KRETS_KOMMUN/VALDISTRIKT[@KOD="10801107"]')[0]
    short = []
    procent = []
    for child in sturk:
        if child.tag == "GILTIGA":
            procent.append(child.attrib['PROCENT'])
            short.append(child.attrib['PARTI'])
    return procent, short
    
def getDataKommGBG():
    tree = ET.parse('tmp/valnatt/valnatt_1480K.xml')
    root = tree.getroot()
    kommun = root.find('./KOMMUN[@KOD="1480"]')
    # Lists to store data being parsed
    short = []
    procent = []
    for child in kommun:
        if child.tag == "GILTIGA":
            procent.append(child.attrib['PROCENT'])
            short.append(child.attrib['PARTI'])
    return procent, short    

def plotPNG(short, procent):
    # Party Colors
    color = dict()
    color['S'] = (0.90980392156,0.06666666666,0.17647058823,1)
    color['M'] = (0.05098039215, 0.61568627451, 0.85882352941, 1)
    color['C'] = (0.0156862745, 0.415686275, 0.219607843, 1)
    color['FP'] = (0, 0.415686275, 0.701960784, 1)
    color['KD'] = (0, 0.368627451, 0.631372549, 1)
    color['V'] = (0.929411765, 0.109803922, 0.141176471, 1)
    color['MP'] = (0, 0.77254902, 0.329411765, 1)
    color['SD'] = (1, 0.8, 0, 1)
    color['FI'] = (1, 0.278431373, 0.623529412, 1)
    
    X1 = range(len(procent))
    procentNum = []
    for i in range(len(procent)):                            
        procentNum.append(float(procent[i].replace(',','.')))
    barList = plt.bar(X1, procentNum)
    for i in range(len(barList)):
        try:
            barList[i].set_color(color[short[i]])
        except KeyError:
            barList[i].set_color('black')
    ax = plt.gca()
    ax.set_xticks(range(len(procent)))
    ax.get_yaxis().set_visible(False)
    ax.set_xticklabels(short)
    rects = ax.patches
    plt.ylim([0,45])
    
    for rect, label in zip(rects, procent):
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width() / 2, height + 1, label,
            ha='center', va='bottom')
        
    plt.savefig('tmp/testFig.png', format='png', dpi=200)
    plt.close()

# Function used to get an image of the current result
@app.route('/getResult', methods=['GET'])
def getResult():
    region = request.args.get('region', default='riks', type=str)
    downloadAndUnpack()
    if region == 'riks':
        procent, short = getDataRiksdag()
        plotPNG(short, procent)
    elif region == 'riksSturk':
        procent, short = getDataRiksdagSturk()
        plotPNG(short, procent)
    elif region == 'kommSturk':
        procent, short = getDataKommSturk()
        plotPNG(short, procent)        
    elif region == 'kommGbg':
        procent, short = getDataKommGBG()
        plotPNG(short, procent)

    return send_file('tmp/testFig.png', mimetype='image/jpg', cache_timeout=-1)

# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, use_reloader=True)
