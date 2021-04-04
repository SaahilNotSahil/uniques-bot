import logging

handler = logging.FileHandler(
    filename='discord.log', encoding='utf-8', mode='a'
)

logger = logging.Logger('discord', level=logging.DEBUG)
logger.addHandler(handler)
