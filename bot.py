"""
Telegram Bot для управления меню канала и модерации обсуждений
"""
import logging
import os
import re
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)
from telegram.constants import ParseMode
from config import Config
from storage import Storage

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


class MenuBot:
    def __init__(self):
        self.config = Config()
        self.storage = Storage()
        
    def is_admin(self, user_id: int) -> bool:
        """Проверка, является ли пользователь администратором"""
        admins = self.storage.get_admins()
        logger.info(f"Проверка прав: user_id={user_id}, admins={admins}, is_admin={user_id in admins}")
        return user_id in admins
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /start"""
        user = update.effective_user
        
        if self.is_admin(user.id):
            await update.message.reply_text(
                f"👋 Привет, {user.first_name}!\n\n"
                "Вы администратор бота. Доступные команды:\n\n"
                "📋 /set_menu - Установить новое меню\n"
                "✏️ /edit_menu - Редактировать существующее меню\n"
                "📤 /publish_menu - Опубликовать/обновить меню в канале\n"
                "ℹ️ /menu_info - Информация о текущем меню\n"
                "⌨️ /setup_keyboard - Установить inline-кнопку меню в группе\n"
                "🔘 /enable_menu_button - Включить постоянную кнопку 'Меню на сегодня' внизу чата\n\n"
                "📞 /set_phone <номер> - Изменить номер телефона для заказов\n"
                "📱 /show_phone - Показать текущий номер телефона\n\n"
                "👥 /add_admin <user_id> - Добавить администратора\n"
                "❌ /remove_admin <user_id> - Удалить администратора\n"
                "📝 /list_admins - Список администраторов\n"
                "🔍 /chat_info - Информация о чате (для диагностики)"
            )
        else:
            await update.message.reply_text(
                f"👋 Привет, {user.first_name}!\n\n"
                "Это бот для управления меню канала."
            )
    
    async def set_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Начало процесса установки меню"""
        user_id = update.effective_user.id
        
        if not self.is_admin(user_id):
            await update.message.reply_text("❌ У вас нет прав для выполнения этой команды.")
            return
        
        await update.message.reply_text(
            "📝 Отправьте текст меню.\n\n"
            "Вы можете использовать форматирование:\n"
            "• *жирный текст*\n"
            "• _курсив_\n"
            "• `моноширинный`\n\n"
            "После отправки текста, вы сможете добавить фото (опционально)."
        )
        
        # Сохраняем состояние ожидания текста меню
        context.user_data['awaiting_menu_text'] = True
    
    async def handle_menu_text(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка текста меню"""
        user_id = update.effective_user.id
        
        if not self.is_admin(user_id):
            return
        
        # Проверяем режим редактирования
        if context.user_data.get('editing_menu_text'):
            await self.handle_edit_text(update, context)
            return
        
        if context.user_data.get('awaiting_menu_text'):
            menu_text = update.message.text
            context.user_data['menu_text'] = menu_text
            context.user_data['awaiting_menu_text'] = False
            
            await update.message.reply_text(
                "✅ Текст меню сохранен!\n\n"
                "📸 Теперь отправьте фото для меню (или отправьте /skip чтобы пропустить)."
            )
            context.user_data['awaiting_menu_photo'] = True
    
    async def handle_menu_photo(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка фото меню"""
        user_id = update.effective_user.id
        
        if not self.is_admin(user_id):
            return
        
        # Проверяем режим редактирования
        if context.user_data.get('editing_menu_photo'):
            await self.handle_edit_photo(update, context)
            return
        
        if context.user_data.get('awaiting_menu_photo'):
            photo = update.message.photo[-1]  # Берем фото наибольшего размера
            photo_file_id = photo.file_id
            
            menu_text = context.user_data.get('menu_text', '')
            
            # Сохраняем меню
            self.storage.save_menu(menu_text, photo_file_id)
            
            # Очищаем состояние
            context.user_data.clear()
            
            await update.message.reply_text(
                "✅ Меню успешно сохранено!\n\n"
                "Используйте /publish_menu для публикации в канале."
            )
    
    async def skip_photo(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Пропуск добавления фото"""
        user_id = update.effective_user.id
        
        if not self.is_admin(user_id):
            return
        
        if context.user_data.get('awaiting_menu_photo'):
            menu_text = context.user_data.get('menu_text', '')
            
            # Сохраняем меню без фото
            self.storage.save_menu(menu_text, None)
            
            # Очищаем состояние
            context.user_data.clear()
            
            await update.message.reply_text(
                "✅ Меню успешно сохранено (без фото)!\n\n"
                "Используйте /publish_menu для публикации в канале."
            )
    
    async def edit_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Начало процесса редактирования меню"""
        user_id = update.effective_user.id
        
        if not self.is_admin(user_id):
            await update.message.reply_text("❌ У вас нет прав для выполнения этой команды.")
            return
        
        # Проверяем, что меню существует
        menu_data = self.storage.get_menu()
        if not menu_data or not menu_data.get('text'):
            await update.message.reply_text(
                "❌ Меню еще не установлено.\n"
                "Сначала используйте /set_menu для создания меню."
            )
            return
        
        # Показываем текущее меню
        current_text = menu_data['text']
        has_photo = menu_data.get('photo') is not None
        
        try:
            # Сначала показываем текущее меню
            if has_photo:
                await update.message.reply_photo(
                    photo=menu_data['photo'],
                    caption=f"📋 Текущее меню:\n\n{current_text}",
                    parse_mode=ParseMode.MARKDOWN
                )
            else:
                await update.message.reply_text(
                    f"📋 Текущее меню:\n\n{current_text}",
                    parse_mode=ParseMode.MARKDOWN
                )
            
            # Затем показываем опции редактирования
            menu_options = (
                f"📸 Фото: {'✅ Есть' if has_photo else '❌ Нет'}\n\n"
                "Что вы хотите изменить?\n\n"
                "1️⃣ /edit_text - Изменить текст меню\n"
                "2️⃣ /edit_photo - Изменить/добавить фото\n"
                "3️⃣ /remove_photo - Удалить фото\n"
                "4️⃣ /cancel - Отменить редактирование"
            )
            
            await update.message.reply_text(menu_options)
            
        except Exception as e:
            logger.error(f"Ошибка при показе меню для редактирования: {e}")
            await update.message.reply_text(
                "❌ Произошла ошибка при показе меню.\n"
                "Попробуйте использовать команды напрямую:\n\n"
                "1️⃣ /edit_text - Изменить текст меню\n"
                "2️⃣ /edit_photo - Изменить/добавить фото\n"
                "3️⃣ /remove_photo - Удалить фото"
            )
    
    async def edit_text(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Начало редактирования текста меню"""
        user_id = update.effective_user.id
        
        if not self.is_admin(user_id):
            await update.message.reply_text("❌ У вас нет прав для выполнения этой команды.")
            return
        
        await update.message.reply_text(
            "📝 Отправьте новый текст меню.\n\n"
            "Вы можете использовать форматирование:\n"
            "• *жирный текст*\n"
            "• _курсив_\n"
            "• `моноширинный`\n\n"
            "Отправьте /cancel для отмены."
        )
        
        context.user_data['editing_menu_text'] = True
    
    async def edit_photo(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Начало редактирования фото меню"""
        user_id = update.effective_user.id
        
        if not self.is_admin(user_id):
            await update.message.reply_text("❌ У вас нет прав для выполнения этой команды.")
            return
        
        await update.message.reply_text(
            "📸 Отправьте новое фото для меню.\n\n"
            "Отправьте /cancel для отмены."
        )
        
        context.user_data['editing_menu_photo'] = True
    
    async def remove_photo(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Удаление фото из меню"""
        user_id = update.effective_user.id
        
        if not self.is_admin(user_id):
            await update.message.reply_text("❌ У вас нет прав для выполнения этой команды.")
            return
        
        menu_data = self.storage.get_menu()
        if not menu_data or not menu_data.get('photo'):
            await update.message.reply_text("❌ У меню нет фото для удаления.")
            return
        
        # Сохраняем меню без фото
        self.storage.save_menu(menu_data['text'], None)
        
        # Обновляем в канале, если меню было опубликовано
        message_id = self.storage.get_menu_message_id()
        if message_id:
            try:
                await context.bot.edit_message_text(
                    chat_id=self.config.CHANNEL_ID,
                    message_id=message_id,
                    text=menu_data['text'],
                    parse_mode=ParseMode.MARKDOWN,
                    reply_markup=self._get_order_keyboard()
                )
                await update.message.reply_text(
                    "✅ Фото удалено из меню!\n"
                    "Меню в канале обновлено."
                )
            except Exception as e:
                logger.error(f"Ошибка при обновлении меню в канале: {e}")
                await update.message.reply_text(
                    "✅ Фото удалено из меню!\n"
                    "⚠️ Не удалось обновить меню в канале. Используйте /publish_menu для обновления."
                )
        else:
            await update.message.reply_text("✅ Фото удалено из меню!")
    
    async def cancel_edit(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Отмена редактирования"""
        user_id = update.effective_user.id
        
        if not self.is_admin(user_id):
            return
        
        # Очищаем состояние редактирования
        context.user_data.pop('editing_menu_text', None)
        context.user_data.pop('editing_menu_photo', None)
        
        await update.message.reply_text("❌ Редактирование отменено.")
    
    async def handle_edit_text(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка нового текста меню при редактировании"""
        user_id = update.effective_user.id
        
        if not self.is_admin(user_id):
            return
        
        if context.user_data.get('editing_menu_text'):
            new_text = update.message.text
            
            # Получаем текущее меню
            menu_data = self.storage.get_menu()
            photo_file_id = menu_data.get('photo') if menu_data else None
            
            # Сохраняем меню с новым текстом
            self.storage.save_menu(new_text, photo_file_id)
            
            # Очищаем состояние
            context.user_data.pop('editing_menu_text', None)
            
            # Обновляем в канале, если меню было опубликовано
            message_id = self.storage.get_menu_message_id()
            if message_id:
                try:
                    # Добавляем номер телефона, если его нет
                    display_text = new_text
                    if self.config.PHONE_NUMBER not in display_text:
                        display_text += f"\n\n📞 *Телефон для заказов:* {self.config.PHONE_NUMBER}"
                    
                    if photo_file_id:
                        await context.bot.edit_message_caption(
                            chat_id=self.config.CHANNEL_ID,
                            message_id=message_id,
                            caption=display_text,
                            parse_mode=ParseMode.MARKDOWN,
                            reply_markup=self._get_order_keyboard()
                        )
                    else:
                        await context.bot.edit_message_text(
                            chat_id=self.config.CHANNEL_ID,
                            message_id=message_id,
                            text=display_text,
                            parse_mode=ParseMode.MARKDOWN,
                            reply_markup=self._get_order_keyboard()
                        )
                    
                    await update.message.reply_text(
                        "✅ Текст меню обновлен!\n"
                        "Меню в канале также обновлено."
                    )
                except Exception as e:
                    logger.error(f"Ошибка при обновлении меню в канале: {e}")
                    await update.message.reply_text(
                        "✅ Текст меню обновлен!\n"
                        "⚠️ Не удалось обновить меню в канале. Используйте /publish_menu для обновления."
                    )
            else:
                await update.message.reply_text(
                    "✅ Текст меню обновлен!\n"
                    "Используйте /publish_menu для публикации в канале."
                )
    
    async def handle_edit_photo(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка нового фото меню при редактировании"""
        user_id = update.effective_user.id
        
        if not self.is_admin(user_id):
            return
        
        if context.user_data.get('editing_menu_photo'):
            photo = update.message.photo[-1]
            new_photo_file_id = photo.file_id
            
            # Получаем текущее меню
            menu_data = self.storage.get_menu()
            menu_text = menu_data.get('text', '') if menu_data else ''
            
            # Сохраняем меню с новым фото
            self.storage.save_menu(menu_text, new_photo_file_id)
            
            # Очищаем состояние
            context.user_data.pop('editing_menu_photo', None)
            
            # Обновляем в канале, если меню было опубликовано
            message_id = self.storage.get_menu_message_id()
            if message_id:
                try:
                    # Добавляем номер телефона, если его нет
                    display_text = menu_text
                    if self.config.PHONE_NUMBER not in display_text:
                        display_text += f"\n\n📞 *Телефон для заказов:* {self.config.PHONE_NUMBER}"
                    
                    # Удаляем старое сообщение и создаем новое с фото
                    await context.bot.delete_message(
                        chat_id=self.config.CHANNEL_ID,
                        message_id=message_id
                    )
                    
                    sent_message = await context.bot.send_photo(
                        chat_id=self.config.CHANNEL_ID,
                        photo=new_photo_file_id,
                        caption=display_text,
                        parse_mode=ParseMode.MARKDOWN,
                        reply_markup=self._get_order_keyboard()
                    )
                    
                    # Сохраняем новый message_id
                    self.storage.save_menu_message_id(sent_message.message_id)
                    
                    await update.message.reply_text(
                        "✅ Фото меню обновлено!\n"
                        "Меню в канале также обновлено."
                    )
                except Exception as e:
                    logger.error(f"Ошибка при обновлении меню в канале: {e}")
                    await update.message.reply_text(
                        "✅ Фото меню обновлено!\n"
                        "⚠️ Не удалось обновить меню в канале. Используйте /publish_menu для обновления."
                    )
            else:
                await update.message.reply_text(
                    "✅ Фото меню обновлено!\n"
                    "Используйте /publish_menu для публикации в канале."
                )
    
    def _get_order_keyboard(self):
        """Создает клавиатуру с кнопкой заказа"""
        phone_clean = self.config.PHONE_NUMBER.replace('+', '').replace(' ', '').replace('-', '')
        keyboard = [
            [InlineKeyboardButton("📞 Заказать (WhatsApp)", url=f"https://wa.me/{phone_clean}")]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    async def publish_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Публикация или обновление меню в канале"""
        user_id = update.effective_user.id
        
        if not self.is_admin(user_id):
            await update.message.reply_text("❌ У вас нет прав для выполнения этой команды.")
            return
        
        menu_data = self.storage.get_menu()
        
        if not menu_data or not menu_data.get('text'):
            await update.message.reply_text("❌ Меню не установлено. Используйте /set_menu")
            return
        
        # Получаем данные меню
        channel_id = self.config.CHANNEL_ID
        menu_text = menu_data['text']
        photo_file_id = menu_data.get('photo')
        
        # Создаем кнопку для заказа
        # Telegram не поддерживает tel: ссылки в inline кнопках
        # Используем WhatsApp ссылку (работает на всех устройствах)
        phone_clean = self.config.PHONE_NUMBER.replace('+', '').replace(' ', '').replace('-', '')
        
        # Добавляем номер телефона в конец меню, если его там нет
        if self.config.PHONE_NUMBER not in menu_text:
            menu_text += f"\n\n📞 *Телефон для заказов:* {self.config.PHONE_NUMBER}"
        
        keyboard = [
            [InlineKeyboardButton("📞 Заказать (WhatsApp)", url=f"https://wa.me/{phone_clean}")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        try:
            # Проверяем, есть ли уже опубликованное меню
            message_id = self.storage.get_menu_message_id()
            
            if message_id:
                # Обновляем существующее сообщение
                try:
                    if photo_file_id:
                        await context.bot.edit_message_media(
                            chat_id=channel_id,
                            message_id=message_id,
                            media={"type": "photo", "media": photo_file_id, "caption": menu_text, "parse_mode": ParseMode.MARKDOWN},
                            reply_markup=reply_markup
                        )
                    else:
                        await context.bot.edit_message_text(
                            chat_id=channel_id,
                            message_id=message_id,
                            text=menu_text,
                            parse_mode=ParseMode.MARKDOWN,
                            reply_markup=reply_markup
                        )
                    
                    await update.message.reply_text("✅ Меню успешно обновлено в канале!")
                    return
                    
                except Exception as e:
                    logger.warning(f"Не удалось обновить сообщение: {e}. Создаем новое.")
            
            # Публикуем новое сообщение
            if photo_file_id:
                sent_message = await context.bot.send_photo(
                    chat_id=channel_id,
                    photo=photo_file_id,
                    caption=menu_text,
                    parse_mode=ParseMode.MARKDOWN,
                    reply_markup=reply_markup
                )
            else:
                sent_message = await context.bot.send_message(
                    chat_id=channel_id,
                    text=menu_text,
                    parse_mode=ParseMode.MARKDOWN,
                    reply_markup=reply_markup
                )
            
            # Сохраняем ID сообщения
            self.storage.save_menu_message_id(sent_message.message_id)
            
            await update.message.reply_text("✅ Меню успешно опубликовано в канале!")
            
        except Exception as e:
            logger.error(f"Ошибка при публикации меню: {e}")
            await update.message.reply_text(f"❌ Ошибка при публикации меню: {str(e)}")
    
    async def menu_info(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Показать информацию о текущем меню"""
        user_id = update.effective_user.id
        
        if not self.is_admin(user_id):
            await update.message.reply_text("❌ У вас нет прав для выполнения этой команды.")
            return
        
        menu_data = self.storage.get_menu()
        
        if not menu_data or not menu_data.get('text'):
            await update.message.reply_text("❌ Меню не установлено.")
            return
        
        info = f"📋 **Текущее меню:**\n\n{menu_data['text']}\n\n"
        info += f"📸 Фото: {'Да' if menu_data.get('photo') else 'Нет'}\n"
        info += f"📅 Обновлено: {menu_data.get('updated_at', 'Неизвестно')}"
        
        await update.message.reply_text(info, parse_mode=ParseMode.MARKDOWN)
    
    async def add_admin(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Добавить администратора"""
        user_id = update.effective_user.id
        
        if not self.is_admin(user_id):
            await update.message.reply_text("❌ У вас нет прав для выполнения этой команды.")
            return
        
        if not context.args or len(context.args) != 1:
            await update.message.reply_text("❌ Использование: /add_admin <user_id>")
            return
        
        try:
            new_admin_id = int(context.args[0])
            
            if self.storage.add_admin(new_admin_id):
                await update.message.reply_text(f"✅ Пользователь {new_admin_id} добавлен в администраторы.")
            else:
                await update.message.reply_text(f"ℹ️ Пользователь {new_admin_id} уже является администратором.")
                
        except ValueError:
            await update.message.reply_text("❌ Неверный формат user_id. Должно быть число.")
    
    async def remove_admin(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Удалить администратора"""
        user_id = update.effective_user.id
        
        if not self.is_admin(user_id):
            await update.message.reply_text("❌ У вас нет прав для выполнения этой команды.")
            return
        
        if not context.args or len(context.args) != 1:
            await update.message.reply_text("❌ Использование: /remove_admin <user_id>")
            return
        
        try:
            admin_id_to_remove = int(context.args[0])
            
            if admin_id_to_remove == user_id:
                await update.message.reply_text("❌ Вы не можете удалить себя из администраторов.")
                return
            
            if self.storage.remove_admin(admin_id_to_remove):
                await update.message.reply_text(f"✅ Пользователь {admin_id_to_remove} удален из администраторов.")
            else:
                await update.message.reply_text(f"❌ Пользователь {admin_id_to_remove} не является администратором.")
                
        except ValueError:
            await update.message.reply_text("❌ Неверный формат user_id. Должно быть число.")
    
    async def list_admins(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Список администраторов"""
        user_id = update.effective_user.id
        
        if not self.is_admin(user_id):
            await update.message.reply_text("❌ У вас нет прав для выполнения этой команды.")
            return
        
        admins = self.storage.get_admins()
        
        if not admins:
            await update.message.reply_text("❌ Список администраторов пуст.")
            return
        
        admin_list = "\n".join([f"• {admin_id}" for admin_id in admins])
        await update.message.reply_text(f"👥 **Администраторы:**\n\n{admin_list}", parse_mode=ParseMode.MARKDOWN)
    
    async def set_phone(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Изменить номер телефона для заказов"""
        user_id = update.effective_user.id
        
        if not self.is_admin(user_id):
            await update.message.reply_text("❌ У вас нет прав для выполнения этой команды.")
            return
        
        if not context.args or len(context.args) != 1:
            await update.message.reply_text(
                "❌ Использование: /set_phone <номер>\n\n"
                "Примеры:\n"
                "• /set_phone +17736812626\n"
                "• /set_phone +1 (773) 681-2626\n"
                "• /set_phone 17736812626"
            )
            return
        
        new_phone = context.args[0]
        
        # Проверяем формат номера (должен содержать цифры)
        phone_digits = ''.join(filter(str.isdigit, new_phone))
        if len(phone_digits) < 10:
            await update.message.reply_text(
                "❌ Номер телефона слишком короткий.\n"
                "Минимум 10 цифр."
            )
            return
        
        # Сохраняем новый номер в .env файл
        try:
            env_path = '.env'
            env_content = []
            phone_updated = False
            
            # Читаем существующий .env файл
            if os.path.exists(env_path):
                with open(env_path, 'r', encoding='utf-8') as f:
                    env_content = f.readlines()
            
            # Обновляем или добавляем PHONE_NUMBER
            new_env_content = []
            for line in env_content:
                if line.startswith('PHONE_NUMBER='):
                    new_env_content.append(f'PHONE_NUMBER={new_phone}\n')
                    phone_updated = True
                else:
                    new_env_content.append(line)
            
            # Если PHONE_NUMBER не было в файле, добавляем
            if not phone_updated:
                new_env_content.append(f'PHONE_NUMBER={new_phone}\n')
            
            # Записываем обновленный .env файл
            with open(env_path, 'w', encoding='utf-8') as f:
                f.writelines(new_env_content)
            
            # Обновляем в памяти
            self.config.PHONE_NUMBER = new_phone
            
            await update.message.reply_text(
                f"✅ Номер телефона успешно изменен!\n\n"
                f"📞 Новый номер: {new_phone}\n\n"
                f"⚠️ Чтобы изменения вступили в силу в опубликованном меню,\n"
                f"используйте /publish_menu для обновления меню в канале."
            )
            
            logger.info(f"Номер телефона изменен на {new_phone} пользователем {user_id}")
            
        except Exception as e:
            logger.error(f"Ошибка при изменении номера телефона: {e}")
            await update.message.reply_text(
                f"❌ Ошибка при сохранении номера телефона:\n{str(e)}\n\n"
                f"Попробуйте изменить номер вручную в файле .env на сервере."
            )
    
    async def show_phone(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Показать текущий номер телефона"""
        user_id = update.effective_user.id
        
        if not self.is_admin(user_id):
            await update.message.reply_text("❌ У вас нет прав для выполнения этой команды.")
            return
        
        current_phone = self.config.PHONE_NUMBER
        await update.message.reply_text(
            f"📱 Текущий номер телефона для заказов:\n\n"
            f"📞 {current_phone}\n\n"
            f"Для изменения используйте:\n"
            f"/set_phone <новый_номер>"
        )
    
    async def get_chat_info(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Получить информацию о текущем чате (для диагностики)"""
        try:
            logger.info("=== chat_info НАЧАЛО ===")
            chat = update.effective_chat
            user_id = update.effective_user.id
            
            # Отладочная информация
            logger.info(f"chat_info вызвана пользователем {user_id}")
            logger.info(f"Список администраторов: {self.storage.get_admins()}")
            logger.info(f"Проверка is_admin({user_id}): {self.is_admin(user_id)}")
            
            if not self.is_admin(user_id):
                await update.message.reply_text(
                    f"❌ У вас нет прав для выполнения этой команды.\n\n"
                    f"🆔 Ваш ID: `{user_id}`\n"
                    f"👥 Администраторы: {self.storage.get_admins()}"
                )
                return
        except Exception as e:
            logger.error(f"Ошибка в начале chat_info: {e}", exc_info=True)
            await update.message.reply_text(f"❌ Ошибка: {str(e)}")
            return
        
        try:
            info = f"🔍 Информация о чате:\n\n"
            info += f"📝 Название: {chat.title or 'N/A'}\n"
            info += f"🆔 Chat ID: {chat.id}\n"
            info += f"📊 Тип: {chat.type}\n"
            
            # Безопасная обработка username
            username_text = f"@{chat.username}" if chat.username else "N/A"
            info += f"👤 Username: {username_text}\n\n"
            
            info += f"⚙️ Настроенный CHANNEL_ID: {self.config.CHANNEL_ID}\n"
            
            if str(chat.id) == str(self.config.CHANNEL_ID):
                info += "\n✅ ID совпадает с настроенным!"
            else:
                info += "\n⚠️ ID НЕ совпадает с настроенным в .env!"
            
            # Проверяем права бота в этом чате
            try:
                bot_member = await context.bot.get_chat_member(chat.id, context.bot.id)
                info += f"\n\n🤖 Статус бота:\n"
                info += f"Статус: {bot_member.status}\n"
                
                if bot_member.status in ['administrator', 'creator']:
                    info += "✅ Бот является администратором\n"
                    # Проверяем конкретные права
                    if hasattr(bot_member, 'can_post_messages'):
                        info += f"Может публиковать: {'✅' if bot_member.can_post_messages else '❌'}\n"
                    if hasattr(bot_member, 'can_delete_messages'):
                        info += f"Может удалять: {'✅' if bot_member.can_delete_messages else '❌'}\n"
                    if hasattr(bot_member, 'can_pin_messages'):
                        info += f"Может закреплять: {'✅' if bot_member.can_pin_messages else '❌'}\n"
                else:
                    info += "❌ Бот НЕ является администратором\n"
            except Exception as e:
                info += f"\n\n⚠️ Не удалось получить информацию о правах: {str(e)}"
            
            logger.info(f"Отправка ответа chat_info пользователю {user_id}")
            await update.message.reply_text(info)
            logger.info("chat_info успешно завершена")
        except Exception as e:
            logger.error(f"Ошибка при формировании ответа chat_info: {e}", exc_info=True)
            await update.message.reply_text(f"❌ Ошибка при получении информации: {str(e)}")
    
    async def setup_menu_keyboard(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Установить закрепленное сообщение с кнопкой меню в группе (только для админов)"""
        user_id = update.effective_user.id
        
        if not self.is_admin(user_id):
            await update.message.reply_text("❌ У вас нет прав для выполнения этой команды.")
            return
        
        # Проверяем, что команда вызвана в группе
        if update.effective_chat.type not in ['group', 'supergroup']:
            await update.message.reply_text("❌ Эта команда работает только в группах.")
            return
        
        try:
            # Проверяем, что меню установлено
            menu_data = self.storage.get_menu()
            if not menu_data or not menu_data.get('text'):
                await update.message.reply_text(
                    "❌ Меню еще не установлено.\n"
                    "Сначала используйте /set_menu для создания меню."
                )
                return
            
            # Создаем inline-кнопку с callback для показа меню
            keyboard = [
                [InlineKeyboardButton("📋 Menu", callback_data="show_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            # Отправляем сообщение с кнопкой
            sent_message = await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="🍽 Нажмите кнопку ниже, чтобы посмотреть меню:",
                reply_markup=reply_markup
            )
            
            # Пытаемся закрепить сообщение
            try:
                await context.bot.pin_chat_message(
                    chat_id=update.effective_chat.id,
                    message_id=sent_message.message_id,
                    disable_notification=True  # Без уведомления
                )
                await update.message.reply_text(
                    "✅ Кнопка меню установлена и закреплена!\n\n"
                    "Все участники группы могут нажать на неё, чтобы посмотреть меню."
                )
            except Exception as pin_error:
                logger.warning(f"Не удалось закрепить сообщение: {pin_error}")
                await update.message.reply_text(
                    "✅ Кнопка меню установлена!\n\n"
                    "⚠️ Не удалось закрепить сообщение. Убедитесь, что бот имеет права на закрепление сообщений в группе."
                )
                
        except Exception as e:
            logger.error(f"Ошибка при установке кнопки меню: {e}")
            await update.message.reply_text(f"❌ Ошибка: {str(e)}")
    
    async def enable_menu_button(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Включить постоянную кнопку 'Menu' внизу чата для всех пользователей группы"""
        user_id = update.effective_user.id
        
        if not self.is_admin(user_id):
            await update.message.reply_text("❌ У вас нет прав для выполнения этой команды.")
            return
        
        # Проверяем, что команда вызвана в группе
        if update.effective_chat.type not in ['group', 'supergroup']:
            await update.message.reply_text("❌ Эта команда работает только в группах.")
            return
        
        try:
            # Проверяем, что меню установлено
            menu_data = self.storage.get_menu()
            if not menu_data or not menu_data.get('text'):
                await update.message.reply_text(
                    "❌ Меню еще не установлено.\n"
                    "Сначала используйте /set_menu для создания меню."
                )
                return
            
            # Создаем постоянную клавиатуру с кнопкой Menu
            keyboard = [[KeyboardButton("📋 Меню на сегодня")]]
            reply_markup = ReplyKeyboardMarkup(
                keyboard,
                resize_keyboard=True,  # Автоматически подстраивать размер кнопок
                one_time_keyboard=False  # Кнопка остается видимой после нажатия
            )
            
            # Отправляем сообщение с клавиатурой
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="✅ Постоянная кнопка '📋 Меню на сегодня' активирована!\n\n"
                     "Теперь все участники группы могут нажать на кнопку внизу чата, чтобы посмотреть меню.",
                reply_markup=reply_markup
            )
            
        except Exception as e:
            logger.error(f"Ошибка при включении кнопки Menu: {e}")
            await update.message.reply_text(f"❌ Ошибка: {str(e)}")
    
    async def handle_menu_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик нажатия на inline-кнопку Menu"""
        query = update.callback_query
        await query.answer()  # Убираем "часики" на кнопке
        
        try:
            # Получаем данные меню
            menu_data = self.storage.get_menu()
            
            if not menu_data or not menu_data.get('text'):
                await query.message.reply_text(
                    "❌ Меню пока не установлено.\n"
                    "Пожалуйста, обратитесь к администратору."
                )
                return
            
            menu_text = menu_data['text']
            photo_file_id = menu_data.get('photo')
            
            # Создаем кнопку для заказа
            phone_clean = self.config.PHONE_NUMBER.replace('+', '').replace(' ', '').replace('-', '')
            keyboard = [
                [InlineKeyboardButton("📞 Заказать (WhatsApp)", url=f"https://wa.me/{phone_clean}")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            # Отправляем меню
            if photo_file_id:
                await query.message.reply_photo(
                    photo=photo_file_id,
                    caption=menu_text,
                    parse_mode=ParseMode.MARKDOWN,
                    reply_markup=reply_markup
                )
            else:
                await query.message.reply_text(
                    menu_text,
                    parse_mode=ParseMode.MARKDOWN,
                    reply_markup=reply_markup
                )
                
        except Exception as e:
            logger.error(f"Ошибка при показе меню через callback: {e}")
            await query.message.reply_text(f"❌ Ошибка при загрузке меню: {str(e)}")
    
    async def show_today_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Показать меню на сегодня (доступно всем пользователям в группе)"""
        try:
            # Получаем данные меню
            menu_data = self.storage.get_menu()
            
            if not menu_data or not menu_data.get('text'):
                await update.message.reply_text(
                    "❌ Меню пока не установлено.\n"
                    "Пожалуйста, обратитесь к администратору."
                )
                return
            
            # Получаем ID опубликованного сообщения в канале
            message_id = self.storage.get_menu_message_id()
            channel_id = self.config.CHANNEL_ID
            
            if message_id and channel_id:
                # Формируем ссылку на сообщение в канале
                # Убираем -100 из начала ID канала для ссылки
                channel_id_str = str(channel_id)
                if channel_id_str.startswith('-100'):
                    channel_id_clean = channel_id_str[4:]
                else:
                    channel_id_clean = channel_id_str.lstrip('-')
                
                menu_link = f"https://t.me/c/{channel_id_clean}/{message_id}"
                
                # Создаем кнопку для перехода к меню в канале
                keyboard = [
                    [InlineKeyboardButton("📋 Открыть меню в канале", url=menu_link)]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                await update.message.reply_text(
                    "🍽 Меню на сегодня опубликовано в канале!\n\n"
                    "Нажмите кнопку ниже, чтобы посмотреть:",
                    reply_markup=reply_markup
                )
            else:
                # Если меню не опубликовано, показываем текст напрямую
                menu_text = menu_data['text']
                photo_file_id = menu_data.get('photo')
                
                # Создаем кнопку для заказа
                phone_clean = self.config.PHONE_NUMBER.replace('+', '').replace(' ', '').replace('-', '')
                keyboard = [
                    [InlineKeyboardButton("📞 Заказать (WhatsApp)", url=f"https://wa.me/{phone_clean}")]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                if photo_file_id:
                    await update.message.reply_photo(
                        photo=photo_file_id,
                        caption=menu_text,
                        parse_mode=ParseMode.MARKDOWN,
                        reply_markup=reply_markup
                    )
                else:
                    await update.message.reply_text(
                        menu_text,
                        parse_mode=ParseMode.MARKDOWN,
                        reply_markup=reply_markup
                    )
                    
        except Exception as e:
            logger.error(f"Ошибка при показе меню: {e}", exc_info=True)
            await update.message.reply_text(
                "❌ Произошла ошибка при получении меню.\n"
                "Пожалуйста, попробуйте позже."
            )
    
    async def moderate_links(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Удаление сообщений со ссылками в обсуждениях канала"""
        message = update.message or update.channel_post
        
        if not message or not message.text:
            return
        
        # Проверяем, что это сообщение из обсуждений канала
        if message.chat.type not in ['group', 'supergroup']:
            return
        
        # Проверяем, является ли отправитель администратором
        user_id = message.from_user.id if message.from_user else None
        if user_id and self.is_admin(user_id):
            return  # Админы могут отправлять ссылки
        
        # Регулярное выражение для поиска ссылок
        url_pattern = re.compile(
            r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
            r'|(?:www\.)[a-zA-Z0-9-]+\.[a-zA-Z]{2,}'
            r'|(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}'
            r'|t\.me/[a-zA-Z0-9_]+'
        )
        
        # Проверяем наличие ссылок
        if url_pattern.search(message.text):
            try:
                await message.delete()
                logger.info(f"Удалено сообщение со ссылкой от пользователя {user_id}")
                
                # Отправляем предупреждение (опционально)
                warning = await context.bot.send_message(
                    chat_id=message.chat_id,
                    text="⚠️ Ссылки в обсуждениях запрещены и были удалены.",
                    reply_to_message_id=message.message_id if message.message_id else None
                )
                
                # Удаляем предупреждение через 5 секунд
                await context.application.job_queue.run_once(
                    lambda ctx: warning.delete(),
                    when=5
                )
                
            except Exception as e:
                logger.error(f"Ошибка при удалении сообщения: {e}")
    
    def run(self):
        """Запуск бота"""
        # Создаем приложение
        application = Application.builder().token(self.config.BOT_TOKEN).build()
        
        # Регистрируем обработчики команд
        application.add_handler(CommandHandler("start", self.start))
        application.add_handler(CommandHandler("set_menu", self.set_menu))
        application.add_handler(CommandHandler("edit_menu", self.edit_menu))
        application.add_handler(CommandHandler("edit_text", self.edit_text))
        application.add_handler(CommandHandler("edit_photo", self.edit_photo))
        application.add_handler(CommandHandler("remove_photo", self.remove_photo))
        application.add_handler(CommandHandler("cancel", self.cancel_edit))
        application.add_handler(CommandHandler("skip", self.skip_photo))
        application.add_handler(CommandHandler("publish_menu", self.publish_menu))
        application.add_handler(CommandHandler("menu_info", self.menu_info))
        application.add_handler(CommandHandler("add_admin", self.add_admin))
        application.add_handler(CommandHandler("remove_admin", self.remove_admin))
        application.add_handler(CommandHandler("list_admins", self.list_admins))
        application.add_handler(CommandHandler("set_phone", self.set_phone))
        application.add_handler(CommandHandler("show_phone", self.show_phone))
        application.add_handler(CommandHandler("chat_info", self.get_chat_info))
        application.add_handler(CommandHandler("setup_keyboard", self.setup_menu_keyboard))
        application.add_handler(CommandHandler("enable_menu_button", self.enable_menu_button))
        
        # Обработчик callback для inline-кнопки Menu
        application.add_handler(CallbackQueryHandler(self.handle_menu_callback, pattern="^show_menu$"))
        
        # Обработчики сообщений
        application.add_handler(
            MessageHandler(
                filters.TEXT & ~filters.COMMAND & filters.ChatType.PRIVATE,
                self.handle_menu_text
            )
        )
        application.add_handler(
            MessageHandler(
                filters.PHOTO & filters.ChatType.PRIVATE,
                self.handle_menu_photo
            )
        )
        
        # Обработчик кнопки "Меню на сегодня" и "Menu" в группах
        application.add_handler(
            MessageHandler(
                filters.Regex(r'^(Меню на сегодня|📋 Меню на сегодня|📋 Menu|Menu)$') & filters.ChatType.GROUPS,
                self.show_today_menu
            )
        )
        
        # Модерация ссылок в группах/обсуждениях
        application.add_handler(
            MessageHandler(
                filters.TEXT & filters.ChatType.GROUPS,
                self.moderate_links
            )
        )
        
        logger.info("Бот запущен!")
        
        # Запускаем бота
        application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    bot = MenuBot()
    bot.run()