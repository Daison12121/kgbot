# 🚀 Деплой бота на Vultr

Пошаговая инструкция по развертыванию Telegram бота на сервере Vultr.

---

## 📋 Что вам понадобится

- ✅ Аккаунт на [Vultr.com](https://www.vultr.com/)
- ✅ $5-10 на балансе (минимальный тариф ~$5/месяц)
- ✅ SSH клиент (встроен в Windows 10/11, macOS, Linux)
- ✅ Git репозиторий с вашим ботом (GitHub, GitLab, Bitbucket)

---

## 🖥️ Часть 1: Создание сервера на Vultr

### Шаг 1: Регистрация и пополнение баланса

1. Зарегистрируйтесь на [Vultr.com](https://www.vultr.com/)
2. Пополните баланс минимум на $10 (принимают карты, PayPal)

### Шаг 2: Создание сервера

1. Нажмите **"Deploy +"** → **"Deploy New Server"**

2. **Choose Server:**

   - Выберите **"Cloud Compute"**

3. **Server Location:**

   - Выберите ближайший к вам регион (например, Frankfurt для Европы)

4. **Server Type:**

   - Выберите **"Ubuntu 22.04 LTS x64"**

5. **Server Size:**

   - Выберите минимальный план: **$5/month** (1 CPU, 1GB RAM, 25GB SSD)
   - Этого достаточно для Telegram бота

6. **Additional Features:**

   - ✅ Включите **"Enable IPv6"** (опционально)
   - ✅ Включите **"Enable Auto Backups"** ($1/месяц, рекомендуется)

7. **Server Hostname & Label:**

   - Hostname: `telegram-bot`
   - Label: `Telegram Menu Bot`

8. Нажмите **"Deploy Now"**

### Шаг 3: Ожидание создания сервера

- Сервер создается 2-5 минут
- Статус изменится с "Installing" на "Running"
- Запишите **IP адрес** и **пароль root** (показывается один раз!)

---

## 🔐 Часть 2: Подключение к серверу

### Windows (PowerShell или CMD)

```powershell
ssh root@YOUR_SERVER_IP
```

### macOS / Linux (Terminal)

```bash
ssh root@YOUR_SERVER_IP
```

**При первом подключении:**

- Вопрос "Are you sure you want to continue connecting?" → введите `yes`
- Введите пароль root (скопируйте из панели Vultr)

**Смена пароля (рекомендуется):**

```bash
passwd
```

---

## 📦 Часть 3: Подготовка Git репозитория

### Вариант 1: GitHub (рекомендуется)

#### 3.1. Создание репозитория

1. Перейдите на [GitHub.com](https://github.com/)
2. Нажмите **"New repository"**
3. Название: `telegram-menu-bot`
4. Выберите **"Private"** (чтобы скрыть код)
5. Нажмите **"Create repository"**

#### 3.2. Загрузка кода (на вашем компьютере)

**Windows (PowerShell):**

```powershell
cd "c:\Users\dasta\OneDrive\Документы\Telegram"

# Инициализация Git (если еще не сделано)
git init

# Добавление всех файлов
git add .

# Первый коммит
git commit -m "Initial commit"

# Добавление remote (замените YOUR_USERNAME на ваш GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/telegram-menu-bot.git

# Отправка кода
git branch -M main
git push -u origin main
```

**Если Git просит авторизацию:**

- Username: ваш GitHub username
- Password: используйте **Personal Access Token** (не пароль!)
  - Создать токен: GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic) → Generate new token
  - Выберите scope: `repo`
  - Скопируйте токен и используйте вместо пароля

#### 3.3. Настройка SSH ключа (опционально, но удобнее)

**На вашем компьютере:**

```powershell
# Генерация SSH ключа
ssh-keygen -t ed25519 -C "your_email@example.com"

# Просмотр публичного ключа
cat ~/.ssh/id_ed25519.pub
```

**На GitHub:**

1. Settings → SSH and GPG keys → New SSH key
2. Вставьте содержимое `id_ed25519.pub`
3. Сохраните

**Теперь можно использовать SSH URL:**

```powershell
git remote set-url origin git@github.com:YOUR_USERNAME/telegram-menu-bot.git
```

---

## 🚀 Часть 4: Деплой бота на сервер

### Шаг 1: Клонирование репозитория на сервер

**На сервере (через SSH):**

```bash
# Установка Git
apt update
apt install -y git

# Клонирование репозитория
cd ~
git clone https://github.com/YOUR_USERNAME/telegram-menu-bot.git telegram-bot
cd telegram-bot
```

**Если репозиторий приватный:**

```bash
# Вариант 1: HTTPS (нужен Personal Access Token)
git clone https://YOUR_TOKEN@github.com/YOUR_USERNAME/telegram-menu-bot.git telegram-bot

# Вариант 2: SSH (нужен SSH ключ на сервере)
# Сгенерируйте ключ на сервере и добавьте в GitHub
ssh-keygen -t ed25519 -C "server@vultr"
cat ~/.ssh/id_ed25519.pub  # Добавьте в GitHub SSH keys
git clone git@github.com:YOUR_USERNAME/telegram-menu-bot.git telegram-bot
```

### Шаг 2: Запуск скрипта деплоя

```bash
cd ~/telegram-bot

# Сделать скрипт исполняемым
chmod +x deploy.sh

# Запустить деплой
./deploy.sh
```

**Скрипт автоматически:**

- ✅ Обновит систему
- ✅ Установит Python и зависимости
- ✅ Создаст виртуальное окружение
- ✅ Установит Python пакеты
- ✅ Создаст .env файл из .env.example
- ✅ Настроит systemd service
- ✅ Включит автозапуск

### Шаг 3: Настройка .env файла

```bash
nano .env
```

**Заполните данные:**

```env
BOT_TOKEN=8434304055:AAHbnCxsM1OP0fWzHkX400zetb4aq11n6mI
CHANNEL_ID=-1002947483367
PHONE_NUMBER=+77078958827
OWNER_ID=7737197594
STORAGE_FILE=data.json
```

**Сохранение:**

- `Ctrl+O` → `Enter` (сохранить)
- `Ctrl+X` (выйти)

### Шаг 4: Проверка конфигурации

```bash
source venv/bin/activate
python check_config.py
```

### Шаг 5: Запуск бота

```bash
# Запуск
sudo systemctl start telegram-bot

# Проверка статуса
sudo systemctl status telegram-bot

# Просмотр логов
sudo journalctl -u telegram-bot -f
```

**Если все ОК, вы увидите:**

```
✅ Бот успешно запущен!
✅ Бот подключен к Telegram
```

---

## 🔄 Часть 5: Обновление бота

### Когда вы внесли изменения в код:

**На вашем компьютере:**

```powershell
cd "c:\Users\dasta\OneDrive\Документы\Telegram"

# Добавить изменения
git add .

# Создать коммит
git commit -m "Описание изменений"

# Отправить на GitHub
git push
```

**На сервере:**

```bash
cd ~/telegram-bot

# Сделать скрипт исполняемым (только первый раз)
chmod +x update.sh

# Запустить обновление
./update.sh
```

**Скрипт автоматически:**

- ✅ Создаст бэкап data.json
- ✅ Остановит бота
- ✅ Скачает обновления из Git
- ✅ Обновит зависимости
- ✅ Запустит бота
- ✅ Проверит статус

---

## 📊 Управление ботом

### Основные команды

```bash
# Запуск
sudo systemctl start telegram-bot

# Остановка
sudo systemctl stop telegram-bot

# Перезапуск
sudo systemctl restart telegram-bot

# Статус
sudo systemctl status telegram-bot

# Логи (в реальном времени)
sudo journalctl -u telegram-bot -f

# Последние 100 строк логов
sudo journalctl -u telegram-bot -n 100

# Логи за сегодня
sudo journalctl -u telegram-bot --since today
```

### Автозапуск

```bash
# Включить автозапуск при перезагрузке
sudo systemctl enable telegram-bot

# Отключить автозапуск
sudo systemctl disable telegram-bot
```

---

## 🔒 Безопасность

### 1. Создание нового пользователя (вместо root)

```bash
# Создание пользователя
adduser botuser

# Добавление в sudo группу
usermod -aG sudo botuser

# Переключение на нового пользователя
su - botuser

# Теперь повторите деплой от имени botuser
```

### 2. Настройка firewall

```bash
# Установка UFW
sudo apt install -y ufw

# Разрешить SSH
sudo ufw allow ssh

# Включить firewall
sudo ufw enable

# Проверка
sudo ufw status
```

### 3. Отключение входа root по SSH (после создания нового пользователя)

```bash
sudo nano /etc/ssh/sshd_config
```

Найдите и измените:

```
PermitRootLogin no
```

Перезапустите SSH:

```bash
sudo systemctl restart sshd
```

---

## 💾 Резервное копирование

### Ручной бэкап

```bash
# Создание бэкапа
cp ~/telegram-bot/data.json ~/telegram-bot/data.json.backup.$(date +%Y%m%d)

# Скачивание бэкапа на локальный компьютер
scp root@YOUR_SERVER_IP:~/telegram-bot/data.json ./data.json.backup
```

### Автоматический бэкап (cron)

```bash
# Открыть crontab
crontab -e

# Добавить строку (бэкап каждый день в 3:00)
0 3 * * * cp ~/telegram-bot/data.json ~/telegram-bot/backups/data.json.$(date +\%Y\%m\%d)
```

---

## 🐛 Решение проблем

### Бот не запускается

```bash
# Проверка логов
sudo journalctl -u telegram-bot -n 50

# Проверка конфигурации
cd ~/telegram-bot
source venv/bin/activate
python check_config.py

# Проверка прав доступа
ls -la ~/telegram-bot/
```

### Бот не отвечает

```bash
# Проверка статуса
sudo systemctl status telegram-bot

# Перезапуск
sudo systemctl restart telegram-bot

# Проверка интернет-соединения
ping -c 4 api.telegram.org
```

### Ошибка "Permission denied"

```bash
# Исправление прав доступа
cd ~/telegram-bot
chmod +x deploy.sh update.sh
```

### Git ошибки

```bash
# Сброс локальных изменений
git reset --hard origin/main

# Принудительное обновление
git fetch --all
git reset --hard origin/main
```

---

## 📞 Полезные ссылки

- 📖 [Документация Vultr](https://www.vultr.com/docs/)
- 🐙 [GitHub Docs](https://docs.github.com/)
- 🤖 [Telegram Bot API](https://core.telegram.org/bots/api)
- 🐍 [Python Telegram Bot](https://python-telegram-bot.org/)

---

## ✅ Чеклист деплоя

- [ ] Создан сервер на Vultr
- [ ] Подключение по SSH работает
- [ ] Создан Git репозиторий
- [ ] Код загружен в репозиторий
- [ ] Репозиторий склонирован на сервер
- [ ] Запущен скрипт deploy.sh
- [ ] Настроен .env файл
- [ ] Бот запущен и работает
- [ ] Проверена работа команд
- [ ] Настроен автозапуск
- [ ] Создан скрипт обновления
- [ ] Настроен firewall
- [ ] Настроено резервное копирование

---

**🎉 Поздравляем! Ваш бот работает 24/7 на сервере Vultr!**
