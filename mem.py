import datetime
import os
from telegram import Update
from telegram.ext import CallbackContext

WEIGHTS = {
    'стикер': 30,
    'достижения': 5,
    'жиза': 7,
    'навязчивые_мысли': 5,
    'планы': 8,
    'вопросы': 3,
    'настроение': 1,
    'правила': 7,
    'это_я': 3,
    'информация': 3
}


async def get_mem(update: Update, context: CallbackContext) -> None:
    seed = get_daily_seed(update.message.from_user.id)
    category = choose_category(seed)
    if category == 'стикер':
        sticker_set = await context.bot.get_sticker_set("Haha_kemp")
        await update.message.reply_text(f'{update.message.from_user.name}, твое состояние сегодня:')
        await update.message.reply_sticker(sticker_set.stickers[seed % len(sticker_set.stickers)])
    else:
        images = os.listdir('res/images/' + category)
        await context.bot.send_message(
            update.message.chat_id,
            f'{update.message.from_user.name}, {get_category_text(category)}'
        )
        await context.bot.send_photo(
            update.message.chat_id,
            f'res/images/{category}/{images[seed % len(images)]}'
        )


def get_daily_seed(user_id: int) -> int:
    date = datetime.date.today()
    return user_id * date.day * date.month * date.year


def choose_category(seed: int) -> str:
    seed = seed % sum(WEIGHTS.values())
    right = 0
    for category in WEIGHTS:
        left = right
        right += WEIGHTS[category]
        if left <= seed < right:
            return category


def get_category_text(category: str) -> str:
    match category:
        case 'достижения':
            return 'возможно, сегодня ты сможешь добиться чего-то необычного:\n\nРедкость: обычная 🌝🌝🌑🌑🌑'
        case 'жиза':
            return 'думаю, тебе знакомо это чувство:\n\nРедкость: стандартная 🌝🌑🌑🌑🌑'
        case 'навязчивые_мысли':
            return ('может быть, тебя преследуют подобные навязчивые мысли. '
                    'Постарайся думать, что это все неправда.\n\nРедкость: обычная 🌝🌝🌑🌑🌑')
        case 'планы':
            return 'думаю, сегодня тебе определенно стоит сделать что-то похожее:\n\nРедкость: стандартная 🌝🌑🌑🌑🌑'
        case 'вопросы':
            return 'сегодня важно задать себе правильный вопрос, а потом ответить на него\n\nРедкость: обычная 🌝🌝🌑🌑🌑'
        case 'настроение':
            return 'возможно это поднимет тебе настроение\n\nРедкость: легендарка 🌝🌝🌝🌝🌑'
        case 'правила':
            return 'есть важное правило. Сегодня лучше следовать ему во всем\n\nРедкость: стандартная 🌝🌑🌑🌑🌑'
        case 'это_я':
            return 'узнаешь себя?\n\nРедкость: редкая 🌝🌝🌝🌑🌑'
        case 'информация':
            return 'у меня есть важное сообщение для тебя.\n\nРедкость: редкая 🌝🌝🌝🌑🌑'
        case _:
            return 'без комментариев...\n\nРедкость: Невозможно 🌝🌝🌝🌝🌝'
