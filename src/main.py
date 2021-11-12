from lib.client import DiscordClient
from src import utils


if __name__ == "__main__":
  client = DiscordClient(
    configuration=(config := utils.read_configuration("config.json")),
    log_function=utils.debug_print
    )

  generic_dispatch = utils.load_command_dispatch(
    config['commands']['dispatch']['load_from']
    )

  client.set_command_dispatch(
    utils.load_command_dispatch(
      config['commands']['dispatch']['load_from']
      )
    )

  client.run()
