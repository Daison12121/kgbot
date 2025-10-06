# ✅ Чеклист деплоя на Vultr

Используйте этот чеклист для пошагового деплоя бота.

---

## 📋 Подготовка (на вашем компьютере)

### ✅ Шаг 1: Проверка файлов проекта

- [ ] Все файлы проекта на месте
- [ ] `.env.example` содержит все необходимые переменные
- [ ] `requirements.txt` содержит все зависимости
- [ ] `.gitignore` настроен (не загружает .env и data.json)
- [ ] `deploy.sh` и `update.sh` созданы

### ✅ Шаг 2: Создание Git репозитория

- [ ] Зарегистрирован аккаунт на GitHub
- [ ] Создан **приватный** репозиторий `telegram-menu-bot`
- [ ] Инициализирован Git в проекте: `git init`
- [ ] Добавлены файлы: `git add .`
- [ ] Создан коммит: `git commit -m "Initial commit"`
- [ ] Добавлен remote: `git remote add origin https://github.com/YOUR_USERNAME/telegram-menu-bot.git`
- [ ] Код загружен: `git push -u origin main`

**Команды для копирования:**

```powershell
cd "c:\Users\dasta\OneDrive\Документы\Telegram"
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/telegram-menu-bot.git
git branch -M main
git push -u origin main
```

---

## 🖥️ Создание сервера на Vultr

### ✅ Шаг 3: Регистрация и настройка

- [ ] Зарегистрирован аккаунт на [vultr.com](https://www.vultr.com/)
- [ ] Пополнен баланс (минимум $10)
- [ ] Нажато "Deploy New Server"

### ✅ Шаг 4: Настройка сервера

- [ ] Выбрано: **Cloud Compute**
- [ ] Регион: **Frankfurt** (или ближайший)
- [ ] ОС: **Ubuntu 22.04 LTS x64**
- [ ] План: **$5/month** (1GB RAM, 25GB SSD)
- [ ] (Опционально) Включены Auto Backups
- [ ] Hostname: `telegram-bot`
- [ ] Нажато "Deploy Now"

### ✅ Шаг 5: Сохранение данных

- [ ] **IP адрес сервера записан:** `_________________`
- [ ] **Пароль root записан:** `_________________`
- [ ] Сервер в статусе "Running"

---

## 🔐 Подключение к серверу

### ✅ Шаг 6: SSH подключение

- [ ] Открыт PowerShell/Terminal
- [ ] Выполнено: `ssh root@YOUR_SERVER_IP`
- [ ] Введен пароль root
- [ ] Подключение успешно

**Команда:**

```powershell
ssh root@YOUR_SERVER_IP
```

### ✅ Шаг 7: Смена пароля (рекомендуется)

- [ ] Выполнено: `passwd`
- [ ] Введен новый пароль
- [ ] Новый пароль записан: `_________________`

---

## 📦 Установка бота на сервер

### ✅ Шаг 8: Установка Git

```bash
apt update && apt install -y git
```

- [ ] Git установлен

### ✅ Шаг 9: Клонирование репозитория

```bash
cd ~
git clone https://github.com/YOUR_USERNAME/telegram-menu-bot.git telegram-bot
cd telegram-bot
```

**Если репозиторий приватный:**

```bash
# Используйте Personal Access Token
git clone https://YOUR_TOKEN@github.com/YOUR_USERNAME/telegram-menu-bot.git telegram-bot
```

- [ ] Репозиторий склонирован
- [ ] Перешли в директорию `telegram-bot`

### ✅ Шаг 10: Запуск автоматической установки

```bash
chmod +x deploy.sh
./deploy.sh
```

- [ ] Скрипт запущен
- [ ] Система обновлена
- [ ] Python установлен
- [ ] Виртуальное окружение создано
- [ ] Зависимости установлены
- [ ] Файл .env создан
- [ ] Systemd service настроен

---

## ⚙️ Настройка бота

### ✅ Шаг 11: Редактирование .env

```bash
nano .env
```

**Вставьте ваши данные:**

```env
BOT_TOKEN=8434304055:AAHbnCxsM1OP0fWzHkX400zetb4aq11n6mI
CHANNEL_ID=-1002947483367
PHONE_NUMBER=+77078958827
OWNER_ID=7737197594
STORAGE_FILE=data.json
```

**Сохранение:** `Ctrl+O` → `Enter` → `Ctrl+X`

- [ ] Файл .env отредактирован
- [ ] Все данные заполнены
- [ ] Файл сохранен

### ✅ Шаг 12: Проверка конфигурации

```bash
source venv/bin/activate
python check_config.py
```

- [ ] Конфигурация проверена
- [ ] Все параметры корректны
- [ ] Нет ошибок

---

## 🚀 Запуск бота

### ✅ Шаг 13: Запуск и проверка

```bash
# Запуск
sudo systemctl start telegram-bot

# Проверка статуса
sudo systemctl status telegram-bot

# Просмотр логов
sudo journalctl -u telegram-bot -f
```

- [ ] Бот запущен
- [ ] Статус: **active (running)**
- [ ] В логах: "✅ Бот успешно запущен!"
- [ ] В логах: "✅ Бот подключен к Telegram"

### ✅ Шаг 14: Проверка работы в Telegram

- [ ] Открыт Telegram
- [ ] Найден бот по username
- [ ] Отправлено `/start`
- [ ] Бот ответил
- [ ] Команда `/enable_menu_button` работает
- [ ] Кнопка "📋 Меню на сегодня" появилась

---

## 🔒 Безопасность (опционально, но рекомендуется)

### ✅ Шаг 15: Настройка firewall

```bash
sudo apt install -y ufw
sudo ufw allow ssh
sudo ufw enable
sudo ufw status
```

- [ ] UFW установлен
- [ ] SSH разрешен
- [ ] Firewall включен

### ✅ Шаг 16: Создание нового пользователя (вместо root)

```bash
adduser botuser
usermod -aG sudo botuser
```

- [ ] Пользователь создан
- [ ] Добавлен в sudo группу
- [ ] Пароль записан: `_________________`

---

## 🔄 Настройка автоматического обновления

### ✅ Шаг 17: Проверка скрипта обновления

```bash
chmod +x update.sh
```

- [ ] Скрипт `update.sh` исполняемый

### ✅ Шаг 18: Тест обновления

**На вашем компьютере:**

```powershell
cd "c:\Users\dasta\OneDrive\Документы\Telegram"
# Внесите небольшое изменение (например, в README)
git add .
git commit -m "Test update"
git push
```

**На сервере:**

```bash
cd ~/telegram-bot
./update.sh
```

- [ ] Обновление скачано
- [ ] Бот перезапущен
- [ ] Изменения применены

---

## 💾 Резервное копирование

### ✅ Шаг 19: Настройка автоматического бэкапа

```bash
mkdir -p ~/telegram-bot/backups
crontab -e
```

**Добавьте строку:**

```
0 3 * * * cp ~/telegram-bot/data.json ~/telegram-bot/backups/data.json.$(date +\%Y\%m\%d)
```

- [ ] Директория backups создана
- [ ] Cron задача добавлена
- [ ] Бэкап будет создаваться каждый день в 3:00

---

## 📊 Финальная проверка

### ✅ Шаг 20: Проверка всех функций

- [ ] Бот отвечает на команды
- [ ] `/publish_menu` работает (текст)
- [ ] `/publish_menu` работает (фото)
- [ ] `/edit_menu` работает
- [ ] `/edit_text` работает
- [ ] `/edit_photo` работает
- [ ] `/remove_photo` работает
- [ ] Кнопка "Меню на сегодня" работает
- [ ] Кнопка "Заказать через WhatsApp" работает
- [ ] Меню публикуется в канале
- [ ] Редактирование обновляет меню в канале

### ✅ Шаг 21: Проверка автозапуска

```bash
# Перезагрузка сервера
sudo reboot
```

**После перезагрузки (через 1-2 минуты):**

```bash
ssh root@YOUR_SERVER_IP
sudo systemctl status telegram-bot
```

- [ ] Сервер перезагружен
- [ ] Бот запустился автоматически
- [ ] Статус: **active (running)**

---

## 🎉 Готово!

### ✅ Финальный чеклист

- [ ] Бот работает 24/7
- [ ] Автозапуск настроен
- [ ] Автоматическое обновление работает
- [ ] Резервное копирование настроено
- [ ] Firewall настроен
- [ ] Все команды работают
- [ ] Меню публикуется в канале

---

## 📝 Полезные команды для ежедневного использования

### Просмотр логов

```bash
sudo journalctl -u telegram-bot -f
```

### Перезапуск бота

```bash
sudo systemctl restart telegram-bot
```

### Обновление бота

```bash
cd ~/telegram-bot
./update.sh
```

### Проверка статуса

```bash
sudo systemctl status telegram-bot
```

### Ручной бэкап

```bash
cp ~/telegram-bot/data.json ~/telegram-bot/data.json.backup.$(date +%Y%m%d)
```

---

## 🆘 Если что-то пошло не так

### Бот не запускается

```bash
sudo journalctl -u telegram-bot -n 50
```

### Проверка конфигурации

```bash
cd ~/telegram-bot
source venv/bin/activate
python check_config.py
```

### Полная переустановка

```bash
cd ~
rm -rf telegram-bot
git clone https://github.com/YOUR_USERNAME/telegram-menu-bot.git telegram-bot
cd telegram-bot
./deploy.sh
# Затем настройте .env и запустите бота
```

---

## 📞 Документация

- 📖 [VULTR_DEPLOY.md](VULTR_DEPLOY.md) - Подробная инструкция
- ⚡ [QUICK_DEPLOY.md](QUICK_DEPLOY.md) - Быстрый деплой
- 📚 [README_DEPLOY.md](README_DEPLOY.md) - Общая информация

---

**🎊 Поздравляем! Ваш бот успешно задеплоен и работает!**

**Дата деплоя:** `_______________`  
**IP сервера:** `_______________`  
**GitHub репозиторий:** `_______________`
