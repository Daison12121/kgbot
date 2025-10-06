#!/bin/bash

# Скрипт для первоначального деплоя бота на сервер

set -e

echo "🚀 Начинаем деплой Telegram бота..."

# Цвета для вывода
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Проверка, что скрипт запущен не от root
if [ "$EUID" -eq 0 ]; then 
    echo -e "${RED}❌ Не запускайте этот скрипт от root!${NC}"
    exit 1
fi

# Обновление системы
echo -e "${YELLOW}📦 Обновление системы...${NC}"
sudo apt update && sudo apt upgrade -y

# Установка зависимостей
echo -e "${YELLOW}📦 Установка зависимостей...${NC}"
sudo apt install -y python3 python3-pip python3-venv git

# Создание директории для бота
BOT_DIR="$HOME/telegram-bot"
echo -e "${YELLOW}📁 Создание директории $BOT_DIR...${NC}"
mkdir -p "$BOT_DIR"
cd "$BOT_DIR"

# Проверка наличия Git репозитория
if [ ! -d ".git" ]; then
    echo -e "${YELLOW}📥 Инициализация Git репозитория...${NC}"
    git init
    echo -e "${GREEN}✅ Git репозиторий инициализирован${NC}"
    echo -e "${YELLOW}⚠️  Не забудьте добавить remote: git remote add origin YOUR_REPO_URL${NC}"
fi

# Создание виртуального окружения
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}🐍 Создание виртуального окружения...${NC}"
    python3 -m venv venv
    echo -e "${GREEN}✅ Виртуальное окружение создано${NC}"
fi

# Активация виртуального окружения
echo -e "${YELLOW}🔄 Активация виртуального окружения...${NC}"
source venv/bin/activate

# Установка зависимостей Python
if [ -f "requirements.txt" ]; then
    echo -e "${YELLOW}📦 Установка Python зависимостей...${NC}"
    pip install --upgrade pip
    pip install -r requirements.txt
    echo -e "${GREEN}✅ Зависимости установлены${NC}"
else
    echo -e "${RED}❌ Файл requirements.txt не найден!${NC}"
    exit 1
fi

# Проверка наличия .env файла
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚙️  Создание .env файла...${NC}"
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo -e "${GREEN}✅ Файл .env создан из .env.example${NC}"
        echo -e "${RED}⚠️  ВАЖНО: Отредактируйте .env файл и добавьте ваши данные!${NC}"
        echo -e "${YELLOW}Используйте: nano .env${NC}"
    else
        echo -e "${RED}❌ Файл .env.example не найден!${NC}"
        exit 1
    fi
fi

# Создание systemd service файла
SERVICE_FILE="/etc/systemd/system/telegram-bot.service"
echo -e "${YELLOW}⚙️  Настройка systemd service...${NC}"

# Замена YOUR_USERNAME на текущего пользователя
CURRENT_USER=$(whoami)
sed "s/YOUR_USERNAME/$CURRENT_USER/g" telegram-bot.service > /tmp/telegram-bot.service

sudo cp /tmp/telegram-bot.service "$SERVICE_FILE"
sudo systemctl daemon-reload
echo -e "${GREEN}✅ Systemd service настроен${NC}"

# Включение автозапуска
echo -e "${YELLOW}🔄 Включение автозапуска...${NC}"
sudo systemctl enable telegram-bot
echo -e "${GREEN}✅ Автозапуск включен${NC}"

echo ""
echo -e "${GREEN}✅ Деплой завершен!${NC}"
echo ""
echo -e "${YELLOW}📝 Следующие шаги:${NC}"
echo "1. Отредактируйте .env файл: nano $BOT_DIR/.env"
echo "2. Проверьте конфигурацию: python check_config.py"
echo "3. Запустите бота: sudo systemctl start telegram-bot"
echo "4. Проверьте статус: sudo systemctl status telegram-bot"
echo "5. Просмотр логов: sudo journalctl -u telegram-bot -f"
echo ""
echo -e "${YELLOW}🔄 Для автоматического обновления используйте: ./update.sh${NC}"