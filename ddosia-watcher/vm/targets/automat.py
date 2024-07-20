from recover import recover_targets
import subprocess
import json
import os
import glob
import requests

GRUPO = -1 #OFUSCADO
TOKEN = "$OFUSCADO$"
API_URL = "https://api.telegram.org/{}/{}"

def send_document(file_path, receptor=GRUPO, token=TOKEN):
    chat_id = receptor
    method = "sendDocument"
    files = {
        'document': open(file_path, 'rb')  #
    }
    data = {
        'chat_id': chat_id
    }
    response = requests.post(API_URL.format(token, method), files=files, data=data)
    return response.json()

def send_message(text,receptor=GRUPO,token = TOKEN ):
    chat_id = receptor
    method = "sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    response = requests.post(API_URL.format(token, method), data=payload)
    return response.json()

def get_targets(ip):
    for f in glob.glob('dumps/*'):
        os.remove(f)
    subprocess.run(["frida.exe", "-l", "targets.js", "./d_win_x64.exe", "--", "-p", "{}".format(ip)])
    recover_targets()
    with open("resumen.txt",'r') as f:
        cont = f.read()
    with open("out.json",'r') as f:
        ndata = f.read()
    with open("out.old.json",'r') as f:
        odata = f.read()
    if ndata == odata:
        print("Mismos targets....")
        print(ndata)
        print(odata)
    else:
        print("Targets diferentes")
        x=send_message("Los targets de DDoSia han cambiado....")
        print(x)
        send_message(cont)
        send_document("out.json")
    return cont

def get_ip():
    with open('ip.json','r') as f:
        ip = json.load(f)['ip']
    return ip

if __name__ == "__main__":
    ip = get_ip()
    get_targets(ip)
