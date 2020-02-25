import sys
from io import StringIO
from paramiko import SSHClient, AutoAddPolicy, RSAKey
from paramiko.auth_handler import AuthenticationException
from scp import SCPClient


class DownloaderClient:
    """Cliente SSH para la conexión, ejecución de comandos
    y descarga de files.

    """
    def __init__(
        self,
        remote_url='',
        remote_username='',
        ssh_key='',
        remote_passphrase='',
        port='22',
        progress_info=False
    ):
        self.remote_url = remote_url
        self.remote_user = remote_username
        self.ssh_key = ssh_key
        self.password = remote_passphrase
        self.port = port
        self.client = None
        self.pkey = self._get_ssh_key()
        self.progress_info = progress_info

    def _connect(self):
        """Conexión SSH.

        Returns
        -------
        SSHClient
            Cliente SSH de paramiko.

        Raises
        ------
        AuthenticationException
            En caso de que la autenticación retorne error.
        """
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
        """Retorna la ssh key para la coneción.

        Returns
        -------
        PKey
            Objeto PKey de paramiko.
        """
        f = open(self.ssh_key, 'r')
        s = f.read()
        keyfile = StringIO(s)
        pkey = RSAKey.from_private_key(keyfile, password=self.password)
        return pkey

    def _progress(self, filename, size, sent):
        """Indica el progreso de la descarga por consola.

        Parameters
        ----------
        filename : str
            file name.
        size : str
            size del file.
        sent : str
            size pasado.
        """
        sys.stdout.write("%s\'s progress: %.2f%%   \r" %
                         (filename, float(sent)/float(size)*100))

    def disconnect(self):
        """Desconecta el cliente de la conexión SSH.
        """
        self.client.close()

    def execute(self, cmd):
        """Ejecuta un comando en el host al que esta conectado
        por SSH.

        Parameters
        ----------
        cmd : str
            Comando para ejecutar en el host al que estamos
            conectados.

        Returns
        -------
        str
            resultado de la salida que produce el comando ejecutado
            en el host al que estamos conectados.
        """
        self.client = self._connect()
        stdin, stdout, stderr = self.client.exec_command(cmd)
        return stdout.readlines()

    def download(self, file, local_path=''):
        """Descarga de un file que se encuentra en el
        host al que nos conectamos por SSH.

        Parameters
        ----------
        file : str
            file name
        local_path : str, optional
            path en donde se guarda el file descargado, by default ''
        """
        client = self._connect()
        progress = self._progress if self.progress_info else None
        scp = SCPClient(client.get_transport(), progress=progress)
        scp.get(file, local_path=local_path)
