from cryptography.fernet import Fernet
from backorder.util.util import read_yaml_file
from backorder.constant import *

class Decrypt():
    def __init__(self,massage:str) -> None:
        self.massage = massage.encode()
    def get_decrypted_massage(self):
        key =read_yaml_file(file_path=CREDENTIAL_FILE_PATH)['key']
        fernet = Fernet(key)
        return fernet.decrypt(self.massage).decode()


