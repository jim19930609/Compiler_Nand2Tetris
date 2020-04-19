import copy

class Terminator(object):
  def __init__(self, val, const_type):
    self.val = val
    self.type = const_type
  
  def is_integerConstant(self):
    return self.type == "integerConstant"
  
  def is_stringConstant(self):
    return self.type == "stringConstant"
    
  def is_identifier(self):
    return self.type == "identifier"

  def __repr__(self):
    return f"{self.val}(\"{self.type}\")"    
  
  def __str__(self):
    return f"{self.val}(\"{self.type}\")"    

# Tokenizer:
# 1. original file content
# 2. cursor (never stop at a space)
# 3. look_ahead()
# 4. consume()
class Tokenizer(object):
  def __init__(self):
    self.content = ""
    self.cursor  = 0

  def is_tok_keyword(self, tok):
    if tok in ["class", "constructor", "function", "method", 
               "field", "static", "var", "int", "char", "boolean", 
               "void", "true", "false", "null", "this", "let", "do", 
               "if", "else", "while", "return"]:
      return True
    return False
  
  def is_tok_symbol(self, tok):
    if tok in ["{", "}", "(", ")", "[", "]", ".", ",", ";", "+", "-", "*", "/", "&", "|", "<", ">", "=", "~"]:
      return True
    return False
    
  def is_tok_string(self, tok):
    if tok[0] == "\"" and tok[-1] == "\"":
      return True
    return False

  def is_tok_integer(self, tok):
    try:
      int(tok)
      return True
    except ValueError:
      return False
    
  def is_tok_identifier(self, tok):
      # Is identifier
      legal_identifier_letters = [v for v in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz_0123456789"]
      ilegal_start_letter = [v for v in "0123456789"]
      if tok[0] in ilegal_start_letter:
        return False
      for char in tok:
        if char not in legal_identifier_letters:
          return False
      return True

  def remove_space(self, cursor):
    cursor_tmp = copy.copy(cursor)
    if cursor_tmp >= len(self.content):
      print("Finished parsing file")
      return cursor_tmp
    
    while self.content[cursor_tmp] in [" ", "\n", "/"]:
      if self.content[cursor_tmp] == "/" and self.content[cursor_tmp+1] == "/":
        cursor_tmp = self.erase_comments_short(cursor_tmp)
        continue
      if self.content[cursor_tmp] == "/" and self.content[cursor_tmp+1] == "*":
        cursor_tmp = self.erase_comments_long(cursor_tmp)
        continue
      
      cursor_tmp += 1
      if cursor_tmp >= len(self.content):
        print("Finished parsing file")
        return cursor_tmp
    return cursor_tmp

  def erase_comments_short(self, cursor):
    assert self.content[cursor] == "/" and self.content[cursor+1] == "/"
    while self.content[cursor] != "\n":
      cursor += 1
    
    # Skip "\n"
    cursor += 1
    return cursor

  def erase_comments_long(self, cursor):
    assert self.content[cursor] == "/" and self.content[cursor+1] == "*"
    while True:
      if self.content[cursor] == "*" and self.content[cursor+1] == "/":
        cursor += 2
        break
      cursor += 1
    
    return cursor

  ## Read methods ##
  #  tok_ahead: do not consume
  #  tok_consume
  def get_tok(self, extern_cursor):
    # current cursor to next space
    # do not update cursor
    # determine and return tok
    assert extern_cursor < len(self.content)
    tok = ""
    cursor = self.remove_space(extern_cursor)
    content = self.content
    
    char = content[cursor]
    is_string = char == "\""
    if is_string:
      tok += char
      cursor += 1

    while True:
      char = content[cursor]
      if is_string:
        if char == "\"":
          tok += char
          cursor += 1
          break
      elif char in [" ", "\n"]:
        break
      elif self.is_tok_symbol(char):
        if len(tok) == 0:
          tok = char
          cursor += 1
        break
      elif char == "/" and content[cursor+1] == "/":
        break
      elif char == "/" and content[cursor+1] == "*":
        break
      
      tok += char
      cursor += 1
    
    cursor = self.remove_space(cursor)
    
    ret = None
    if self.is_tok_keyword(tok):
      ret = tok
    elif self.is_tok_symbol(tok):
      ret = tok
    elif self.is_tok_string(tok):
      ret = Terminator(tok, "stringConstant")
    elif self.is_tok_integer(tok):
      ret = Terminator(int(tok), "integerConstant")
    elif self.is_tok_identifier(tok):
      ret = Terminator(tok, "identifier")
    else:
      assert False

    return ret, cursor

  def tok_ahead_next(self):
    tok, cursor = self.get_tok(self.cursor)
    tok, cursor = self.get_tok(cursor)
    
    return tok
    
  ##### User Interface ##### 
  def tok_ahead(self):
    tok, cursor = self.get_tok(self.cursor)
    return tok
    
  def tok_advance(self):
    tok, cursor = self.get_tok(self.cursor)
    self.cursor = cursor
    return tok

  def file_ends(self):
    if self.cursor >= len(self.content) - 1:
      return True
    return False
  
  def load_file(self, filename):
    with open(filename, "r") as f:
      self.content = f.read()
    
    assert len(self.content) > 0
    print(self.content)


if __name__ == "__main__":
  # Test tokenizer
  filename = ""
  tokenizer = Tokenizer(filename)
  while not tokenizer.file_ends():
    print(tokenizer.tok_ahead)
    print(tokenizer.tok_advance)
