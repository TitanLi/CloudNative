from pymongo import MongoClient
import subprocess
import sys
import csv
import grequests

# subprocess.call(['ping', '-c 4','localhost'])
client = MongoClient('mongodb://10.20.0.19:27017/')
db = client['speedTest']

for num1 in range(0,1):
    for num2 in range(0,101):
        if num2 % 10 == 0:
            urls = [
                'http://10.0.1.97:5000/?network='+str(num2),
                'http://10.0.1.21:5000/?network='+str(num2),
                'http://10.0.1.22:5000/?network='+str(num2),
                'http://10.0.1.23:5000/?network='+str(num2),
                'http://10.0.1.24:5000/?network='+str(num2),
                'http://10.0.1.35:5000/?network='+str(num2)
            ]
            print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
            print('subnet:'+str(num2))
            print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
            print('\nMem:\n')
            process = subprocess.Popen(['free'], stdout=subprocess.PIPE)
            out, err = process.communicate()
            reader = csv.DictReader(out.decode('ascii').splitlines(),
                                        delimiter='\n', skipinitialspace=True,
                                        fieldnames=['Retrieving'])
            for index, item in enumerate(reader):
                if index == 1:
                    data = item['Retrieving'].split(' ')
                    for i in range(data.count('')):
                        data.remove('')
                    print(data)
                    collection = db['NetworkNodeMem']
                    collection.insert_one({
                        'networkNum':num2,
                        'total':float(data[1]),
                        'used':float(data[2]),
                        'free':float(data[3]),
                        'shared':float(data[4]),
                        'buff-cache':float(data[5]),
                        'available':float(data[6])
                    })
            index + 1
            
            results = grequests.map((grequests.get(u) for u in urls), size=6)
            print(results)
        print('192.'+str(num1)+'.'+str(num2)+'.0/24')
        subprocess.call(['openstack','network','create','--project','admin','a'+str(num1)+'-'+str(num2)+'_network'])
        subprocess.call(['openstack','subnet','create','--project','admin','--network','a'+str(num1)+'-'+str(num2)+'_network','--gateway','192.'+str(num1)+'.'+str(num2)+'.254','--subnet-range','192.'+str(num1)+'.'+str(num2)+'.0/24','a'+str(num1)+'-'+str(num2)+'_subnet'])
        subprocess.call(['openstack','port','create','--project','admin','--network','a'+str(num1)+'-'+str(num2)+'_network','--fixed-ip','ip-address=192.'+str(num1)+'.'+str(num2)+'.254','a'+str(num1)+'-'+str(num2)+'_port'])
        subprocess.call(['openstack','router','add','port','03d3e3ed-53b2-4c0e-b250-04683ab586a4','a'+str(num1)+'-'+str(num2)+'_port'])
