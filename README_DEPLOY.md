# 🤖 Telegram Menu Bot

Telegram бот для публикации меню в канале с возможностью заказа через WhatsApp.

## ✨ Возможности

- 📋 Публикация меню дня в канале
- 🖼️ Поддержка фото меню
- ✏️ Редактирование опубликованного меню
- 📱 Кнопка заказа через WhatsApp
- 🔐 Защита от несанкционированного доступа
- 🔄 Автоматическое обновление меню в канале

## 🚀 Быстрый старт

### Локальный запуск

1. **Клонируйте репозиторий:**

```bash
git clone https://github.com/YOUR_USERNAME/telegram-menu-bot.git
cd telegram-menu-bot
```

2. **Установите зависимости:**

```bash
pip install -r requirements.txt
```

3. **Настройте .env файл:**

```bash
cp .env.example .env
nano .env
```

4. **Запустите бота:**

```bash
python bot.py
```

### Деплой на сервер

📖 **Полная инструкция:** [VULTR_DEPLOY.md](VULTR_DEPLOY.md)

**Быстрый деплой на Ubuntu/Debian:**

```bash
# На сервере
git clone https://github.com/YOUR_USERNAME/telegram-menu-bot.git telegram-bot
cd telegram-bot
chmod +x deploy.sh
./deploy.sh
```

## 📋 Требования

- Python 3.8+
- python-telegram-bot 20.7+
- python-dotenv 1.0.0+

## ⚙️ Конфигурация

Создайте `.env` файл:

```env
BOT_TOKEN=your_bot_token
CHANNEL_ID=-1001234567890
PHONE_NUMBER=+1234567890
OWNER_ID=123456789
STORAGE_FILE=data.json
```

### Получение данных:

- **BOT_TOKEN**: [@BotFather](https://t.me/BotFather)
- **CHANNEL_ID**: [@userinfobot](https://t.me/userinfobot) (перешлите сообщение из канала)
- **OWNER_ID**: [@userinfobot](https://t.me/userinfobot) (отправьте /start)
- **PHONE_NUMBER**: Ваш номер WhatsApp в формате +1234567890

## 📝 Команды бота

### Для владельца:

- `/start` - Информация о боте
- `/publish_menu` - Опубликовать меню (отправьте текст или фото)
- `/edit_menu` - Редактировать опубликованное меню
- `/edit_text` - Изменить текст меню
- `/edit_photo` - Изменить фото меню
- `/remove_photo` - Удалить фото из меню
- `/cancel` - Отменить редактирование
- `/enable_menu_button` - Включить кнопку "Меню на сегодня"

### Для пользователей:

- Кнопка "📋 Меню на сегодня" - Получить текущее меню
- Кнопка "📱 Заказать через WhatsApp" - Открыть WhatsApp для заказа

## 🔄 Обновление бота

### На сервере:

```bash
cd ~/telegram-bot
./update.sh
```

Скрипт автоматически:

- Создаст бэкап данных
- Скачает обновления
- Обновит зависимости
- Перезапустит бота

## 📊 Управление на сервере

```bash
# Статус
sudo systemctl status telegram-bot

# Логи
sudo journalctl -u telegram-bot -f

# Перезапуск
sudo systemctl restart telegram-bot

# Остановка
sudo systemctl stop telegram-bot
```

## 🔒 Безопасность

- ✅ Не публикуйте `.env` файл
- ✅ Используйте приватный репозиторий для конфиденциальных данных
- ✅ Регулярно обновляйте зависимости
- ✅ Делайте бэкапы `data.json`

## 📖 Документация

- [VULTR_DEPLOY.md](VULTR_DEPLOY.md) - Полная инструкция по деплою на Vultr
- [DEPLOY.md](DEPLOY.md) - Деплой на различные платформы
- [QUICKSTART.md](QUICKSTART.md) - Быстрый старт
- [EXAMPLES.md](EXAMPLES.md) - Примеры использования

## 🐛 Решение проблем

### Бот не запускается

```bash
# Проверьте конфигурацию
python check_config.py

# Проверьте логи
sudo journalctl -u telegram-bot -n 50
```

### Бот не отвечает

```bash
# Перезапустите бота
sudo systemctl restart telegram-bot

# Проверьте статус
sudo systemctl status telegram-bot
```

## 📞 Поддержка

Если у вас возникли проблемы:

1. Проверьте [VULTR_DEPLOY.md](VULTR_DEPLOY.md) - раздел "Решение проблем"
2. Проверьте логи: `sudo journalctl -u telegram-bot -f`
3. Создайте Issue в репозитории

## 📄 Лицензия

MIT License - см. [LICENSE](LICENSE)

---

**Сделано с ❤️ для управления меню в Telegram**
