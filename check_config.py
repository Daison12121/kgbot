"""
Скрипт для проверки конфигурации бота
"""
import os
from config import Config


def check_config():
    """Проверка конфигурации"""
    print("🔍 Проверка конфигурации...\n")
    
    config = Config()
    errors = []
    warnings = []
    
    # Проверка BOT_TOKEN
    if not config.BOT_TOKEN:
        errors.append("❌ BOT_TOKEN не установлен")
    elif len(config.BOT_TOKEN) < 40:
        warnings.append("⚠️ BOT_TOKEN выглядит некорректно (слишком короткий)")
    else:
        print(f"✅ BOT_TOKEN: {config.BOT_TOKEN[:10]}...{config.BOT_TOKEN[-10:]}")
    
    # Проверка CHANNEL_ID
    if not config.CHANNEL_ID:
        errors.append("❌ CHANNEL_ID не установлен")
    elif config.CHANNEL_ID.startswith('@'):
        print(f"✅ CHANNEL_ID: {config.CHANNEL_ID}")
    elif config.CHANNEL_ID.startswith('-100'):
        print(f"✅ CHANNEL_ID: {config.CHANNEL_ID}")
    else:
        warnings.append(f"⚠️ CHANNEL_ID выглядит некорректно: {config.CHANNEL_ID}")
        warnings.append("   ID канала должен начинаться с -100 или @")
    
    # Проверка PHONE_NUMBER
    if not config.PHONE_NUMBER or config.PHONE_NUMBER == '+1234567890':
        warnings.append("⚠️ PHONE_NUMBER не изменен (используется значение по умолчанию)")
    else:
        print(f"✅ PHONE_NUMBER: {config.PHONE_NUMBER}")
    
    # Проверка OWNER_ID
    if not config.OWNER_ID or config.OWNER_ID == 0:
        errors.append("❌ OWNER_ID не установлен")
    else:
        print(f"✅ OWNER_ID: {config.OWNER_ID}")
    
    # Проверка файла хранилища
    if os.path.exists(config.STORAGE_FILE):
        print(f"✅ Файл хранилища существует: {config.STORAGE_FILE}")
    else:
        print(f"ℹ️ Файл хранилища будет создан при первом запуске: {config.STORAGE_FILE}")
    
    print("\n" + "="*50 + "\n")
    
    # Вывод предупреждений
    if warnings:
        print("⚠️ ПРЕДУПРЕЖДЕНИЯ:\n")
        for warning in warnings:
            print(warning)
        print()
    
    # Вывод ошибок
    if errors:
        print("❌ ОШИБКИ:\n")
        for error in errors:
            print(error)
        print("\n❌ Конфигурация содержит ошибки! Исправьте их в файле .env")
        return False
    
    if not warnings:
        print("✅ Конфигурация корректна! Можно запускать бота.")
    else:
        print("⚠️ Конфигурация содержит предупреждения, но бот может работать.")
    
    print("\n📝 Для запуска бота выполните: python bot.py")
    return True


if __name__ == '__main__':
    try:
        check_config()
    except Exception as e:
        print(f"\n❌ Ошибка при проверке конфигурации: {e}")
        print("\nУбедитесь, что файл .env существует и заполнен корректно.")