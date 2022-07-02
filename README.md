# StudySentryBot

### О проекте

Telegram бот для оповещения о статусе code-review проекта на курсе Yandex Practicum.  
Проект объединяет работу REST API Yandex Practicum и Telegram, предоставляя студентам удобный способ отслеживать статус
своих домашних работ.

#### Основная цель проекта

StudySentryBot разработан для студентов Yandex Practicum, чтобы помочь им следить за статусами и изменениями в проверке и
ревью их домашних работ.

### Технологии и инструменты

[![Python](https://img.shields.io/badge/Python-3.7%2B-blue?style=for-the-badge&labelColor=333333&logo=python&logoColor=white)](https://www.python.org/)
[![flake8](https://img.shields.io/badge/Code%20Style-flake8-blue?style=for-the-badge&labelColor=333333)](https://flake8.pycqa.org/)
[![python-dotenv](https://img.shields.io/badge/python--dotenv-0.19.0-blue?style=for-the-badge&labelColor=333333&logo=python&logoColor=white)](https://pypi.org/project/python-dotenv/)
[![python-telegram-bot](https://img.shields.io/badge/python--telegram--bot-13.7-blue?style=for-the-badge&labelColor=333333&logo=python&logoColor=white)](https://pypi.org/project/python-telegram-bot/)
[![requests](https://img.shields.io/badge/requests-2.26.0-blue?style=for-the-badge&labelColor=333333&logo=python&logoColor=white)](https://pypi.org/project/requests/)
[![Yandex Practicum API](https://img.shields.io/badge/Yandex%20Practicum%20API-2.1.4-blue?style=for-the-badge&labelColor=333333)](https://link_to_your_api_documentation)
[![Лицензия](https://img.shields.io/github/license/kluevevga/StudySentryBot?color=blue&style=for-the-badge&labelColor=333333&logo=github)](https://github.com/kluevevga/StudySentryBot/blob/master/LICENSE)
[![Размер кода](https://img.shields.io/github/languages/code-size/kluevevga/StudySentryBot?style=for-the-badge&labelColor=333333&logo=github)](https://github.com/kluevevga/StudySentryBot)

### Функциональность бота

- Раз в 10 минут опрашивает API Yandex Practicum и проверяет статус отправленных на ревью домашних работ.
- При обновлении статуса анализирует ответ API и отправляет уведомление в Telegram.
- Логирует свою работу и уведомляет об важных проблемах через Telegram.

#### Примеры уведомлений бота:

StudySentryBot отправляет следующие уведомления о статусе проверки домашней работы ревьюером:

1. Уведомление о принятии домашней работы на ревью.
2. Уведомление о завершении проверки домашней работы.
3. Уведомление о доработке домашней работы, если требуются исправления.

Такие уведомления помогают студентам быстро и удобно следить за статусом своих заданий на платформе Yandex Practicum.

### Запуск проекта

Чтобы запустить проект, выполните следующие шаги:

1. Клонируйте проект и перейдите в него:

   ```shell
   git clone https://github.com/kluevevga/StudySentryBot
   cd StudySentryBot
   ```

2. Установите виртуальное окружение:

   ```shell
   python3 -m venv venv
   ```

3. Активируйте окружение:

    - Windows (PowerShell):

   ```shell
   .\venv\Scripts\Activate.ps1
   ```

    - Windows (Git Bash):

   ```shell
   source venv/Scripts/activate
   ```

    - Linux (Bash):

   ```shell
   source venv/bin/activate
   ```

4. Установите зависимости:

   ```shell
   pip install -r requirements.txt
   ```

5. Запустите проект:

   ```shell
   python3 homework.py
   ```

## Лицензия 📜

Этот проект распространяется под лицензией MIT. Дополнительную информацию можно найти в
файле [LICENSE](https://github.com/kluevevga/StudySentryBot/blob/master/LICENSE).