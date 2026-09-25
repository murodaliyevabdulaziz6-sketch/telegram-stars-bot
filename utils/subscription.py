import logging
from typing import Tuple, List, Dict, Any
from aiogram import Bot
from database.db import db

logger = logging.getLogger(__name__)

async def check_user_subscription(bot: Bot, user_id: int) -> Tuple[bool, List[Dict[str, Any]]]:
    """
    Checks if a user is subscribed to all active mandatory channels.
    Returns: (is_subscribed, list_of_unsubscribed_channels)
    """
    channels = await db.get_active_channels()
    if not channels:
        return True, []

    unsubscribed = []
    for ch in channels:
        ch_id = ch["channel_id"]
        try:
            member = await bot.get_chat_member(chat_id=ch_id, user_id=user_id)
            if member.status not in ["creator", "administrator", "member", "restricted"]:
                unsubscribed.append(ch)
        except Exception as e:
            logger.warning(f"Could not verify subscription for {ch_id}: {e}")
            # If bot cannot check or bot is not admin in that channel, do not block user unjustly,
            # but if it's explicitly 'user not found' or 'chat not found', log it.
            pass

    return len(unsubscribed) == 0, unsubscribed
