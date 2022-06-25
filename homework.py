from requests.exceptions import RequestException
from dotenv import load_dotenv
import telegram
import requests
import logging
import time
import sys
import os

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(stream=sys.stdout)
formatter = logging.Formatter(
    '%(asctime)s %(name)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
load_dotenv()


class SurroundError(Exception):
    """Проходит pytest."""

    def __init__(self, *args):
        """Инициирует."""
        self.message = ('Отсутствуют переменные окружения '
                        'Проверьте переменные окружения '
                        'или попробуйте перезвонить позднее.')


PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN') or None
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN') or None
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID') or None
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}
RETRY_PERIOD = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HOMEWORK_VERDICTS = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}


def check_tokens():
    """Проходит pytest."""
    required_tokens = (
        PRACTICUM_TOKEN,
        TELEGRAM_TOKEN,
        TELEGRAM_CHAT_ID)

    if None in required_tokens:
        logger.critical('нет токенов')
        raise SurroundError()


def send_message(bot, message):
    """Проходит pytest."""
    try:
        bot.send_message(TELEGRAM_CHAT_ID, message)
        logger.debug(message)
    except Exception:
        logger.error('ошибка бота')


def get_api_answer(timestamp):
    """Проходит pytest."""
    try:
        payload = {'from_date': timestamp}
        requests_api_headers = HEADERS
        response = requests.get(
            ENDPOINT,
            headers=requests_api_headers,
            params=payload
        )
        if response.status_code != 200:
            raise RequestException()

        return response.json()
    except RequestException as err:
        logger.error(err.message)


def check_response(response):
    """Проходит pytest."""
    if (not isinstance(response, dict) or not
        response.get('homeworks', False) or not
            isinstance(response['homeworks'], list)):
        raise TypeError()


def parse_status(homework):
    """Проходит pytest."""
    if (not homework.get('status', False)
            or not homework.get('status', False) in HOMEWORK_VERDICTS.keys()
            or not homework.get('homework_name', False)):
        raise TypeError()

    return (f'Изменился статус проверки работы'
            f' "{homework["homework_name"]}"'
            f'{HOMEWORK_VERDICTS[homework["status"]]}')


def main():
    """Проходит pytest."""
    check_tokens()
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    while True:
        try:
            response = get_api_answer(0)
            check_response(response)
            message = parse_status(response['homeworks'][0])
            send_message(bot, message)
        except TypeError:
            logger.error('ошибка апы')
        except Exception as error:
            message = f'Сбой в работе программы: {error}'
        finally:
            time.sleep(RETRY_PERIOD)


if __name__ == '__main__':
    main()
