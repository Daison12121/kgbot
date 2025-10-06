#!/bin/bash

# Скрипт для автоматического обновления бота

set -e

echo "🔄 Обновление Telegram бота..."

# Цвета для вывода
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

BOT_DIR="$HOME/telegram-bot"

# Проверка существования директории
if [ ! -d "$BOT_DIR" ]; then
    echo -e "${RED}❌ Директория $BOT_DIR не найдена!${NC}"
    exit 1
fi

cd "$BOT_DIR"

# Проверка наличия Git репозитория
if [ ! -d ".git" ]; then
    echo -e "${RED}❌ Git репозиторий не найден!${NC}"
    exit 1
fi

# Создание бэкапа data.json
if [ -f "data.json" ]; then
    BACKUP_FILE="data.json.backup.$(date +%Y%m%d_%H%M%S)"
    echo -e "${YELLOW}💾 Создание бэкапа: $BACKUP_FILE${NC}"
    cp data.json "$BACKUP_FILE"
    echo -e "${GREEN}✅ Бэкап создан${NC}"
fi

# Получение обновлений из Git
echo -e "${YELLOW}📥 Получение обновлений из Git...${NC}"
git fetch origin

# Проверка наличия обновлений
LOCAL=$(git rev-parse @)
REMOTE=$(git rev-parse @{u})

if [ "$LOCAL" = "$REMOTE" ]; then
    echo -e "${GREEN}✅ Бот уже обновлен до последней версии${NC}"
    exit 0
fi

echo -e "${YELLOW}🔄 Найдены обновления, применяем...${NC}"

# Остановка бота
echo -e "${YELLOW}⏸️  Остановка бота...${NC}"
sudo systemctl stop telegram-bot

# Применение обновлений
git pull origin main

# Активация виртуального окружения
source venv/bin/activate

# Обновление зависимостей
if [ -f "requirements.txt" ]; then
    echo -e "${YELLOW}📦 Обновление зависимостей...${NC}"
    pip install --upgrade pip
    pip install -r requirements.txt
    echo -e "${GREEN}✅ Зависимости обновлены${NC}"
fi

# Запуск бота
echo -e "${YELLOW}▶️  Запуск бота...${NC}"
sudo systemctl start telegram-bot

# Проверка статуса
sleep 2
if sudo systemctl is-active --quiet telegram-bot; then
    echo -e "${GREEN}✅ Бот успешно обновлен и запущен!${NC}"
    echo ""
    echo -e "${YELLOW}📊 Статус бота:${NC}"
    sudo systemctl status telegram-bot --no-pager -l
else
    echo -e "${RED}❌ Ошибка при запуске бота!${NC}"
    echo -e "${YELLOW}Просмотрите логи: sudo journalctl -u telegram-bot -n 50${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}✅ Обновление завершено!${NC}"
echo -e "${YELLOW}📝 Просмотр логов: sudo journalctl -u telegram-bot -f${NC}"