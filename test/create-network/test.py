# sudo apt install sysstat
import subprocess
import sys
import csv

# subprocess.call(['ping', '-c 4','localhost'])

for num1 in range(0,1):
    for num2 in range(0,100):
        if num2 % 10 == 0:
		print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
		print('subnet:'+str(num2))
		print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
		print('\nspeedtest-cli:\n')
		test = subprocess.call(['speedtest-cli'])
		print('\nCPU:\n')
		CPU = subprocess.call(['sar','-u','2','5'])
		print('\nMem:\n')
		Mem = subprocess.call(['free'])
	print('192.'+str(num1)+'.'+str(num2)+'.0/24')
        subprocess.call(['openstack','network','create','--project','admin','a'+str(num1)+'-'+str(num2)+'_network'])
        subprocess.call(['openstack','subnet','create','--project','admin','--network','a'+str(num1)+'-'+str(num2)+'_network','--gateway','192.'+str(num1)+'.'+str(num2)+'.254','--subnet-range','192.'+str(num1)+'.'+str(num2)+'.0/24','a'+str(num1)+'-'+str(num2)+'_subnet'])
        subprocess.call(['openstack','port','create','--project','admin','--network','a'+str(num1)+'-'+str(num2)+'_network','--fixed-ip','ip-address=192.'+str(num1)+'.'+str(num2)+'.254','a'+str(num1)+'-'+str(num2)+'_port'])
        subprocess.call(['openstack','router','add','port','4b06a733-fea2-43ef-a5a2-d56c21307429','a'+str(num1)+'-'+str(num2)+'_port'])