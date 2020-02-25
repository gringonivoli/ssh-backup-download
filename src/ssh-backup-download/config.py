import os
import json
from dotenv import load_dotenv


load_dotenv()


LOGGER_NAME = os.getenv('LOGGER_NAME')


LOGS_PATH = os.getenv('LOGS_PATH')


DEBUG = os.getenv('DEBUG', True)


CONFIG = {
    'hosts': json.loads(os.getenv('HOSTS')),
    'local_path': os.getenv('LOCAL_PATH')
}
