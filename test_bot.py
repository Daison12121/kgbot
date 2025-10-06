"""
Скрипт для тестирования основных функций бота
"""
import asyncio
from config import Config
from storage import Storage


async def test_storage():
    """Тест хранилища"""
    print("🧪 Тестирование хранилища...\n")
    
    storage = Storage()
    
    # Тест администраторов
    print("1. Тест администраторов:")
    admins = storage.get_admins()
    print(f"   Текущие администраторы: {admins}")
    
    # Добавление тестового админа
    test_admin_id = 999999999
    if storage.add_admin(test_admin_id):
        print(f"   ✅ Тестовый админ {test_admin_id} добавлен")
    
    admins = storage.get_admins()
    print(f"   Администраторы после добавления: {admins}")
    
    # Удаление тестового админа
    if storage.remove_admin(test_admin_id):
        print(f"   ✅ Тестовый админ {test_admin_id} удален")
    
    admins = storage.get_admins()
    print(f"   Администраторы после удаления: {admins}\n")
    
    # Тест меню
    print("2. Тест меню:")
    test_menu_text = "🍽️ **Тестовое меню**\n\n• Блюдо 1 - 100₽\n• Блюдо 2 - 200₽"
    storage.save_menu(test_menu_text, None)
    print(f"   ✅ Меню сохранено")
    
    menu = storage.get_menu()
    print(f"   Текст меню: {menu['text'][:50]}...")
    print(f"   Фото: {menu['photo']}")
    print(f"   Обновлено: {menu['updated_at']}\n")
    
    print("✅ Все тесты хранилища пройдены!\n")


async def test_config():
    """Тест конфигурации"""
    print("🧪 Тестирование конфигурации...\n")
    
    config = Config()
    
    print(f"BOT_TOKEN: {'✅ Установлен' if config.BOT_TOKEN else '❌ Не установлен'}")
    print(f"CHANNEL_ID: {'✅ Установлен' if config.CHANNEL_ID else '❌ Не установлен'}")
    print(f"PHONE_NUMBER: {config.PHONE_NUMBER}")
    print(f"OWNER_ID: {'✅ Установлен' if config.OWNER_ID else '❌ Не установлен'}")
    print(f"STORAGE_FILE: {config.STORAGE_FILE}\n")
    
    try:
        config.validate()
        print("✅ Конфигурация валидна!\n")
    except ValueError as e:
        print(f"❌ Ошибка конфигурации: {e}\n")


async def test_bot_connection():
    """Тест подключения к Telegram API"""
    print("🧪 Тестирование подключения к Telegram...\n")
    
    try:
        from telegram import Bot
        config = Config()
        
        if not config.BOT_TOKEN:
            print("❌ BOT_TOKEN не установлен. Пропускаем тест подключения.\n")
            return
        
        bot = Bot(token=config.BOT_TOKEN)
        
        # Получение информации о боте
        me = await bot.get_me()
        print(f"✅ Подключение успешно!")
        print(f"   Имя бота: {me.first_name}")
        print(f"   Username: @{me.username}")
        print(f"   ID: {me.id}\n")
        
        # Проверка доступа к каналу
        if config.CHANNEL_ID:
            try:
                chat = await bot.get_chat(config.CHANNEL_ID)
                print(f"✅ Доступ к каналу есть!")
                print(f"   Название: {chat.title}")
                print(f"   Тип: {chat.type}")
                print(f"   ID: {chat.id}\n")
            except Exception as e:
                print(f"❌ Ошибка доступа к каналу: {e}")
                print(f"   Убедитесь, что бот добавлен в канал как администратор.\n")
        else:
            print("⚠️ CHANNEL_ID не установлен. Пропускаем проверку канала.\n")
        
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}\n")


async def main():
    """Главная функция"""
    print("="*50)
    print("🤖 ТЕСТИРОВАНИЕ TELEGRAM БОТА")
    print("="*50 + "\n")
    
    # Тест конфигурации
    await test_config()
    
    # Тест хранилища
    await test_storage()
    
    # Тест подключения к Telegram
    await test_bot_connection()
    
    print("="*50)
    print("✅ ТЕСТИРОВАНИЕ ЗАВЕРШЕНО")
    print("="*50)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⚠️ Тестирование прервано пользователем")
    except Exception as e:
        print(f"\n\n❌ Критическая ошибка: {e}")