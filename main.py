import notification_type
from config import CONFIG
from ParamikoTest import Client
from telegram_notifications import send_notification


def main():
    print('✨ 🦄 Backups Download ✨')
    for host in CONFIG.get('hosts', []):
        host_name = host.get("remote_url", "🤔")
        print(f'\n🔥 Download from: {host_name}\n')
        client = Client(**host)
        result = client.execute('cd db_backups; ls -dt $PWD/* | head -n 1')
        client.download(result[0].replace('\n', ''), local_path=CONFIG.get('local_path', ''))
        send_notification(
            message=f'{host_name} - backup done!',
            notification_type=notification_type.INFO
        )
        client.disconnect()
    print('\n✨ 🦄 Finished ✨')


if __name__ == '__main__':
    main()
