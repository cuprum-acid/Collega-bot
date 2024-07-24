import mem
import players_info

from telegram import Update
from telegram.ext import CommandHandler, CallbackContext, ApplicationBuilder, JobQueue

TELEGRAM_BOT_TOKEN = ''


async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
        'Привет! Используй команду /players, чтобы узнать кто сейчас на сервере Minecraft. '
        'Запусти слежку за сервером командой /monitor или останови ее с помощью /monitor_stop '
    )


async def players(update: Update, context: CallbackContext) -> None:
    try:
        online_players = players_info.get_players()
        if online_players is None:
            reply = 'Не удалось получить информацию о игроках.'
        elif online_players:
            reply = f'В данный момент на сервере находятся игроки: {", ".join(online_players)}'
        else:
            reply = 'На сервере в данный момент нет игроков.'
    except Exception as e:
        reply = f"Произошла ошибка при запросе к серверу: {e}"
    await update.message.reply_text(reply)


async def monitor(update: Update, context: CallbackContext) -> None:
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


async def monitor_stop(update: Update, context: CallbackContext) -> None:
    can_stop_job = players_info.monitor_stop(context, update.message.chat_id)
    if can_stop_job:
        await update.message.reply_text('Свободная посещаемость! я не слежу за вами.')
    else:
        await update.message.reply_text('Уже выключено.')


async def collega_taro(update: Update, context: CallbackContext) -> None:
    await mem.get_mem(update, context)


def main() -> None:
    application = ApplicationBuilder().job_queue(JobQueue()).token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("monitor", monitor))
    application.add_handler(CommandHandler("monitor_stop", monitor_stop))
    application.add_handler(CommandHandler("players", players))
    application.add_handler(CommandHandler("collega_taro", collega_taro))
    application.run_polling()


if __name__ == '__main__':
    main()
