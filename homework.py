import logging
import time
import sys
import os

from dotenv import load_dotenv
import telegram
import requests

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(stream=sys.stdout)
formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

load_dotenv()
PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

HOMEWORK_VERDICTS = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}

ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}
RETRY_PERIOD = 600


def check_tokens():
    """Тест .env токенов."""
    return all((PRACTICUM_TOKEN, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID))


def send_message(bot, message):
    """Проходит pytest."""
    logger.debug('Отправка сообщений в telegram')
    logger.info(message)

    try:
        bot.send_message(TELEGRAM_CHAT_ID, message)
    except Exception:
        logger.error('Ошибка отправки сообщения в телеграм')


def get_api_answer(timestamp):
    """Проходит pytest."""
    logger.debug('Отправка api запроса')

    try:
        response = requests.get(
            ENDPOINT,
            timeout=5,
            headers=HEADERS,
            params={'from_date': timestamp})

    except requests.ConnectTimeout:
        logger.error('api connection timeout')
    except requests.RequestException as err:
        logger.error(f'ambiguous api error: {err}')

    if response.status_code != 200:
        raise requests.HTTPError(response.status_code)

    return response.json()


def check_response(response):
    """Проходит pytest."""
    logger.debug('Проверка api ответа')

    if not isinstance(response, dict):
        raise TypeError('В ответе API response не является dict')

    missed_keys = {'homeworks', 'current_date'}
    if missed_keys - response.keys():
        raise TypeError(f'В ответе API нет ожидаемых ключей: {missed_keys}')

    if not isinstance(response['homeworks'], list):
        raise TypeError('В ответе API homeworks не является типом list')

    return len(response['homeworks']) > 0


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
    bot = telegram.Bot(token=TELEGRAM_TOKEN)

    if not check_tokens():
        send_message(bot, 'Ошибка импорта токенов')
        logger.critical('Токен | токены не импортировались')
        sys.exit()

    timestamp = 0
    while True:
        try:
            response = get_api_answer(timestamp)
            has_new_status = check_response(response)
            timestamp = response['current_date']

            if has_new_status:
                message = parse_status(response['homeworks'][0])
                send_message(bot, message)
            else:
                logger.info('Новых статусов нет')

        except TypeError as err:
            logger.error(err)
        except requests.HTTPError as code:
            logger.error(f'api http error, status code: {code}')
        finally:
            time.sleep(RETRY_PERIOD)


if __name__ == '__main__':
    main()
