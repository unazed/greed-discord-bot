from lib import utils
from typing import Callable
import discord


class DiscordClient(discord.Client):
  def __init__(self, configuration: dict, *,
      log_function: Callable=utils.null_function):
    
    self.configuration = configuration
    self.prefix = configuration['bot']['prefix']
    self.log = log_function

    self.dispatch_fn = None

    assert "token" in self.configuration['bot'], \
      "Configuration must define the bot's token"

    intents = discord.Intents.default()
    intents.members = True
    super().__init__(intents=intents)
    self.log("initialized bot, ready to run")

  def run(self):
    self.log("beginning to run bot...")
    super().run(self.configuration['bot']['token'])
  
  def set_command_dispatch(self, dispatch_fn: Callable):
    self.log("dispatch function has been configured")
    self.dispatch_fn = dispatch_fn
  
  async def on_ready(self):
    self.log("bot is in a ready state, awaiting messages...")
    self.log("invite the bot with the following link: "                 \
      f"https://discord.com/oauth2/authorize?client_id={self.user.id}"  \
       "&permissions=8&scope=bot")

  async def alert_user(self, channel: discord.TextChannel, user: discord.User,
      message: str):
    await channel.send(f"<@{user.id}>, {message}")

  async def on_message(self, message: discord.Message):
    if self.dispatch_fn is None:
      return
    
    content: str = message.content
    channel: discord.TextChannel = message.channel
    user: discord.User = message.author

    if not content.startswith(self.prefix):
      return

    result, content = utils.parse_command(content.lstrip(self.prefix))
    if not result:
      await self.alert_user(channel, user, content)
      return
    
    command, *args = content
    await self.dispatch_fn(
      self.configuration['commands']['modules']['auto_reload'],
      self, message, command, args)
