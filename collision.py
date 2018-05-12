from secretsharing import SecretSharer as Shamir
import numpy as np
from decimal import *

server_number = 3

def parser(u1,a,b):
	k = []

	for i in range(len(u1)):
		shares = Shamir.split_secret(u1[i],a,b)
		tmp = []
		for i in shares:
			tmp.append(int(i[2:],16))
		k.append(tmp)

	k = np.transpose(np.array(k))
	return k

def recover(s):
	db = []

	for i in range(np.shape(s)[1]):
		for j in range(np.shape(s)[2]):
			tmp1 = []
			for k in range(np.shape(s)[0]):
				tmp1.append(str(k+1)+"-"+str(hex(s[k][i][j]))[2:-1])
			answer = Shamir.recover_secret(tmp1)
			if len(answer) % 2 == 1:
				answer = '0' + answer
			db.append(answer.decode('hex'))
	return db



m1 = 'the first secret message'.encode('hex')
m2 = 'the second secret message'.encode('hex')

u1 = ['1']
v1 = [m1]
v1_square = [hex(int(m1,16) ** 2)[2:-1]]

u2 = ['1']
v2 = [m2]
v2_square = [hex(int(m2,16) ** 2)[2:-1]]

#for i in range(server_number):
#	s = u_share[i].reshape([-1,1]).dot(v_share[i].reshape([1,-1]))

a,b,c = parser(u1,2,server_number)
d,e,f = parser(v1,2,server_number)
d_1,e_1,f_1 = parser(v1_square,2,server_number)
h,i,j = parser(u2,2,server_number)
k,l,m = parser(v2,2,server_number)
k_1,l_1,m_1 = parser(v2_square,2,server_number)

s1 = a.reshape([-1,1]).dot(d.reshape([1,-1]))
s2 = b.reshape([-1,1]).dot(e.reshape([1,-1]))
s3 = c.reshape([-1,1]).dot(f.reshape([1,-1]))

s1_1 = a.reshape([-1,1]).dot(d_1.reshape([1,-1]))
s2_1 = b.reshape([-1,1]).dot(e_1.reshape([1,-1]))
s3_1 = c.reshape([-1,1]).dot(f_1.reshape([1,-1]))

s4 = h.reshape([-1,1]).dot(k.reshape([1,-1]))
s5 = i.reshape([-1,1]).dot(l.reshape([1,-1]))
s6 = j.reshape([-1,1]).dot(m.reshape([1,-1]))

s4_1 = h.reshape([-1,1]).dot(k_1.reshape([1,-1]))
s5_1 = i.reshape([-1,1]).dot(l_1.reshape([1,-1]))
s6_1 = j.reshape([-1,1]).dot(m_1.reshape([1,-1]))

s1 += s4
s2 += s5
s3 += s6

s1_1 += s4_1
s2_1 += s5_1
s3_1 += s6_1

s = np.array([s1,s2,s3])
s_1 = np.array([s1_1,s2_1,s3_1])

msg_sum = recover(s)[0].encode('hex')
square_sum = recover(s_1)[0].encode('hex')

getcontext().prec = 100
msg_minus = long(Decimal(int(square_sum,16) * 2-int(msg_sum,16) ** 2).sqrt())

print hex((-msg_minus + int(msg_sum,16))/2)[2:-1].decode('hex')
print hex((msg_minus + int(msg_sum,16))/2)[2:-1].decode('hex')

