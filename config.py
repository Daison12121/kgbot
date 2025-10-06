"""
Конфигурация бота
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Класс конфигурации"""
    
    # Токен бота (получить у @BotFather)
    BOT_TOKEN = os.getenv('BOT_TOKEN', '')
    
    # ID канала (например: @your_channel или -100123456789)
    CHANNEL_ID = os.getenv('CHANNEL_ID', '')
    
    # Номер телефона для заказов (формат: +1234567890)
    PHONE_NUMBER = os.getenv('PHONE_NUMBER', '+1234567890')
    
    # ID первого администратора (ваш Telegram ID)
    # Узнать свой ID можно у бота @userinfobot
    OWNER_ID = int(os.getenv('OWNER_ID', '0') or '0')
    
    # Путь к файлу хранилища
    STORAGE_FILE = os.getenv('STORAGE_FILE', 'data.json')
    
    def validate(self):
        """Проверка конфигурации"""
        errors = []
        
        if not self.BOT_TOKEN:
            errors.append("BOT_TOKEN не установлен")
        
        if not self.CHANNEL_ID:
            errors.append("CHANNEL_ID не установлен")
        
        if not self.OWNER_ID or self.OWNER_ID == 0:
            errors.append("OWNER_ID не установлен")
        
        if errors:
            raise ValueError(f"Ошибки конфигурации:\n" + "\n".join(errors))
        
        return True