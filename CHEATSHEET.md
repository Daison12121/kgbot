# 📋 Шпаргалка по командам

## Быстрый старт

```bash
# 1. Установка зависимостей
pip install -r requirements.txt

# 2. Настройка .env
copy .env.example .env
# Отредактируйте .env файл

# 3. Проверка конфигурации
python check_config.py

# 4. Тестирование
python test_bot.py

# 5. Запуск бота
python bot.py
```

## Команды бота

### Для всех пользователей

```
/start - Показать информацию о боте
```

### Для администраторов

#### Управление меню

```
/set_menu - Установить новое меню
/publish_menu - Опубликовать меню в канале
/menu_info - Показать текущее меню
/skip - Пропустить добавление фото
```

#### Управление администраторами

```
/add_admin <user_id> - Добавить администратора
/remove_admin <user_id> - Удалить администратора
/list_admins - Список администраторов
```

## Процесс обновления меню

```
1. /set_menu
2. [Отправить текст меню]
3. [Отправить фото или /skip]
4. /publish_menu
```

## Получение ID

### Ваш Telegram ID

```
1. Найти @userinfobot
2. Нажать Start
3. Скопировать ID
```

### ID канала

```
1. Добавить @userinfobot в канал
2. Переслать сообщение из канала боту
3. Скопировать ID (начинается с -100)
```

### ID другого пользователя

```
1. Попросить пользователя написать @userinfobot
2. Пользователь отправляет вам свой ID
```

## Настройка канала

### Добавление бота в канал

```
1. Открыть канал → Настройки
2. Администраторы → Добавить администратора
3. Найти бота и добавить
4. Дать права:
   ✅ Публикация сообщений
   ✅ Редактирование сообщений
   ✅ Удаление сообщений
```

### Настройка обсуждений

```
1. Настройки канала → Обсуждения
2. Включить обсуждения
3. Добавить бота в группу обсуждений
4. Дать права на удаление сообщений
```

### Отключение Privacy Mode

```
1. Найти @BotFather
2. /setprivacy
3. Выбрать бота
4. Disable
```

## Форматирование текста

```markdown
_жирный_
_курсив_
`моноширинный`
**очень жирный**
**подчеркнутый**
~зачеркнутый~
```

## Структура .env файла

```env
BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
CHANNEL_ID=-1001234567890
PHONE_NUMBER=+79991234567
OWNER_ID=123456789
STORAGE_FILE=data.json
```

## Полезные скрипты

```bash
# Проверка конфигурации
python check_config.py

# Тестирование бота
python test_bot.py

# Запуск бота
python bot.py
```

## Решение проблем

### Бот не отвечает

```
✓ Проверить BOT_TOKEN в .env
✓ Убедиться, что бот запущен
✓ Проверить логи в консоли
```

### Не публикуется меню

```
✓ Проверить CHANNEL_ID в .env
✓ Убедиться, что бот админ канала
✓ Проверить права бота в канале
```

### Не удаляются ссылки

```
✓ Бот должен быть админом группы обсуждений
✓ Privacy Mode должен быть отключен
✓ У бота должны быть права на удаление
```

## Логи и отладка

### Просмотр логов (Linux)

```bash
# Последние 50 строк
sudo journalctl -u telegram-bot -n 50

# В реальном времени
sudo journalctl -u telegram-bot -f

# За последний час
sudo journalctl -u telegram-bot --since "1 hour ago"
```

### Управление сервисом (Linux)

```bash
# Запуск
sudo systemctl start telegram-bot

# Остановка
sudo systemctl stop telegram-bot

# Перезапуск
sudo systemctl restart telegram-bot

# Статус
sudo systemctl status telegram-bot

# Включить автозапуск
sudo systemctl enable telegram-bot

# Отключить автозапуск
sudo systemctl disable telegram-bot
```

## Резервное копирование

```bash
# Создать бэкап
cp data.json data.json.backup

# Восстановить из бэкапа
cp data.json.backup data.json

# Бэкап с датой
cp data.json data.json.$(date +%Y%m%d)
```

## Обновление бота

```bash
# 1. Остановить бота
sudo systemctl stop telegram-bot

# 2. Создать бэкап
cp data.json data.json.backup

# 3. Обновить код
git pull

# 4. Обновить зависимости
pip install -r requirements.txt

# 5. Запустить бота
sudo systemctl start telegram-bot

# 6. Проверить статус
sudo systemctl status telegram-bot
```

## Регулярные выражения для ссылок

Бот удаляет сообщения, содержащие:

```
http://...
https://...
www.example.com
example.com
t.me/...
```

Администраторы могут отправлять ссылки без ограничений.

## Структура проекта

```
telegram-bot/
├── bot.py              # Основной файл бота
├── config.py           # Конфигурация
├── storage.py          # Хранилище данных
├── check_config.py     # Проверка конфигурации
├── test_bot.py         # Тестирование
├── requirements.txt    # Зависимости
├── .env               # Конфигурация (не коммитить!)
├── .env.example       # Пример конфигурации
├── data.json          # Данные (создается автоматически)
├── README.md          # Документация
├── QUICKSTART.md      # Быстрый старт
├── EXAMPLES.md        # Примеры меню
├── DEPLOY.md          # Деплой на сервер
└── CHEATSHEET.md      # Эта шпаргалка
```

## Горячие клавиши (для разработки)

```
Ctrl+C - Остановить бота
Ctrl+Z - Приостановить процесс (Linux)
```

## Полезные ссылки

- [@BotFather](https://t.me/BotFather) - создание ботов
- [@userinfobot](https://t.me/userinfobot) - получение ID
- [Telegram Bot API](https://core.telegram.org/bots/api) - документация API
- [python-telegram-bot](https://docs.python-telegram-bot.org/) - документация библиотеки

## Контакты для поддержки

При возникновении проблем:

1. Проверьте README.md
2. Проверьте QUICKSTART.md
3. Запустите check_config.py
4. Запустите test_bot.py
5. Проверьте логи

---

**Сохраните эту шпаргалку для быстрого доступа! 📌**
