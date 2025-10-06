"""
Скрипт для проверки готовности бота к запуску
"""
import os
import sys


def print_header(text):
    """Печать заголовка"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")


def print_step(number, text, status=None):
    """Печать шага"""
    if status is None:
        print(f"\n{number}. {text}")
    elif status:
        print(f"   ✅ {text}")
    else:
        print(f"   ❌ {text}")


def check_python_version():
    """Проверка версии Python"""
    print_step(1, "Проверка версии Python")
    
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print_step("", f"Python {version.major}.{version.minor}.{version.micro}", True)
        return True
    else:
        print_step("", f"Python {version.major}.{version.minor}.{version.micro} (требуется 3.8+)", False)
        return False


def check_dependencies():
    """Проверка установленных зависимостей"""
    print_step(2, "Проверка зависимостей")
    
    required = {
        'telegram': 'python-telegram-bot',
        'dotenv': 'python-dotenv'
    }
    
    all_installed = True
    
    for module, package in required.items():
        try:
            __import__(module)
            print_step("", f"{package} установлен", True)
        except ImportError:
            print_step("", f"{package} НЕ установлен", False)
            all_installed = False
    
    if not all_installed:
        print("\n   💡 Установите зависимости: pip install -r requirements.txt")
    
    return all_installed


def check_env_file():
    """Проверка наличия .env файла"""
    print_step(3, "Проверка файла .env")
    
    if os.path.exists('.env'):
        print_step("", "Файл .env существует", True)
        return True
    else:
        print_step("", "Файл .env НЕ найден", False)
        print("\n   💡 Скопируйте .env.example в .env и заполните данные")
        return False


def check_config():
    """Проверка конфигурации"""
    print_step(4, "Проверка конфигурации")
    
    try:
        from config import Config
        config = Config()
        
        checks = {
            'BOT_TOKEN': bool(config.BOT_TOKEN),
            'CHANNEL_ID': bool(config.CHANNEL_ID),
            'PHONE_NUMBER': config.PHONE_NUMBER != '+1234567890',
            'OWNER_ID': config.OWNER_ID != 0
        }
        
        all_ok = True
        for key, value in checks.items():
            if value:
                print_step("", f"{key} установлен", True)
            else:
                print_step("", f"{key} НЕ установлен или некорректен", False)
                all_ok = False
        
        if not all_ok:
            print("\n   💡 Заполните все поля в файле .env")
        
        return all_ok
        
    except Exception as e:
        print_step("", f"Ошибка при загрузке конфигурации: {e}", False)
        return False


def check_files():
    """Проверка наличия необходимых файлов"""
    print_step(5, "Проверка файлов проекта")
    
    required_files = [
        'bot.py',
        'config.py',
        'storage.py',
        'requirements.txt'
    ]
    
    all_exist = True
    for file in required_files:
        if os.path.exists(file):
            print_step("", f"{file} найден", True)
        else:
            print_step("", f"{file} НЕ найден", False)
            all_exist = False
    
    return all_exist


def check_bot_connection():
    """Проверка подключения к Telegram"""
    print_step(6, "Проверка подключения к Telegram")
    
    try:
        import asyncio
        from telegram import Bot
        from config import Config
        
        config = Config()
        
        if not config.BOT_TOKEN:
            print_step("", "BOT_TOKEN не установлен, пропускаем проверку", False)
            return False
        
        async def test_connection():
            bot = Bot(token=config.BOT_TOKEN)
            me = await bot.get_me()
            return me
        
        me = asyncio.run(test_connection())
        print_step("", f"Подключение успешно! Бот: @{me.username}", True)
        return True
        
    except Exception as e:
        print_step("", f"Ошибка подключения: {str(e)[:50]}...", False)
        print("\n   💡 Проверьте правильность BOT_TOKEN в .env")
        return False


def check_channel_access():
    """Проверка доступа к каналу"""
    print_step(7, "Проверка доступа к каналу")
    
    try:
        import asyncio
        from telegram import Bot
        from config import Config
        
        config = Config()
        
        if not config.BOT_TOKEN or not config.CHANNEL_ID:
            print_step("", "BOT_TOKEN или CHANNEL_ID не установлены", False)
            return False
        
        async def test_channel():
            bot = Bot(token=config.BOT_TOKEN)
            chat = await bot.get_chat(config.CHANNEL_ID)
            return chat
        
        chat = asyncio.run(test_channel())
        print_step("", f"Доступ к каналу есть! Канал: {chat.title}", True)
        return True
        
    except Exception as e:
        print_step("", f"Нет доступа к каналу: {str(e)[:50]}...", False)
        print("\n   💡 Убедитесь, что:")
        print("      - Бот добавлен в канал как администратор")
        print("      - CHANNEL_ID указан правильно (начинается с -100)")
        return False


def print_summary(results):
    """Печать итогов"""
    print_header("ИТОГИ ПРОВЕРКИ")
    
    total = len(results)
    passed = sum(results.values())
    
    print(f"Пройдено проверок: {passed}/{total}\n")
    
    if passed == total:
        print("🎉 ВСЕ ПРОВЕРКИ ПРОЙДЕНЫ!")
        print("\n✅ Бот готов к запуску!")
        print("\n📝 Для запуска выполните: python bot.py")
    else:
        print("⚠️ НЕКОТОРЫЕ ПРОВЕРКИ НЕ ПРОЙДЕНЫ")
        print("\nНе пройдены:")
        for name, status in results.items():
            if not status:
                print(f"   ❌ {name}")
        
        print("\n📚 Для помощи откройте:")
        print("   - START_HERE.md - Быстрый старт")
        print("   - QUICKSTART.md - Подробная инструкция")
        print("   - README.md - Полная документация")


def main():
    """Главная функция"""
    print_header("ПРОВЕРКА ГОТОВНОСТИ TELEGRAM БОТА")
    
    results = {}
    
    # Выполняем все проверки
    results['Python 3.8+'] = check_python_version()
    results['Зависимости'] = check_dependencies()
    results['Файл .env'] = check_env_file()
    results['Конфигурация'] = check_config()
    results['Файлы проекта'] = check_files()
    results['Подключение к Telegram'] = check_bot_connection()
    results['Доступ к каналу'] = check_channel_access()
    
    # Печатаем итоги
    print_summary(results)
    
    print("\n" + "="*60 + "\n")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Проверка прервана пользователем")
    except Exception as e:
        print(f"\n\n❌ Критическая ошибка: {e}")