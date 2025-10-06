"""
Модуль для работы с хранилищем данных (JSON)
"""
import json
import os
from datetime import datetime
from typing import Optional, List, Dict
from config import Config


class Storage:
    """Класс для работы с хранилищем данных"""
    
    def __init__(self):
        self.config = Config()
        self.storage_file = self.config.STORAGE_FILE
        self._ensure_storage_exists()
    
    def _ensure_storage_exists(self):
        """Создание файла хранилища, если он не существует"""
        if not os.path.exists(self.storage_file):
            initial_data = {
                'admins': [self.config.OWNER_ID],
                'menu': {
                    'text': None,
                    'photo': None,
                    'updated_at': None,
                    'message_id': None
                }
            }
            self._save_data(initial_data)
    
    def _load_data(self) -> dict:
        """Загрузка данных из файла"""
        try:
            with open(self.storage_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {
                'admins': [self.config.OWNER_ID],
                'menu': {
                    'text': None,
                    'photo': None,
                    'updated_at': None,
                    'message_id': None
                }
            }
    
    def _save_data(self, data: dict):
        """Сохранение данных в файл"""
        with open(self.storage_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    # Работа с администраторами
    
    def get_admins(self) -> List[int]:
        """Получить список администраторов"""
        data = self._load_data()
        admins = data.get('admins', [])
        
        # Убеждаемся, что владелец всегда в списке
        if self.config.OWNER_ID not in admins:
            admins.append(self.config.OWNER_ID)
            data['admins'] = admins
            self._save_data(data)
        
        return admins
    
    def add_admin(self, user_id: int) -> bool:
        """Добавить администратора"""
        data = self._load_data()
        admins = data.get('admins', [])
        
        if user_id in admins:
            return False
        
        admins.append(user_id)
        data['admins'] = admins
        self._save_data(data)
        return True
    
    def remove_admin(self, user_id: int) -> bool:
        """Удалить администратора"""
        data = self._load_data()
        admins = data.get('admins', [])
        
        # Нельзя удалить владельца
        if user_id == self.config.OWNER_ID:
            return False
        
        if user_id not in admins:
            return False
        
        admins.remove(user_id)
        data['admins'] = admins
        self._save_data(data)
        return True
    
    # Работа с меню
    
    def save_menu(self, text: str, photo_file_id: Optional[str] = None):
        """Сохранить меню"""
        data = self._load_data()
        
        data['menu'] = {
            'text': text,
            'photo': photo_file_id,
            'updated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'message_id': data.get('menu', {}).get('message_id')  # Сохраняем старый message_id
        }
        
        self._save_data(data)
    
    def get_menu(self) -> Optional[Dict]:
        """Получить меню"""
        data = self._load_data()
        return data.get('menu')
    
    def save_menu_message_id(self, message_id: int):
        """Сохранить ID сообщения с меню в канале"""
        data = self._load_data()
        
        if 'menu' not in data:
            data['menu'] = {}
        
        data['menu']['message_id'] = message_id
        self._save_data(data)
    
    def get_menu_message_id(self) -> Optional[int]:
        """Получить ID сообщения с меню в канале"""
        data = self._load_data()
        menu = data.get('menu', {})
        return menu.get('message_id')