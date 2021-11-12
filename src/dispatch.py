from typing import Tuple, Type, Union
from lib.client import DiscordClient
from src import utils
import time
import discord


generic_command_cache = {}
last_cache_update = None


def update_command_cache(bot: DiscordClient):
  global last_cache_update
  bot.log("updating command cache...")
  utils.regenerate_command_listing(
    generic_command_cache,
    bot.configuration['directories']['commands']
    )
  last_cache_update = time.time()


async def generic_command_dispatch(is_dynamic: bool, bot: DiscordClient,
    message: discord.Message, command: str, args: Tuple[Union[str, int]]):

  if not generic_command_cache:
    bot.log("populating command cache for the first time...")
    update_command_cache(bot)
  elif is_dynamic:
    if time.time() - last_cache_update \
        >= bot.configuration['commands']['modules']['reload_every']:
      update_command_cache(bot)
        
  command_fn = utils.find_command(generic_command_cache, command)
  
  if command_fn is None:
    return await bot.alert_user(message.channel, message.author,
        "no such command exists")

  try:
    await command_fn(bot, message, *args)
  except TypeError as exc:
    return await bot.alert_user(message.channel, message.author,
        f"invalid parameters for command `{command}`")
