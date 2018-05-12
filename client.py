from secretsharing import SecretSharer as Shamir
import numpy as np
import json
import requests
import time
from random import randint

#m1_raw = raw_input("User message:")
m1_raw = "It is a secret message"

u_length = 3
v_length = 3
location_U = randint(0, u_length-1)
location_V = randint(0, v_length-1)	

def parser(u1,a,b):
    k = []

    for i in range(len(u1)):
        shares = Shamir.split_secret(u1[i],a,b)
        tmp = []
        for i in shares:
            tmp.append(int(i[2:],16))
        k.append(tmp)

    k = np.transpose(np.array(k)).tolist()
    return k

# url = 'http://localhost:5000/server_0_uploader'
url = 'http://localhost:5000/batch_predict'

server_number = 3
m1 = m1_raw.encode('hex')
# m2 = 'let me die'.encode('hex')

u1 = []
v1 = []
v1_square = []
for i in range(u_length):
	if i == location_U:
		u1.append('1')
	else:
		u1.append('0')

for i in range(v_length):
	if i == location_V:
		v1.append(m1)
		v1_square.append(hex(int(m1,16) ** 2)[2:-1])
	else:
		v1.append('0')
		v1_square.append('0')

# u2 = ['0','1','0','0']
# v2 = [m2,'0','0','0']

start_time = time.time()
u1_split = parser(u1,2,server_number)
v1_split = parser(v1,2,server_number)
v1_square = parser(v1_square,2,server_number)
# h,i,j = parser(u2,2,server_number)
# k,l,m = parser(v2,2,server_number)
print("--- %s seconds ---" % (time.time() - start_time))
#print u1_split
#print v1_split


# payload = {	'u_0' : u1_split[0],
# 			'u_1' : u1_split[1],
# 			'u_2' : u1_split[2],
# 			'v_0' : v1_split[0],
# 			'v_1' : v1_split[1],
# 			'v_2' : v1_split[2],
# 			'v1_square_0' : v1_square[0],
# 			'v1_square_1' : v1_square[1],
# 			'v1_square_2' : v1_square[2],
# 		}
payload = {	'u_0' : 0,
			'u_1' : 1,
		}
r = requests.post(url, json=payload)