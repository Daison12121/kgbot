# 🚀 Деплой бота на сервер

Это руководство поможет вам развернуть бота на сервере для круглосуточной работы.

## Вариант 1: VPS/VDS сервер (Linux)

### Требования

- Ubuntu 20.04+ / Debian 10+ / CentOS 8+
- Python 3.8+
- 512 MB RAM (минимум)
- 1 GB свободного места

### Шаг 1: Подключение к серверу

```bash
ssh user@your-server-ip
```

### Шаг 2: Установка зависимостей

```bash
# Обновление системы
sudo apt update && sudo apt upgrade -y

# Установка Python и pip
sudo apt install python3 python3-pip python3-venv git -y
```

### Шаг 3: Загрузка проекта

```bash
# Создание директории
mkdir -p ~/telegram-bot
cd ~/telegram-bot

# Загрузка файлов (через git или scp)
# Вариант 1: Git
git clone your-repository-url .

# Вариант 2: SCP (с локального компьютера)
# scp -r /path/to/project/* user@server-ip:~/telegram-bot/
```

### Шаг 4: Настройка виртуального окружения

```bash
# Создание виртуального окружения
python3 -m venv venv

# Активация
source venv/bin/activate

# Установка зависимостей
pip install -r requirements.txt
```

### Шаг 5: Настройка конфигурации

```bash
# Создание .env файла
nano .env
```

Заполните данные:

```env
BOT_TOKEN=your_bot_token
CHANNEL_ID=-1001234567890
PHONE_NUMBER=+79991234567
OWNER_ID=123456789
```

Сохраните: `Ctrl+O`, `Enter`, `Ctrl+X`

### Шаг 6: Проверка конфигурации

```bash
python check_config.py
```

### Шаг 7: Настройка systemd для автозапуска

Создайте файл сервиса:

```bash
sudo nano /etc/systemd/system/telegram-bot.service
```

Вставьте:

```ini
[Unit]
Description=Telegram Menu Bot
After=network.target

[Service]
Type=simple
User=your-username
WorkingDirectory=/home/your-username/telegram-bot
Environment="PATH=/home/your-username/telegram-bot/venv/bin"
ExecStart=/home/your-username/telegram-bot/venv/bin/python bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Замените `your-username` на ваше имя пользователя!**

### Шаг 8: Запуск бота

```bash
# Перезагрузка systemd
sudo systemctl daemon-reload

# Включение автозапуска
sudo systemctl enable telegram-bot

# Запуск бота
sudo systemctl start telegram-bot

# Проверка статуса
sudo systemctl status telegram-bot
```

### Шаг 9: Просмотр логов

```bash
# Просмотр логов в реальном времени
sudo journalctl -u telegram-bot -f

# Последние 100 строк
sudo journalctl -u telegram-bot -n 100
```

### Управление ботом

```bash
# Остановка
sudo systemctl stop telegram-bot

# Перезапуск
sudo systemctl restart telegram-bot

# Статус
sudo systemctl status telegram-bot

# Отключение автозапуска
sudo systemctl disable telegram-bot
```

---

## Вариант 2: Windows Server

### Шаг 1: Установка Python

1. Скачайте Python с [python.org](https://www.python.org/downloads/)
2. Установите с опцией "Add to PATH"

### Шаг 2: Установка зависимостей

```powershell
cd C:\telegram-bot
pip install -r requirements.txt
```

### Шаг 3: Настройка автозапуска через Task Scheduler

1. Откройте Task Scheduler
2. Создайте новую задачу:
   - **General**: Имя "Telegram Bot", "Run whether user is logged on or not"
   - **Triggers**: At startup
   - **Actions**: Start a program
     - Program: `C:\Python312\python.exe`
     - Arguments: `C:\telegram-bot\bot.py`
     - Start in: `C:\telegram-bot`
   - **Settings**: "If task fails, restart every 1 minute"

### Шаг 4: Запуск

Запустите задачу вручную или перезагрузите сервер.

---

## Вариант 3: Docker

### Создайте Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "bot.py"]
```

### Создайте docker-compose.yml

```yaml
version: "3.8"

services:
  telegram-bot:
    build: .
    restart: always
    env_file:
      - .env
    volumes:
      - ./data.json:/app/data.json
```

### Запуск

```bash
# Сборка и запуск
docker-compose up -d

# Просмотр логов
docker-compose logs -f

# Остановка
docker-compose down

# Перезапуск
docker-compose restart
```

---

## Вариант 4: Heroku (бесплатный хостинг)

### Шаг 1: Подготовка

Создайте файл `Procfile`:

```
worker: python bot.py
```

Создайте файл `runtime.txt`:

```
python-3.11.0
```

### Шаг 2: Деплой

```bash
# Установка Heroku CLI
# https://devcenter.heroku.com/articles/heroku-cli

# Логин
heroku login

# Создание приложения
heroku create your-bot-name

# Установка переменных окружения
heroku config:set BOT_TOKEN=your_token
heroku config:set CHANNEL_ID=-1001234567890
heroku config:set PHONE_NUMBER=+79991234567
heroku config:set OWNER_ID=123456789

# Деплой
git push heroku main

# Запуск worker
heroku ps:scale worker=1

# Просмотр логов
heroku logs --tail
```

---

## Вариант 5: PythonAnywhere (бесплатный хостинг)

### Ограничения

- Бесплатный план не поддерживает постоянные процессы
- Подходит только для платных планов

### Шаг 1: Регистрация

1. Зарегистрируйтесь на [pythonanywhere.com](https://www.pythonanywhere.com)
2. Выберите платный план (минимум $5/месяц)

### Шаг 2: Загрузка кода

```bash
# В консоли PythonAnywhere
git clone your-repository-url
cd your-repository
pip3 install --user -r requirements.txt
```

### Шаг 3: Настройка Always-On Task

1. Перейдите в "Tasks"
2. Создайте новую задачу:
   - Command: `/home/username/your-repository/venv/bin/python /home/username/your-repository/bot.py`
   - Type: "Always-on"

---

## Мониторинг и обслуживание

### Проверка работы бота

```bash
# Linux
sudo systemctl status telegram-bot

# Docker
docker-compose ps

# Heroku
heroku ps
```

### Обновление бота

```bash
# Linux
cd ~/telegram-bot
git pull
sudo systemctl restart telegram-bot

# Docker
docker-compose pull
docker-compose up -d

# Heroku
git push heroku main
```

### Резервное копирование

```bash
# Создание бэкапа data.json
cp data.json data.json.backup.$(date +%Y%m%d)

# Автоматический бэкап (добавьте в crontab)
0 0 * * * cp /home/user/telegram-bot/data.json /home/user/backups/data.json.$(date +\%Y\%m\%d)
```

---

## Безопасность

### Рекомендации:

1. **Не публикуйте .env файл** в публичных репозиториях
2. **Используйте firewall** на сервере
3. **Регулярно обновляйте** систему и зависимости
4. **Делайте бэкапы** data.json
5. **Используйте SSH ключи** вместо паролей
6. **Ограничьте доступ** к серверу

### Настройка firewall (Linux)

```bash
# Установка UFW
sudo apt install ufw

# Разрешить SSH
sudo ufw allow ssh

# Включить firewall
sudo ufw enable

# Проверка статуса
sudo ufw status
```

---

## Решение проблем

### Бот не запускается

```bash
# Проверка логов
sudo journalctl -u telegram-bot -n 50

# Проверка конфигурации
python check_config.py

# Проверка прав доступа
ls -la /home/user/telegram-bot/
```

### Бот падает при запуске

```bash
# Проверка зависимостей
pip list

# Переустановка зависимостей
pip install --force-reinstall -r requirements.txt
```

### Высокое использование памяти

```bash
# Проверка использования памяти
free -h

# Перезапуск бота
sudo systemctl restart telegram-bot
```

---

## Полезные команды

```bash
# Просмотр процессов Python
ps aux | grep python

# Убить процесс бота (если завис)
pkill -f bot.py

# Проверка использования диска
df -h

# Очистка логов
sudo journalctl --vacuum-time=7d
```

---

**Удачи с деплоем! 🚀**
