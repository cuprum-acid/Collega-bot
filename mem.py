import os
import random
from datetime import date
from telegram import Update
from telegram.ext import CallbackContext

WEIGHTS: dict[str, int] = {
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
today_memes: dict[int: [str, int]] = {}  # matches (category, img_number) to a user_id
last_update: date = date.today()

random.seed(last_update.year * last_update.month * last_update.day)


async def get_mem(update: Update, context: CallbackContext) -> None:
    mem: (str, int) = get_daily_mem(update.message.from_user.id)
    if mem[0] == 'стикер':
        sticker_set = await context.bot.get_sticker_set("Haha_kemp")
        if mem[1] == -1:
            mem[1] = random.randint(0, len(sticker_set.stickers) - 1)
        await context.bot.send_message(
            update.message.chat_id,
            f'{update.message.from_user.name}, твое состояние сегодня:'
        )
        await context.bot.send_sticker(
            update.message.chat_id,
            sticker_set.stickers[mem[1]]
        )
    else:
        images = os.listdir('res/images/' + mem[0])
        await context.bot.send_message(
            update.message.chat_id,
            f'{update.message.from_user.name}, {get_category_text(mem[0])}'
        )
        await context.bot.send_photo(
            update.message.chat_id,
            f'res/images/{mem[0]}/{images[mem[1]]}'
        )


def get_daily_mem(user_id: int) -> (str, int):
    global last_update
    if last_update.day != date.today().day:
        today_memes.clear()
        last_update = date.today()
    if user_id not in today_memes:
        category = choose_category(random.randint(0, sum(WEIGHTS.values()) - 1))
        img_id = -1
        if category != 'стикер':
            img_id = random.randint(0, len(os.listdir('res/images/' + category)) - 1)
        today_memes[user_id] = [category, img_id]
    return today_memes[user_id]


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
