from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
from config import TELEGRAM_BOT_TOKEN
from database import init_db, add_user
from roles import can_create_task, can_send_to_chat
from utils import get_main_menu_keyboard, get_task_type_keyboard, get_additional_params_keyboard, get_send_target_keyboard
from calendar_integration import create_calendar_event
import json

# Глобальное состояние для сбора данных задачи
active_tasks = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    # Пример: добавляем пользователя как "worker", если его нет
    add_user(user.id, user.full_name, "worker")

    await update.message.reply_html(
        f"Привет, {user.mention_html()}! Это бот для управления задачами по уходу за растениями.",
        reply_markup=get_main_menu_keyboard(),
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.effective_user.id

    if text == "📋 Создать задачу":
        if can_create_task(user_id):
            await update.message.reply_text("Выберите тип задачи:", reply_markup=get_task_type_keyboard())
            active_tasks[user_id] = {}
        else:
            await update.message.reply_text("У вас нет прав для создания задач.")

    elif text == "📢 В общий чат":
        if can_send_to_chat(user_id):
            await context.bot.send_message(chat_id=-1001234567890, text="Сообщение от озеленителя!")  # ID чата
        else:
            await update.message.reply_text("У вас нет прав для отправки в общий чат.")

# Обработчик inline-кнопок
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    data = query.data

    if data.startswith("type_"):
        active_tasks[user_id]["type"] = data.replace("type_", "")
        await query.edit_message_text(text="Укажите место (адрес или отправьте геолокацию).")

    elif data.startswith("param_"):
        param = data.replace("param_", "")
        if param != "skip":
            if "params" not in active_tasks[user_id]:
                active_tasks[user_id]["params"] = []
            active_tasks[user_id]["params"].append(param)
        await query.edit_message_text(text="Прикрепите фото (опционально) или нажмите 'Пропустить'.")

    elif data.startswith("send_"):
        target = data.replace("send_", "")
        task = active_tasks.get(user_id, {})

        # Если есть дата и время — создаём событие в календаре
        if "datetime" in task and "location" in task:
            try:
                link = create_calendar_event(
                    summary=task["type"],
                    location=task["location"],
                    start_time=task["datetime"],
                    end_time=task["datetime"]  # или +1 час, если нужно
                )
                await query.edit_message_text(f"Задача отправлена {target} и добавлена в календарь: {link}")
            except Exception as e:
                await query.edit_message_text(f"Ошибка при добавлении в календарь: {e}")
        else:
            await query.edit_message_text(f"Задача отправлена {target}.")

# Запуск бота
if __name__ == "__main__":
    init_db()
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(button_callback))

    print("Бот запущен...")
    app.run_polling()
