# 📞 Быстрая смена номера телефона

## 🚀 На сервере (SSH):

```bash
cd ~/telegram-bot && ./update.sh
```

## 💬 В Telegram (личные сообщения с ботом):

```
/set_phone +17736812626
```

```
/publish_menu
```

## ✅ Готово!

---

## 📋 Другие команды:

```
/show_phone          - Показать текущий номер
/menu_info           - Информация о меню
/list_admins         - Список администраторов
```

---

## 🔧 Если что-то не работает:

```bash
# На сервере проверьте статус:
sudo systemctl status telegram-bot

# Перезапустите бота:
sudo systemctl restart telegram-bot

# Посмотрите логи:
sudo journalctl -u telegram-bot -n 50
```
