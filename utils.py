from telegram import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

def get_main_menu_keyboard():
    keyboard = [
        [KeyboardButton("📋 Создать задачу")],
        [KeyboardButton("📋 Мои задачи"), KeyboardButton("📋 Задачи команды")],
        [KeyboardButton("⚙️ Настройки")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def get_task_type_keyboard():
    keyboard = [
        [InlineKeyboardButton("🌱 Полив", callback_data="type_watering")],
        [InlineKeyboardButton("🐛 Протравка", callback_data="type_treatment")],
        [InlineKeyboardButton("🌿 Дополнительный полив", callback_data="type_extra_water")],
        [InlineKeyboardButton("💧 Удобрения", callback_data="type_fertilizer")],
        [InlineKeyboardButton("✂️ Уход", callback_data="type_care")],
        [InlineKeyboardButton("🌿 Другое", callback_data="type_other")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_additional_params_keyboard():
    keyboard = [
        [InlineKeyboardButton("Протравка", callback_data="param_treatment")],
        [InlineKeyboardButton("Дополнительный полив", callback_data="param_extra_water")],
        [InlineKeyboardButton("Удобрения", callback_data="param_fertilizer")],
        [InlineKeyboardButton("Уход", callback_data="param_care")],
        [InlineKeyboardButton("Пропустить", callback_data="param_skip")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_send_target_keyboard():
    keyboard = [
        [InlineKeyboardButton("📥 Себе", callback_data="send_self")],
        [InlineKeyboardButton("👤 Конкретному пользователю", callback_data="send_user")],
        [InlineKeyboardButton("📢 В общий чат", callback_data="send_group")],
        [InlineKeyboardButton("📢 Всем", callback_data="send_all")]
    ]
    return InlineKeyboardMarkup(keyboard)
