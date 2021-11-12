from logging import currentframe
import string


def null_function(*args, **kwargs):
  return


def is_whitespace(char):
  return char in string.whitespace


def is_string(char):
  return char in "\"`'"


def is_numeric(char):
  return char in string.digits


def is_identifier(char):
  return char in string.ascii_letters
  

def is_escape_code(char):
  return char == '\\'


def concatenate_token(token):
  if isinstance(token[0], int):
    return int(''.join(map(str, token)))
  
  if isinstance(token[0], str):
    return ''.join(token)


def parse_string(content, eol):
  string = ""
  ignore_next_character = False

  while content:
    current_character = content.pop(0)

    if ignore_next_character:
      string += current_character
      ignore_next_character = False
      continue
    
    if is_escape_code(current_character):
      ignore_next_character = True
      continue

    if current_character == eol:
      return string
    
    string += current_character
  
  return False


def parse_command(content):
  content, tokens, current_token = [*content], [], []

  trace_idx = 0
  while content:
    current_character = content.pop(0)
    last_character_type = type(current_token[-1]) if current_token else None

    if is_identifier(current_character):
      if last_character_type is int:
        return (False, f"0:{trace_idx}, identifiers cannot contain integers")

      current_token.append(current_character)
    elif is_whitespace(current_character):
      tokens.append(concatenate_token(current_token))
      current_token.clear()
    elif is_numeric(current_character):
      if last_character_type is str:
        return (False, f"0:{trace_idx}, numerals cannot contain alphabetic " \
                        "letters")

      current_token.append(int(current_character))
    elif is_string(current_character):
      if last_character_type is int:
        return (False, f"0:{trace_idx}, integers cannot precede strings")
      if last_character_type is str:
        return (False, f"0:{trace_idx}, strings/identifiers cannot precede " \
                        "other strings")
      if not (string := parse_string(content, current_character)):
        return (False, f"0:{trace_idx}, failed to parse string")
      
      trace_idx += len(string) + 1
      current_token.append(string)

    trace_idx += 1
  
  if current_token:
    tokens.append(concatenate_token(current_token))

  return (True, tokens)