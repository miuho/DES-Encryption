# HingOn Miu (hmiu)

import urllib2


# DES Decryption Attack
C0 = "0c80353a2c634be4"
C1 = "4096f9d7977bad4d"
C2 = "60dcd00022474310"
C3 = "5c8eacc3f872e37a"
C4 = "2e6c8afdaecba65e"
C5 = "8d94754e15a587ea"
C6 = "1620cf6b6bc59a0f"
C7 = "e5d74400a7cabebb"
C8 = "e9fa63236a1a6c90"
C  = C0 + C1 + C2 + C3 + C4 + C5 + C6 + C7 + C8
print "Ciphertext: " + C

Z  = "0000000000000000"
Z += "0000000000000000"
Z += "0000000000000000"
Z += "0000000000000000"
Z += "0000000000000000"
Z += "0000000000000000"
Z += "0000000000000000"
Z += "0000000000000000"
Z += "0000000000000000"

def pad_zero(num):
	s = hex(num)[2:]
	if (len(s) == 1):
		s = "0" + s
	return s

P = []
acc = [0,0,0,0, 0,0,0,0]

def padding(num):
	s = ""
	for x in range(1, num):
		s = pad_zero((acc[8 - x] ^ x) ^ num) + s
	return s	

for n in range(0, 8):
	base = -1
	acc = [0,0,0,0, 0,0,0,0]
	for b in range(1, 9):
		i = 0
		while (1):
			try:
				url = urllib2.urlopen(
					"http://127.0.0.1/oracle.php?ticket=" + 
					Z[0:len(Z) - 2*b - 16*n] + 
					pad_zero(i) + 
					padding(b) + 
					C[8*16 - 16*n: 9*16 - 16*n])
			except:
				if (i > 0xff):
					break
				i += 1
				continue
			else:
				acc[8 - b] = i 
				P = [(i ^ b ^ 
				int(C[8*16 - 2*b - 16*n: 
				8*16 - 2*(b-1) - 16*n], 16))] + P
				break

last = P[len(P) - 1]
P = P[0:len(P) - last]
result = "".join([chr(p) for p in P])
print "Plaintext: " + result


# DES Encryption Attack
P = "{\"username\":\"hmiu\",\"is_admin\":\"true\",\"expired\":\"2015-12-10\"}"
print "Plaintext: " + P
pad = chr(0x4)
P = P + pad + pad + pad + pad

Z  = "0000000000000000"
Z += "0000000000000000"
Z += "0000000000000000"
Z += "0000000000000000"
Z += "0000000000000000"
Z += "0000000000000000"
Z += "0000000000000000"
Z += "0000000000000000"
Z += "0000000000000000"

C =  "1231231231231231"

def pad_zero(num):
	s = hex(num)[2:]
	if (len(s) == 1):
		s = "0" + s
	return s

acc = [0,0,0,0, 0,0,0,0]

def padding(num):
	s = ""
	for x in range(1, num):
		s = pad_zero((acc[8 - x] ^ x) ^ num) + s
	return s	

def XOR(d, n):
	p = P[8*(7-n):8*(8-n)]
	s = ""
	for r in range(0, 8):
		s += pad_zero(ord(p[r]) ^ d[r])
	return s	

B = C
for n in range(0, 8):
	acc = [0,0,0,0, 0,0,0,0]
	D = []
	for b in range(1, 9):
		i = 0
		while (1):
			try:
				url = urllib2.urlopen(
					"http://127.0.0.1/oracle.php?ticket=" + 
					Z[0:len(Z) - 2*b - 16*n] + 
					pad_zero(i) + 
					padding(b) + B)
			except:
				if (i > 0xff):
					break
				i += 1
				continue
			else:
				acc[8 - b] = i 
				D = [(i ^ b)] + D
				break
	B = XOR(D, n)
	C = B + C


print "Ciphertext: " + C

try:
	url = urllib2.urlopen(
		"http://127.0.0.1/oracle.php?ticket=" + C)
except:
	print "wrong format"	
else:
	print "Oracle: " + url.read()	



