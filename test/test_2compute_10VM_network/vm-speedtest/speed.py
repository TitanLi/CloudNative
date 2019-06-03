from flask import Flask,request,render_template
from pymongo import MongoClient
import json
import subprocess
import sys
import csv
import datetime

client = MongoClient('mongodb://10.20.0.19:27017/')
db = client['speedTest']
collection = db['VM1']

app = Flask(__name__)

# http://10.0.1.99:5000/
@app.route('/')
def speed():
    start = str(datetime.datetime.now())
    process = subprocess.Popen(['speedtest-cli','--server','4413'], stdout=subprocess.PIPE)
    out, err = process.communicate()
    reader = csv.DictReader(out.decode('ascii').splitlines(),
                            delimiter='\n', skipinitialspace=True,
                            fieldnames=['Retrieving'])
    for index, item in enumerate(reader):
    	if index == 5:
            data = item['Retrieving'].split(' ')
            for i in range(data.count('')):
                data.remove('')
            print(data)
            collection.insert_one({
                'startTime':start,
                'networkNum':request.args.get("network"),
               	'dataType':data[0].split(':')[0],
               	'speed':float(data[1]),
               	'unit':data[2]
            })
    	if index == 7:
            data = item['Retrieving'].split(' ')
            for i in range(data.count('')):
                data.remove('')
            print(data)
            collection.insert_one({
                'startTime':start,
                'networkNum':request.args.get("network"),
               	'dataType':data[0].split(':')[0],
               	'speed':float(data[1]),
               	'unit':data[2]
            })
    	index + 1
    return "VM1 OK"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
