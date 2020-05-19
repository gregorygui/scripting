from argparse import ArgumentParser
from string import printable, ascii_letters
from Crypto.Util.number import long_to_bytes


def inverseStr(s):
    return s[::-1]


def ror(x, n, bits=32):
    x = ord(x)
    mask = (2**n) - 1
    mask_bits = x & mask
    return (x >> n) | (mask_bits << (bits - n))


def rol(x, n, bits=32):
    return ror(x, bits - n, bits)


def xor(x, k):
    return chr(ord(x) ^ k)


def rot(x, k):
    return chr((ord(x)+k) % 128)


def vigenere(s, key, mydict=ascii_letters):
    res = str()
    vigdict = dict()
    i = 0
    while i < len(mydict):
        current_index = mydict.index(mydict[i])
        line = str()
        for c in mydict:
            line += mydict[
                (mydict.index(c) + current_index) % len(mydict)
            ]
        vigdict[mydict[i]] = line
        i += 1
    i = 0
    for c in s:
        if c in mydict:
            current_index = vigdict[key[i % len(key)]].index(c)
            res += mydict[current_index]
            i += 1
        else:
            res += c
    return res


def iterate_string(s, a, k, space):
    if a == 0:
        res = s
    else:
        res = str()
        for c in s:
            if space and c == ' ':
                res += c
            elif a == 1:
                res += xor(c, k)
            elif a == 2:
                res += rot(c, k)
            elif a == 3:
                res += chr(rol(c, k) % 128)
            elif a == 4:
                res += chr(ror(c, k) % 128)
    return res


def generate_all(s, a, space, base=printable):
    res = dict()
    for k in base:
        if isinstance(k, str):
            k = ord(k)
        res[k] = iterate_string(s, a, k, space)
    return res


def lendian(s):
    res = list()
    i = 0
    t = list()
    while i < len(s):
        if (i % 4) or (i == 0):
            t.append(s[i])
        else:
            res.append(''.join(t[::-1]))
            t = [s[i]]
        i += 1
    while (i % 4):
        t.append("\x00")
        i += 1
    res.append(''.join(t[::-1]))
    return ''.join(res)


def main():
    parser = ArgumentParser(description='Process some hexadecimal values.',
                            epilog="Algorithm:\n\t- 1: XOR\n\t- 2: ROT\n\t- 3: ROL\n\t- 4: ROR\n\t- 4: bXX\n\t- 5: Vigenere\n\t- 6: Binary")
    parser.add_argument('val',
                        help='the string to decode')
    parser.add_argument('-a', '--algorithm', default=0, type=int,
                        help='Specify the algorithm to use (default=None).')
    parser.add_argument('-k', '--key', default=-1, type=int,
                        help='Specify the key to use (default=All) by using ord(key).')
    parser.add_argument('-l', '--little_endian', action='store_true',
                        help='Specify endianess of the result. (Default=Big)')
    parser.add_argument('-s', '--ignorespace', action='store_true',
                        help='Ignore space in decryption. (Default=True)')
    args = parser.parse_args()
    if args.algorithm == 5:
        args.key = "blorpy"
        print("[!] Vigenere Code implementation use a hardcoded key: \""
              + args.key + "\"")
        res = vigenere(args.val, args.key)
    elif args.algorithm == 6:
        res = long_to_bytes(int(args.val, 2)).decode()
    elif args.algorithm and args.key < 0:
        if args.algorithm == 3 or args.algorithm == 4:
            res = generate_all(args.val,
                               args.algorithm,
                               args.ignorespace,
                               range(0, 32))
        else:
            res = generate_all(args.val,
                               args.algorithm,
                               args.ignorespace,
                               range(0, 127))
    else:
        res = iterate_string(args.val,
                             args.algorithm,
                             args.key,
                             args.ignorespace)
    if args.little_endian:
        res = lendian(res)
    if isinstance(res, dict):
        for k, v in res.items():
            print("+ (key = " + str(k) + ") " + str(args.val) + " ==> " + str(v.encode()))
    else:
        print("+ (key = " + str(args.key) + ") " + str(args.val) + " ==> " + str(res.encode()))


if __name__ == "__main__":
    main()
