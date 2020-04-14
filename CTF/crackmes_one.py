from random import randrange


def crackmes_1_get_pass():
    # https://crackmes.one/crackme/5c9126c033c5d46ecd37c8f4
    lower = 33
    upper = 126
    res = list()
    res.append(chr(randrange(ord("G")+1, upper)))
    res.append(chr(randrange(lower, ord("m")-1)))
    res.append("V")
    res.append(chr(randrange(ord("f"), upper)))
    res.append(chr(randrange(lower, ord("3"))))
    res.append(chr(randrange(ord("y")+1, upper)))
    res.append(chr(randrange(ord("8"), upper)))
    res.append(chr(randrange(lower, ord("N")-1)))
    res.append(chr(randrange(lower, upper)))
    while res[-1] == "R":
        res[-1] = chr(randrange(lower, upper))
    res.append("2")
    return "".join(res)


if __name__ == "__main__":
    print(crackmes_1_get_pass())
