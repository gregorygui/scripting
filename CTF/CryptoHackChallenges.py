from pwn import remote
from urllib3 import PoolManager
from Crypto.Hash import SHA256, MD5
from Crypto.Util.number import bytes_to_long
from Crypto.Cipher import AES
import base64
import json
import time


site_address = ".cryptohack.org"


def getRemoteHttpData(u):
    remote = PoolManager()
    r = remote.request("GET", u)
    return json.loads(r.data)


def getWords():
    with open("wordlist.txt", 'r') as f:
        words = [w.strip() for w in f.readlines()]
    return words


def isPrime(a):
    if a == 1:
        return True
    i = 2
    while (a % i) != 0:
        i += 1
    if i == a:
        return True
    else:
        return False


def generatePrimeList(s, n):
    lp = list()
    for i in range(s, n+1):
        if isPrime(i):
            lp.append(i)
    return lp


def generateFactor(n):
    i = 2
    limit = n**0.5
    while i <= limit:
        if n % i == 0:
            break
        i += 1
    print("+ Success " + str(n) + " = " + str(i) + " (* " + str(n//i) + ")")
    return i


def generateFactorList(n):
    if n == 1:
        return [1]
    i = 2
    while i**2 <= n:
        if n % i == 0:
            print(i)
            res = generateFactorList(n//i)
            if i not in res:
                res.append(i)
            return res
        i += 1
    return [n]


def recGcd(a, b):
    if b == 0:
        return a
    else:
        return recGcd(b, a % b)


def inverseMod(a, n):
    i = 0
    while (i*a+1) % n:
        i += 1
    return (1+i*a)//n


class myRSA():
    def __init__(self, n, e=65537):
        if isinstance(n, int):
            self.n = n
            self.d = e
        elif isinstance(n, tuple):
            self.p = n[0]
            self.q = n[1]
            self.n = self.p*self.q
            self.e = e
            self.d = inverseMod(self.get_phi(), self.e)

    def get_phi(self):
        return (self.p-1)*(self.q-1)

    def get_pub(self):
        return self.e

    def get_priv(self):
        return self.d

    def encrypt(self, m):
        if isinstance(m, int):
            return self.encryptInt(m)
        else:
            return self.encryptStr(m)

    def decrypt(self, c):
        if isinstance(c, int):
            return self.decryptInt(c)
        else:
            return self.decryptStr(c)

    def sign(self, m):
        if isinstance(m, int):
            return self.decryptInt(m)
        else:
            return self.decryptStr(m)

    def encryptInt(self, m):
        return pow(m, self.e, self.n)

    def decryptInt(self, c):
        return pow(c, self.d, self.n)

    def signInt(self, m):
        return self.decryptInt(m)

    def encryptStr(self, m):
        m = bytes_to_long(m)
        return self.encryptInt(m)

    def decryptStr(self, m):
        m = bytes_to_long(m)
        return self.decryptInt(m)

    def signStr(self, m):
        return self.decryptStr(m)


class RemoteChall(remote):
    def __init__(self, server, port):
        super().__init__(server, port)

    def send_response(self, s):
        self.send(json.dumps(s))
        return self.rec_response()

    def rec_response(self):
        return json.loads(self.recvline())


def flagsFromCat():
    r = RemoteChall("socket" + site_address, 11111)
    print(r.rec_response()['Flag:'])
    r.close()


def flagsForSale():
    r = RemoteChall("socket" + site_address, 11112)
    r.recvlines(4)
    print(r.send_response({'buy': 'flag'})['flag'])
    r.close()


def favouriteByte():
    chall = "73626960647f6b206821204f21254f7d694f7624662065622127234f726927756d"
    for k in range(1, 128):
        # solution: k=16
        res = str()
        for c in bytes.fromhex(chall):
            res += chr(c ^ k)
        if "crypto" in res:
            print("[" + str(k) + "] " + chall + " ==> " + res)
            break


def encodingChallenge():
    r = RemoteChall("socket" + site_address, 13377)
    d = dict()
    i = 0
    d[i] = r.rec_response()
    while i < 100:
        if 'type' not in d[i]:
            print("[!][" + str(i-1) + "] Your program failed: " + str(d[i-1]))
            exit()
        if d[i]['type'] == "base64":
            d[i]['decoded'] = base64.b64decode(d[i]['encoded']).decode()
        elif d[i]['type'] == "hex":
            d[i]['decoded'] = bytes.fromhex(d[i]['encoded']).decode()
        elif d[i]['type'] == "rot13":
            d[i]['decoded'] = list()
            for c in d[i]['encoded']:
                if 64 < ord(c) < 91:
                    d[i]['decoded'].append(chr((ord(c)-65 + 13) % 26+65))
                elif 96 < ord(c) < 123:
                    d[i]['decoded'].append(chr((ord(c)-97 + 13) % 26+97))
                else:
                    d[i]['decoded'].append(c)
            d[i]['decoded'] = "".join(d[i]['decoded'])
        elif d[i]['type'] == "bigint":
            d[i]['decoded'] = bytes.fromhex(d[i]['encoded'][2:]).decode()
        elif d[i]['type'] == "utf-8":
            d[i]['decoded'] = list()
            for c in d[i]['encoded']:
                d[i]['decoded'].append(chr(c))
            d[i]['decoded'] = "".join(d[i]['decoded'])
        print("[" + str(i) + "] " + str(d[i]))
        i += 1
        d[i] = r.send_response(d[i-1])
    print(d[i]['flag'])
    r.close()


def rsaStarter():
    print("+ Starter 1: " + str(pow(101, 17, 22663)))
    p = 17
    q = 23
    e = 65537
    starter2 = myRSA((p, q), e)
    m = 12
    print("+ Starter 2: " + str(starter2.encrypt(m)))
    p = 857504083339712752489993810777
    q = 1029224947942998075080348647219
    e = 65537
    starter3 = myRSA((p, q), e)
    print("+ Starter 3: " + str(starter3.get_phi()))
    print("+ Starter 4: " + str(starter3.get_priv()))
    c = 77578995801157823671636298847186723593814843845525223303932
    print("+ Starter 5: " + str(starter3.decrypt(c)))
    key_file = "./private_rsa_starter6.key"
    with open(key_file, 'r') as f:
        lines = f.readlines()
    n = int((lines[0].split(" = "))[1])
    d = int((lines[1].split(" = "))[1])
    chall = myRSA(n, d)
    flag = SHA256.new()
    flag.update("crypto{Immut4ble_m3ssag1ng}".encode())
    c = chall.sign(flag.digest())
    print("+ Starter 6: " + str(hex(c))[2:])


def factoring():
    n = 510143758735509025530880200653196460532653147
    start = time.time()
    generateFactor(n)
    print("+ Elapsed Time: " + str(time.time()-start))


def monoprime():
    output = "./output_monoprime.txt"
    with open(output, 'r') as f:
        lines = f.readlines()
    n = int(lines[0].split(" = ")[1])
    e = int(lines[1].split(" = ")[1])
    ct = int(lines[2].split(" = ")[1])


def passwordAsKeys():
    data = getRemoteHttpData("aes" +
                             site_address + "/passwords_as_keys/encrypt_flag/")
    ct = bytes.fromhex(data['ciphertext'])
    for w in getWords():
        hw = MD5.new()
        hw.update(w.encode())
        key = hw.digest()
        cipher = AES.new(key, AES.MODE_ECB)
        decrypted = cipher.decrypt(ct)
        if "crypto{".encode() in decrypted:
            print("+ [Success] Pasword: " + w)
            print("+ Flag: " + decrypted.decode())
            break


def ecbOracle():
    plain = "g" * 16
    url = "aes" + site_address + "/ecb_oracle/encrypt/"
    url += plain.encode().hex() + "/"
    data = getRemoteHttpData(url)
    ct = bytes.fromhex(data['ciphertext'])
    for w in getWords():
        hw = MD5.new()
        hw.update(w.encode())
        key = hw.digest()
        cipher = AES.new(key, AES.MODE_ECB)
        decrypted = cipher.decrypt(ct[:16])
        if plain.encode() in decrypted:
            print("+ [Success] Pasword: " + w)
            decrypted = cipher.decrypt(ct)
            print("+ Flag: " + decrypted.decode())
            break


def main():
    # ecbOracle()
    e = 1
    c = 9327565722767258308650643213344542404592011161659991421
    n = 245841236512478852752909734912575581815967630033049838269083
    print(generateFactorList(n))


if __name__ == "__main__":
    main()
