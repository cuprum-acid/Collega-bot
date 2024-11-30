from __future__ import annotations

import os

from dotenv import load_dotenv
load_dotenv()
from telegram import Update, error
from telegram.ext import CommandHandler, CallbackContext, ApplicationBuilder, JobQueue

from mem import get_mem
from logger import logger
import players_info

TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')


async def check_new_players(context: CallbackContext) -> None:
    global online_players
    current_players = players_info.get_players()
    if not current_players:
        return

    joined_players = set(current_players) - set(online_players)
    quitted_players = set(online_players) - set(current_players)
    online_players = current_players
    if joined_players or quitted_players:
        reply = (f'{"На сервер зашли игроки: " + ", ".join(joined_players) + ". " if joined_players else ""}'
                 f'{"С сервера вышли: " + ", ".join(quitted_players) if quitted_players else ""}')
        await context.bot.send_message(context.job.chat_id, reply)


async def start(update: Update, context: CallbackContext) -> None:
    logger.info(f'"/start" by {update.message.from_user.name}')
    await update.message.reply_text(
        'Привет! Используй команду /players, чтобы узнать кто сейчас на сервере Minecraft. '
        'Запусти слежку за сервером командой /monitor или останови ее с помощью /monitor_stop. '
    )


async def players(update: Update, context: CallbackContext) -> None:
    logger.info(f'"/players" by {update.message.from_user.name}')
    try:
        online_players = players_info.get_players()
        if online_players is None:
            reply = 'Не удалось получить информацию о игроках.'
        elif online_players:
            reply = f'В данный момент на сервере находятся игроки: {", ".join(online_players)}.'
        else:
            reply = 'На сервере в данный момент нет игроков.'
    except Exception as e:
        reply = "Произошла ошибка при запросе к серверу."
        logger.warning(f'{e}')
    logger.info(f'players on the server: {online_players}')
    await update.message.reply_text(reply)


async def monitor(update: Update, context: CallbackContext) -> None:
    logger.info(f'"/monitor" by {update.message.from_user.name}')
    can_start_job = await players_info.monitor(context, update.message.chat_id)
    if can_start_job:
        await update.message.reply_text(
            'Коллеги! Просьба не опаздывать на пары! '
            'Теперь в аудитории я слежу за всеми входящими и выходящими.'
        )
    else:
        await update.message.reply_text(
            'Я уже слежу и скажу, когда что-то случится.'
        )
    logger.info(f'Active jobs: {context.job_queue.jobs()}')


async def monitor_stop(update: Update, context: CallbackContext) -> None:
    logger.info(f'"/monitor_stop" by {update.message.from_user.name}')
    can_stop_job = players_info.monitor_stop(context, update.message.chat_id)
    if can_stop_job:
        await update.message.reply_text('Свободная посещаемость! я не слежу за вами.')
    else:
        await update.message.reply_text('Уже выключено.')
    logger.info(f'Active jobs: {context.job_queue.jobs()}')


async def collega_taro(update: Update, context: CallbackContext) -> None:
    logger.info(f'"/collega_taro" by {update.message.from_user.name}')
    await get_mem(update, context)


def main() -> None:
    application = ApplicationBuilder().job_queue(JobQueue()).token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("monitor", monitor))
    application.add_handler(CommandHandler("monitor_stop", monitor_stop))
    application.add_handler(CommandHandler("players", players))
    application.add_handler(CommandHandler("collega_taro", collega_taro))
    try:
        application.run_polling(close_loop=False)
    except error.TimedOut as exception:
        logger.error(f"{exception}, restarting...")
        main()


if __name__ == '__main__':
    logger.info(f'Loaded .env: {os.environ.values()}')
    main()
