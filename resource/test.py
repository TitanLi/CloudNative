# OpenStack Create Network Test
# network、subnet、port、router
# subnet range 192.0.0.0/24 ~ 192.255.255.0/24

import subprocess
import sys

subprocess.call(['ping', '-c 4','localhost'])

for num1 in range(0,256):
    for num2 in range(0,256):
        print('192.'+str(num1)+'.'+str(num2)+'.0/24')
        subprocess.call(['openstack','network','create','--project','admin','a'+str(num1)+'-'+str(num2)+'_network'])
        subprocess.call(['openstack','subnet','create','--project','admin','--network','a'+str(num1)+'-'+str(num2)+'_network','--gateway','192.'+str(num1)+'.'+str(num2)+'.254','--subnet-range','192.'+str(num1)+'.'+str(num2)+'.0/24','a'+str(num1)+'-'+str(num2)+'_subnet'])
        subprocess.call(['openstack','port','create','--project','admin','--network','a'+str(num1)+'-'+str(num2)+'_network','--fixed-ip','ip-address=192.'+str(num1)+'.'+str(num2)+'.254','a'+str(num1)+'-'+str(num2)+'_port'])
        subprocess.call(['openstack','router','add','port','7303d563-0977-45f3-8fea-ac09aa540bc4','a'+str(num1)+'-'+str(num2)+'_port'])