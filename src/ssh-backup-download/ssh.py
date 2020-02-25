import sys
from io import StringIO
from paramiko import SSHClient, AutoAddPolicy, RSAKey
from paramiko.auth_handler import AuthenticationException
from scp import SCPClient


class DownloaderClient:
    def __init__(self, remote_url='', remote_username='', ssh_key='', remote_passphrase='', port='22', progress_info=False):
        self.remote_url = remote_url
        self.remote_user = remote_username
        self.ssh_key = ssh_key
        self.password = remote_passphrase
        self.port = port
        self.client = None
        self.pkey = self._get_ssh_key()
        self.progress_info = progress_info

    def _connect(self):
        if self.client is None:
            try:
                client = SSHClient()
                client.load_system_host_keys()
                client.set_missing_host_key_policy(AutoAddPolicy())
                client.connect(
                    self.remote_url,
                    username=self.remote_user,
                    pkey=self.pkey,
                    port=self.port
                )
            except AuthenticationException:
                raise AuthenticationException(
                    'Authentication failed: did you remember to create a SSH Key?')
            finally:
                return client
        return self.client

    def _get_ssh_key(self):
        f = open(self.ssh_key, 'r')
        s = f.read()
        keyfile = StringIO(s)
        pkey = RSAKey.from_private_key(keyfile, password=self.password)
        return pkey

    def _progress(self, filename, size, sent):
        sys.stdout.write("%s\'s progress: %.2f%%   \r" %
                         (filename, float(sent)/float(size)*100))

    def disconnect(self):
        self.client.close()

    def execute(self, cmd):
        self.client = self._connect()
        stdin, stdout, stderr = self.client.exec_command(cmd)
        return stdout.readlines()

    def download(self, file, local_path=''):
        client = self._connect()
        progress = self._progress if self.progress_info else None
        scp = SCPClient(client.get_transport(), progress=progress)
        scp.get(file, local_path=local_path)
