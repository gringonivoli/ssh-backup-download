import os
from dotenv import load_dotenv


load_dotenv()

CONFIG = {
    'remote_url': os.getenv('HOST_URLS').split(','),
    'remote_username': os.getenv('HOST_USERS').split(','),
    'remote_passphrase': os.getenv('PASSPHRASE'),
    'remote_ssh_key': os.getenv('SSH_KEY')
}
