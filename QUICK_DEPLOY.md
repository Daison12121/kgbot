# ⚡ Быстрый деплой на Vultr

## 🎯 За 10 минут от нуля до работающего бота

---

## 1️⃣ Создайте сервер на Vultr (3 минуты)

1. Зайдите на [vultr.com](https://www.vultr.com/) → Deploy New Server
2. Выберите:
   - **Cloud Compute**
   - **Location**: Frankfurt (или ближайший)
   - **Ubuntu 22.04 LTS**
   - **Plan**: $5/month (1GB RAM)
3. Deploy Now
4. **Сохраните IP адрес и пароль!**

---

## 2️⃣ Загрузите код на GitHub (2 минуты)

**На вашем компьютере (PowerShell):**

```powershell
cd "c:\Users\dasta\OneDrive\Документы\Telegram"

# Инициализация Git
git init
git add .
git commit -m "Initial commit"

# Создайте репозиторий на github.com (Private!)
# Затем:
git remote add origin https://github.com/YOUR_USERNAME/telegram-menu-bot.git
git branch -M main
git push -u origin main
```

---

## 3️⃣ Подключитесь к серверу (1 минута)

```powershell
ssh root@YOUR_SERVER_IP
# Введите пароль из Vultr
```

---

## 4️⃣ Установите бота (3 минуты)

**На сервере:**

```bash
# Установка Git
apt update && apt install -y git

# Клонирование репозитория
git clone https://github.com/YOUR_USERNAME/telegram-menu-bot.git telegram-bot
cd telegram-bot

# Запуск автоматической установки
chmod +x deploy.sh
./deploy.sh
```

---

## 5️⃣ Настройте .env (1 минута)

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

**Сохраните:** `Ctrl+O` → `Enter` → `Ctrl+X`

---

## 6️⃣ Запустите бота (30 секунд)

```bash
# Запуск
sudo systemctl start telegram-bot

# Проверка
sudo systemctl status telegram-bot
```

**Готово! 🎉**

---

## 🔄 Обновление бота

**На вашем компьютере (после изменений):**

```powershell
git add .
git commit -m "Update"
git push
```

**На сервере:**

```bash
cd ~/telegram-bot
./update.sh
```

---

## 📊 Полезные команды

```bash
# Логи в реальном времени
sudo journalctl -u telegram-bot -f

# Перезапуск
sudo systemctl restart telegram-bot

# Остановка
sudo systemctl stop telegram-bot

# Статус
sudo systemctl status telegram-bot
```

---

## 🆘 Проблемы?

### Бот не запускается

```bash
sudo journalctl -u telegram-bot -n 50
```

### Забыли пароль от сервера

- Зайдите в панель Vultr → Server → Settings → Reset Root Password

### Git просит пароль

- Используйте Personal Access Token вместо пароля
- GitHub → Settings → Developer settings → Personal access tokens

---

## 📖 Подробная инструкция

Если нужны детали: [VULTR_DEPLOY.md](VULTR_DEPLOY.md)

---

**Всё! Ваш бот работает 24/7! 🚀**
