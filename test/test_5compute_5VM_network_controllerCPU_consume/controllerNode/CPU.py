# sudo apt-get install python3-pip -y
# pip3 install flask
# pip3 install pymongo
# sudo apt-get install speedtest-cli -y

from flask import Flask,request,render_template
from pymongo import MongoClient
import json
import subprocess
import sys
import csv
import datetime

client = MongoClient('mongodb://10.20.0.19:27017/')
db = client['speedTest']

app = Flask(__name__)

# http://10.0.1.99:5000/
@app.route('/')
def speed():
    start = str(datetime.datetime.now())
    print('start time:' + start)
    process = subprocess.Popen(['sar','-u','1','50'], stdout=subprocess.PIPE)
    out, err = process.communicate()
    reader = csv.DictReader(out.decode('ascii').splitlines(),
                            delimiter='\n', skipinitialspace=True,
                            fieldnames=['Retrieving'])
    for index, item in enumerate(reader):
        if index != 0 and index != 1:
            collection = db['NetworkNodeCPU_' + request.args.get("network")]
            data = item['Retrieving'].split(' ')
            if data[1] == 'AM' or data[1] == 'PM':
                data[0] = data[0] + data[1]
                data[1] = ''
            for i in range(data.count('')):
                data.remove('')
            print(data)
            collection.insert_one({
                    'startTime':index - 1,
                    'user':float(data[2]),
                    'nice':float(data[3]),
                    'system':float(data[4]),
                    'iowait':float(data[5]),
                    'steal':float(data[6]),
                    'idle':float(data[7])
                   })
        index + 1
    print('end time:' + str(datetime.datetime.now()))
    return "CPU OK"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

