from config import CONFIG
from ParamikoTest import Client


if __name__ == '__main__':
    config = CONFIG.copy()
    config['remote_url'] = config.get('remote_url')[0]
    config['remote_username'] = config.get('remote_username')[0]
    client = Client(**config)
    result = client.execute('cd db_backups; ls -dt $PWD/* | head -n 1')
    client.download(result[0].replace('\n', ''))
    client.disconnect()
