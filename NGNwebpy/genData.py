#Generate data to server
import time
import struct
import os
import urllib
import random

from time import strftime
from datetime import date


count = 0
#number of users to be simulated, one for now
Num = 1

while True:
    global count
    #show current time
    #randomly generaytes IP address, only one IP for now
    IPaddress = '.'.join('%s'%random.randint(0, 255) for i in range(4))  #need to change!! -> generate several electricity usage for one IP
    for iter in range(3):
    #randomly generates electricyty usage for each IP address
    	Electr = random.uniform(10.0, 150.0)
    	rectime = date(2015,4+iter,1).strftime("%Y-%m-%d") #need to change -> generate random YYYY-MM-DD
    #parameters about user elecricity usage
    	params = urllib.urlencode({'IPs': IPaddress, 'Electricity': Electr, 'Time': rectime})
   	f = urllib.urlopen("http://168.61.171.247:8080",params)
    #time.sleep(2)
    count = count+1
    if count > Num:
	    break
    
