import os
import json
from dotenv import load_dotenv


load_dotenv()

CONFIG = {
    'hosts': json.loads(os.getenv('HOSTS')),
    'local_path': os.getenv('LOCAL_PATH')
}
