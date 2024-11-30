from __future__ import annotations

from mcstatus import JavaServer
from telegram.ext import CallbackContext
from config import REQUEST_INTERVAL, SERVER_URL
from logger import logger

is_job_running = False
online_players = []
chats_to_notify = set()


server = JavaServer.lookup(SERVER_URL)


def get_players() -> list[str] | None:
    try:
        query = server.query()
        return query.players.names
    except Exception as e:
        logger.warning(f'{e}')


async def check_new_players(context: CallbackContext) -> None:
    global online_players
    current_players = get_players()
    if current_players is None:
        return
    joined_players = set(current_players) - set(online_players)
    quitted_players = set(online_players) - set(current_players)
    online_players = current_players
    if joined_players or quitted_players:
        notification = ''
        if len(joined_players) == 1:
            notification += f'На сервер зашел игрок {joined_players.pop()}.\n'
        elif len(joined_players) > 1:
            notification += f'На сервер зашли игроки {", ".join(joined_players)}.\n'
        if len(quitted_players) == 1:
            notification += f'C сервера вышел игрок {quitted_players.pop()}.'
        elif len(quitted_players) > 1:
            notification += f'С сервера вышли игроки {", ".join(quitted_players)}.'
        for chat in chats_to_notify:
            await context.bot.send_message(chat, notification)


async def monitor(context: CallbackContext, chat_id) -> bool:
    global is_job_running
    if not is_job_running:
        context.job_queue.run_repeating(
            check_new_players,
            interval=REQUEST_INTERVAL,
            name='player_monitor'
        )
        is_job_running = True
    if chat_id in chats_to_notify:
        return False
    else:
        chats_to_notify.add(chat_id)
        logger.info(f'Active jobs: {context.job_queue.jobs()}, {chats_to_notify = }')
        return True


def monitor_stop(context: CallbackContext, chat_id) -> bool:
    global is_job_running
    if chat_id not in chats_to_notify:
        return False
    chats_to_notify.remove(chat_id)
    if not chats_to_notify:
        _remove_job(context, name='player_monitor')
        is_job_running = False
    logger.info(f'Active jobs: {context.job_queue.jobs()}, {chats_to_notify = }')
    return True


def _remove_job(context: CallbackContext, name: str) -> None:
    active_jobs = context.job_queue.jobs()
    for job in active_jobs:
        if job.name == name:
            job.schedule_removal()
            break
    else:
        logger.warning(f'Could not find job with name {name}')
