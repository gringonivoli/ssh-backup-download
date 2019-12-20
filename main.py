from config import CONFIG
from ParamikoTest import Client


def main():
    print('✨ 🦄 Backups Download ✨')
    for host in CONFIG.get('hosts', []):
        print(f'\n🔥 Download from: {host.get("remote_url", "🤔")}\n')
        client = Client(**host)
        result = client.execute('cd db_backups; ls -dt $PWD/* | head -n 1')
        client.download(result[0].replace('\n', ''), local_path=CONFIG.get('local_path', ''))
        client.disconnect()
    print('\n✨ 🦄 Finished ✨')


if __name__ == '__main__':
    main()
