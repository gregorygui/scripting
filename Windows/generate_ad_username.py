#!/usr/bin/python3
from itertools import combinations_with_replacement
import string

def complete(f, l):
	res = list()
	res.append(f+"."+l+"\n")
	res.append(f.capitalize()+"."+l.capitalize()+"\n")
	res.append(f+".a."+l+"\n")
	res.append(f.capitalize()+".a."+l.capitalize()+"\n")
	return res

def inif(f, l):
	res = list()
	res.append(f[0]+l+"\n")
	res.append(f[0]+"a"+l+"\n")
	res.append(f.capitalize()[0]+l+"\n")
	res.append(f.capitalize()[0]+"a"+l+"\n")
	res.append(f.capitalize()[0]+l.capitalize()+"\n")
	res.append(f.capitalize()[0]+"a"+l.capitalize()+"\n")
	return res

def three(f, l):
	res = list()
	res.append(f[0:3]+l[0:3]+"\n")
	res.append(f[0:3]+"a"+l[0:3]+"\n")
	f = f.capitalize()
	l = l.capitalize()
	res.append(f[0:3]+l[0:3]+"\n")
	res.append(f[0:3]+"a"+l[0:3]+"\n")
	return res

def rand(f):
	res = list()
	rand = ["".join(x) for x in combinations_with_replacement(string.digits, 3)]
	for r in rand:
		res.append(f[0:3]+r+"\n")
		f = f.capitalize()
		res.append(f[0:3]+r+"\n")
	return res

def inverse(f, l):
	res = list()
	res.append(l+f[0]+"\n")
	res.append(l+f[0:2]+"\n")
	l = l.capitalize()
	res.append(l+f[0]+"\n")
	res.append(l+f[0:2]+"\n")
	return res

def main():
	file = "./username.csv"
	with open(file, 'r') as fp:
		lines = fp.readlines()
	res = list()
	for l in lines:
		l = l.split(';')
		fname = l[0].lower().rstrip('\n')
		lname = l[1].lower().rstrip('\n')
		res += complete(fname, lname)
		res += inif(fname, lname)
		res += three(fname, lname)
		res += inverse(fname, lname)
		res += rand(fname)
	i = 0
	with open("dict.txt", 'w') as fp:
		for e in res:
			fp.write(e)
			i += 1
	print("[COMPLETED] " + str(i) + " usernames created")


if __name__ == '__main__':
	main()