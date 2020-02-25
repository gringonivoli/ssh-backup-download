import logging
from config import CONFIG, LOGGER_NAME
from ssh import DownloaderClient
from helpers import send_telegram_msg, set_logging


set_logging(log_name='ssh_backup_download.log')
logger = logging.getLogger(LOGGER_NAME)


def main():
    logger.info('✨ 🦄 Backups Download ✨')
    for host in CONFIG.get('hosts', []):
        host_name = host.get("remote_url", "🤔")
        logger.info(f'🔥 Download from: {host_name}')
        client = DownloaderClient(**host)
        result = client.execute('cd db_backups; ls -dt $PWD/* | head -n 1')
        client.download(result[0].replace('\n', ''), local_path=CONFIG.get('local_path', ''))
        send_telegram_msg(message=f'{host_name} - backup done!')
        client.disconnect()
    logger.info('\n✨ 🦄 Finished ✨')


if __name__ == '__main__':
    main()
