# 🖥️ Шпаргалка команд сервера

Быстрый справочник команд для управления ботом на сервере.

---

## 🔐 Подключение к серверу

```bash
# Подключение по SSH
ssh root@YOUR_SERVER_IP

# Подключение с другим пользователем
ssh username@YOUR_SERVER_IP

# Выход из SSH
exit
```

---

## 🤖 Управление ботом

### Запуск/Остановка

```bash
# Запуск бота
sudo systemctl start telegram-bot

# Остановка бота
sudo systemctl stop telegram-bot

# Перезапуск бота
sudo systemctl restart telegram-bot

# Проверка статуса
sudo systemctl status telegram-bot
```

### Автозапуск

```bash
# Включить автозапуск при перезагрузке
sudo systemctl enable telegram-bot

# Отключить автозапуск
sudo systemctl disable telegram-bot

# Проверить, включен ли автозапуск
sudo systemctl is-enabled telegram-bot
```

---

## 📊 Просмотр логов

```bash
# Логи в реальном времени (Ctrl+C для выхода)
sudo journalctl -u telegram-bot -f

# Последние 50 строк
sudo journalctl -u telegram-bot -n 50

# Последние 100 строк
sudo journalctl -u telegram-bot -n 100

# Логи за сегодня
sudo journalctl -u telegram-bot --since today

# Логи за последний час
sudo journalctl -u telegram-bot --since "1 hour ago"

# Логи с определенной даты
sudo journalctl -u telegram-bot --since "2024-01-01"

# Логи с ошибками
sudo journalctl -u telegram-bot -p err

# Экспорт логов в файл
sudo journalctl -u telegram-bot > bot_logs.txt
```

---

## 🔄 Обновление бота

### Автоматическое обновление

```bash
cd ~/telegram-bot
./update.sh
```

### Ручное обновление

```bash
cd ~/telegram-bot

# Создание бэкапа
cp data.json data.json.backup.$(date +%Y%m%d)

# Остановка бота
sudo systemctl stop telegram-bot

# Получение обновлений
git pull origin main

# Активация виртуального окружения
source venv/bin/activate

# Обновление зависимостей
pip install -r requirements.txt

# Запуск бота
sudo systemctl start telegram-bot

# Проверка статуса
sudo systemctl status telegram-bot
```

---

## 📁 Работа с файлами

### Навигация

```bash
# Перейти в домашнюю директорию
cd ~

# Перейти в директорию бота
cd ~/telegram-bot

# Показать текущую директорию
pwd

# Список файлов
ls -la

# Просмотр содержимого файла
cat filename

# Просмотр первых 20 строк
head -n 20 filename

# Просмотр последних 20 строк
tail -n 20 filename
```

### Редактирование

```bash
# Редактирование файла в nano
nano filename

# Сохранение в nano: Ctrl+O, Enter
# Выход из nano: Ctrl+X

# Редактирование .env
nano ~/telegram-bot/.env

# Просмотр .env (без редактирования)
cat ~/telegram-bot/.env
```

### Копирование и перемещение

```bash
# Копирование файла
cp source.txt destination.txt

# Копирование директории
cp -r source_dir destination_dir

# Перемещение/переименование
mv old_name.txt new_name.txt

# Удаление файла
rm filename

# Удаление директории
rm -rf directory_name
```

---

## 💾 Резервное копирование

### Создание бэкапа

```bash
# Бэкап data.json
cp ~/telegram-bot/data.json ~/telegram-bot/data.json.backup.$(date +%Y%m%d)

# Бэкап всей директории
tar -czf telegram-bot-backup-$(date +%Y%m%d).tar.gz ~/telegram-bot/

# Создание директории для бэкапов
mkdir -p ~/backups

# Бэкап в отдельную директорию
cp ~/telegram-bot/data.json ~/backups/data.json.$(date +%Y%m%d)
```

### Восстановление из бэкапа

```bash
# Список бэкапов
ls -lh ~/telegram-bot/data.json.backup*

# Восстановление из бэкапа
cp ~/telegram-bot/data.json.backup.20240101 ~/telegram-bot/data.json

# Перезапуск бота после восстановления
sudo systemctl restart telegram-bot
```

### Скачивание бэкапа на локальный компьютер

**На вашем компьютере (PowerShell):**

```powershell
# Скачать data.json
scp root@YOUR_SERVER_IP:~/telegram-bot/data.json ./data.json.backup

# Скачать весь архив
scp root@YOUR_SERVER_IP:~/telegram-bot-backup-*.tar.gz ./
```

---

## 🔍 Диагностика проблем

### Проверка работы бота

```bash
# Статус сервиса
sudo systemctl status telegram-bot

# Проверка процесса
ps aux | grep bot.py

# Проверка портов (если используются)
netstat -tulpn | grep python

# Использование ресурсов
top
# Нажмите 'q' для выхода

# Использование диска
df -h

# Использование памяти
free -h
```

### Проверка конфигурации

```bash
cd ~/telegram-bot
source venv/bin/activate
python check_config.py
```

### Проверка сети

```bash
# Проверка подключения к Telegram API
ping -c 4 api.telegram.org

# Проверка DNS
nslookup api.telegram.org

# Проверка интернет-соединения
curl -I https://api.telegram.org
```

### Проверка Python и зависимостей

```bash
cd ~/telegram-bot
source venv/bin/activate

# Версия Python
python --version

# Список установленных пакетов
pip list

# Проверка конкретного пакета
pip show python-telegram-bot
```

---

## 🔒 Безопасность

### Firewall (UFW)

```bash
# Статус firewall
sudo ufw status

# Включить firewall
sudo ufw enable

# Отключить firewall
sudo ufw disable

# Разрешить SSH
sudo ufw allow ssh

# Разрешить конкретный порт
sudo ufw allow 8080

# Запретить порт
sudo ufw deny 8080

# Удалить правило
sudo ufw delete allow 8080
```

### Пользователи

```bash
# Список пользователей
cat /etc/passwd

# Создание нового пользователя
sudo adduser username

# Добавление в sudo группу
sudo usermod -aG sudo username

# Смена пароля
passwd

# Смена пароля другого пользователя
sudo passwd username

# Переключение на другого пользователя
su - username
```

---

## 🔧 Системные команды

### Обновление системы

```bash
# Обновление списка пакетов
sudo apt update

# Обновление установленных пакетов
sudo apt upgrade -y

# Полное обновление системы
sudo apt update && sudo apt upgrade -y

# Очистка старых пакетов
sudo apt autoremove -y
sudo apt autoclean
```

### Перезагрузка и выключение

```bash
# Перезагрузка сервера
sudo reboot

# Выключение сервера
sudo shutdown -h now

# Запланированная перезагрузка (через 10 минут)
sudo shutdown -r +10

# Отмена запланированной перезагрузки
sudo shutdown -c
```

### Информация о системе

```bash
# Версия ОС
cat /etc/os-release

# Информация о системе
uname -a

# Время работы сервера
uptime

# Дата и время
date

# Часовой пояс
timedatectl

# Установка часового пояса
sudo timedatectl set-timezone Europe/Moscow
```

---

## 📦 Git команды

```bash
cd ~/telegram-bot

# Проверка статуса
git status

# Просмотр изменений
git diff

# Получение обновлений
git fetch origin

# Применение обновлений
git pull origin main

# Просмотр истории коммитов
git log --oneline -10

# Просмотр remote URL
git remote -v

# Сброс локальных изменений
git reset --hard origin/main

# Просмотр текущей ветки
git branch
```

---

## 🔄 Автоматизация (Cron)

### Просмотр и редактирование cron задач

```bash
# Просмотр cron задач
crontab -l

# Редактирование cron задач
crontab -e

# Удаление всех cron задач
crontab -r
```

### Примеры cron задач

```bash
# Бэкап каждый день в 3:00
0 3 * * * cp ~/telegram-bot/data.json ~/backups/data.json.$(date +\%Y\%m\%d)

# Перезапуск бота каждый день в 4:00
0 4 * * * sudo systemctl restart telegram-bot

# Очистка старых бэкапов (старше 30 дней) каждую неделю
0 5 * * 0 find ~/backups/ -name "data.json.*" -mtime +30 -delete

# Обновление бота каждый день в 5:00
0 5 * * * cd ~/telegram-bot && ./update.sh >> ~/update.log 2>&1
```

---

## 🆘 Экстренные команды

### Бот завис

```bash
# Найти процесс
ps aux | grep bot.py

# Убить процесс (замените PID на номер процесса)
kill -9 PID

# Перезапуск через systemd
sudo systemctl restart telegram-bot
```

### Диск заполнен

```bash
# Проверка использования диска
df -h

# Поиск больших файлов
du -h --max-depth=1 / | sort -hr | head -20

# Очистка логов
sudo journalctl --vacuum-time=7d

# Очистка apt кэша
sudo apt clean
sudo apt autoremove -y
```

### Забыли пароль root

1. Зайдите в панель Vultr
2. Server → Settings → Reset Root Password
3. Новый пароль будет отправлен на email

---

## 📝 Полезные алиасы

Добавьте в `~/.bashrc` для удобства:

```bash
nano ~/.bashrc
```

Добавьте в конец файла:

```bash
# Алиасы для бота
alias bot-start='sudo systemctl start telegram-bot'
alias bot-stop='sudo systemctl stop telegram-bot'
alias bot-restart='sudo systemctl restart telegram-bot'
alias bot-status='sudo systemctl status telegram-bot'
alias bot-logs='sudo journalctl -u telegram-bot -f'
alias bot-update='cd ~/telegram-bot && ./update.sh'
alias bot-backup='cp ~/telegram-bot/data.json ~/telegram-bot/data.json.backup.$(date +%Y%m%d)'
```

Применить изменения:

```bash
source ~/.bashrc
```

Теперь можно использовать короткие команды:

```bash
bot-start
bot-logs
bot-update
```

---

## 📞 Быстрая справка

| Действие                | Команда                                                                       |
| ----------------------- | ----------------------------------------------------------------------------- |
| Запустить бота          | `sudo systemctl start telegram-bot`                                           |
| Остановить бота         | `sudo systemctl stop telegram-bot`                                            |
| Перезапустить бота      | `sudo systemctl restart telegram-bot`                                         |
| Статус бота             | `sudo systemctl status telegram-bot`                                          |
| Логи в реальном времени | `sudo journalctl -u telegram-bot -f`                                          |
| Обновить бота           | `cd ~/telegram-bot && ./update.sh`                                            |
| Создать бэкап           | `cp ~/telegram-bot/data.json ~/telegram-bot/data.json.backup.$(date +%Y%m%d)` |
| Редактировать .env      | `nano ~/telegram-bot/.env`                                                    |
| Перезагрузить сервер    | `sudo reboot`                                                                 |

---

**💡 Совет:** Сохраните эту шпаргалку в закладки для быстрого доступа!
