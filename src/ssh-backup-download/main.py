import logging
from config import CONFIG, LOGGER_NAME
from ssh import DownloaderClient
from helpers import send_telegram_msg, set_logging


set_logging(log_name='ssh_backup_download.log')
logger = logging.getLogger(LOGGER_NAME)


def download_backup(client, host_name):
    """Download a backup file con el cliente y el
    host_name pasados como parámetro.

    Parameters
    ----------
    client : DownloaderClient
        Client para la descarga por ssh.
    host_name : str
        Nombre del host desde el que se descarga el
        backup.
    """
    try:
        result = client.execute('cd db_backups; ls -dt $PWD/* | head -n 1')
        client.download(result[0].replace('\n', ''),
                        local_path=CONFIG.get('local_path', ''))
    except Exception as e:
        logger.exception(e)
        msg = f'Downloading error: {e}'
        send_telegram_msg(message=msg)
    else:
        send_telegram_msg(message=f'{host_name} - backup done!')
    finally:
        client.disconnect()


def download_all():
    """Descarga los backups de la lista de hosts
    especificada en las variables de entorno (.env).
    """

    for host in CONFIG.get('hosts', []):
        host_name = host.get("remote_url", "🤔")
        logger.info(f'🔥 Download from: {host_name}')
        client = DownloaderClient(**host)
        download_backup(client, host_name)


def main():
    """Ejecuta la descarga de los backups.
    """

    try:
        init_msg = '✨ 🦄 Backups Download ✨'
        logger.info(init_msg)
        send_telegram_msg(init_msg)
        download_all()
    except Exception as e:
        logger.exception(e)
        send_telegram_msg(f'General Error: {e}')
    finally:
        final_msg = '✨ 🦄 Finished ✨'
        logger.info(final_msg)
        send_telegram_msg(final_msg)


if __name__ == '__main__':
    main()
