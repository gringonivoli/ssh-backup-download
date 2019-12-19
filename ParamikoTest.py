import sys
from io import StringIO
from paramiko import SSHClient, AutoAddPolicy, RSAKey
from paramiko.auth_handler import AuthenticationException
from scp import SCPClient


class Client:
    def __init__(self, remote_url='', remote_username='', remote_ssh_key='', remote_passphrase=''):
        self.remote_url = remote_url
        self.remote_user = remote_username
        self.remote_ssh_key = remote_ssh_key
        self.password = remote_passphrase
        self.client = None
        self.pkey = self.__get_ssh_key()

    def __connect(self):
        if self.client is None:
            try:
                client = SSHClient()
                client.load_system_host_keys()
                client.set_missing_host_key_policy(AutoAddPolicy())
                client.connect(
                    self.remote_url,
                    username=self.remote_user,
                    pkey=self.pkey
                )
            except AuthenticationException:
                raise AuthenticationException('Authentication failed: did you remember to create a SSH Key?')
            finally:
                return client
        return self.client

    def __get_ssh_key(self):
        f = open(self.remote_ssh_key, 'r')
        s = f.read()
        keyfile = StringIO(s)
        pkey = RSAKey.from_private_key(keyfile, password=self.password)
        return pkey

    def __progress(self, filename, size, sent):
    	sys.stdout.write("%s\'s progress: %.2f%%   \r" % (filename, float(sent)/float(size)*100) )

    def disconnect(self):
        self.client.close()

    def execute(self, cmd):
        self.client = self.__connect()
        stdin, stdout, stderr = self.client.exec_command(cmd)
        return stdout.readlines()

    def download(self, file):
        client = self.__connect()
        scp = SCPClient(client.get_transport(), progress=self.__progress)
        scp.get(file)

