import logging
import os
import random
from datetime import date
from telegram import Update, error
from telegram.ext import CallbackContext

from logger import logger


class ImageCategory:
    def __init__(self, name: str, description: str, chance: int):
        self.name: str = name
        self.description: str = description
        self.chance: int = chance
        self.memes: list[str] = os.listdir(f'res/images/{name}/')


class StickerCategory:
    def __init__(self, name: str, chance: int):
        self.name: str = name
        self.chance: int = chance
        self.memes = None


meme_categories = [
    StickerCategory(
        os.environ.get('STICKERS_NAME1'),
        17
    ),
    StickerCategory(
        os.environ.get('STICKERS_NAME2'),
        17
    ),
    ImageCategory(
        'достижения',
        'возможно, сегодня ты сможешь добиться чего-то необычного:\n\nРедкость: колдовство\n🌝🌝🌝🌑🌑',
        4
    ),
    ImageCategory(
        'жиза',
        'думаю, тебе знакомо это чувство:\n\nРедкость: ничего особенного\n🌝🌝🌑🌑🌑',
        8
    ),
    ImageCategory(
        'навязчивые_мысли',
        ('может быть, тебя преследуют подобные навязчивые мысли. '
         'Постарайся думать, что это все неправда.\n\nРедкость: колдовство\n🌝🌝🌝🌑🌑'),
        4
    ),
    ImageCategory(
        'планы',
        'думаю, сегодня тебе определенно стоит сделать что-то похожее:\n\nРедкость: ничего особенного\n🌝🌝🌑🌑🌑',
        8
    ),
    ImageCategory(
        'вопросы',
        'сегодня важно задать себе правильный вопрос, а потом ответить на него\n\nРедкость: ничего особенного\n🌝🌝🌑🌑🌑',
        8
    ),
    ImageCategory(
        'настроение',
        'возможно это поднимет тебе настроение\n\nРедкость: ЛеГеНдАрКа\n🌝🌝🌝🌝🌝',
        1
    ),
    ImageCategory(
        'правила',
        'есть важное правило. Сегодня лучше следовать ему во всем\n\nРедкость: ничего особенного\n🌝🌝🌑🌑🌑',
        8
    ),
    ImageCategory(
        'это_я',
        'узнаешь себя?\n\nРедкость: цыганские фокусы!\n🌝🌝🌝🌝🌑',
        2
    ),
    ImageCategory(
        'информация',
        'у меня есть важное сообщение для тебя.\n\nРедкость: цыганские фокусы!\n🌝🌝🌝🌝🌑',
        2
    )
]
today_memes = dict()
last_update: date = date.today()


async def get_mem(update: Update, context: CallbackContext) -> None:
    global last_update
    if date.today() != last_update:
        today_memes.clear()
        last_update = date.today()
        logger.info(f"Updated memes on {last_update}")
    user_id = update.message.from_user.id
    if user_id not in today_memes:
        meme_category = random.choices(meme_categories, weights=[category.chance for category in meme_categories])[0]
        if isinstance(meme_category, StickerCategory) and meme_category.memes is None:
            try:
                meme_category.memes = (await context.bot.get_sticker_set(meme_category.name)).stickers
                logger.info(f'Loaded sticker set {meme_category.name}')
            except error.TimedOut as e:
                logger.warning(f'Timed out getting sticker set {meme_category.name}\n')
            except Exception as e:
                logger.warning(f'Invalid sticker set {meme_category.name}\n {e}')

        today_memes[user_id] = (meme_category, random.randint(0, len(meme_category.memes) - 1))

    meme_category = today_memes[user_id][0]
    meme_number = today_memes[user_id][1]
    logger.info(f'{meme_category.name = }, {meme_number = }')
    if isinstance(meme_category, StickerCategory):
        await context.bot.send_message(
            update.message.chat_id,
            f'{update.message.from_user.name}, твое состояние сегодня\n\nРедкость: стикер\n🌝🌑🌑🌑🌑'
        )
        await context.bot.send_sticker(
            update.message.chat_id,
            meme_category.memes[meme_number])
    elif isinstance(meme_category, ImageCategory):
        await context.bot.send_message(
            update.message.chat_id,
            f'{update.message.from_user.name}, {meme_category.description}'
        )
        await context.bot.send_photo(
            update.message.chat_id,
            f'res/images/{meme_category.name}/{meme_category.memes[meme_number]}'
        )
    else:
        logging.warning('unknown category')
