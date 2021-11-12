from datetime import datetime
import json
import importlib
import inspect
import time
import os
from typing import Callable, Tuple


def read_configuration(path: str) -> dict:
  with open(path) as config:
    return json.load(config)


def translate_path_to_module(path: str) -> str:
  return path.replace("/", ".").rstrip(".py")


def load_command_dispatch(path: str) -> Tuple[Callable, Callable]:
  module = importlib.import_module(translate_path_to_module(path))

  assert (gen_dispatch := getattr(
      module, "generic_command_dispatch", None)) is not None,   \
    f"Generic dispatch function under {path!r} must be named "  \
     "`generic_command_dispatch`"

  return gen_dispatch


def debug_print(*args, **kwargs):
  previous_frame = inspect.currentframe().f_back.f_code
  print(
    time.strftime('(%H:%M:%S)'),
    f"[{previous_frame.co_name}]",
    *args, **kwargs
    )


def regenerate_command_listing(cache: dict, path: str):
  cache.clear()
  for command in os.listdir(path):
    module = importlib.import_module(
      f"{translate_path_to_module(path)}.{translate_path_to_module(command)}"
      )
    cache[module.__COMMAND__] = importlib.reload(module)


def find_command(cache: dict, command: str):
  return cache.get(command).invoke


def format_date(date: datetime):
  if date is None:
    return "n/a"
    
  partial = date.strftime("%d %b %Y, %I:%M %p")
  days_since = (datetime.now() - date).days
  years_since = days_since // 365

  if not years_since:
    return f"{partial} ({days_since} day(s) ago)"
  return f"{partial} ({years_since} year(s) ago)"