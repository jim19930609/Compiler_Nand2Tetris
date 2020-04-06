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
    

# Tokenizer:
# 1. original file content
# 2. cursor (never stop at a space)
# 3. look_ahead()
# 4. consume()
class Tokenizer(object):
  def __init__(self):
    self.content = ""
    self.cursor  = 0

  @staticmethod
  def is_tok_keywork(self, tok):
    if tok in ["class", "constructor", "function", "method", 
               "field", "static", "var", "int", "char", "boolean", 
               "void", "true", "false", "null", "this", "let", "do", 
               "if", "else", "while", "return"]:
      return True
    return False
  
  @staticmethod
  def is_tok_symbol(self, tok):
    if tok in ["{", "}", "(", ")", "[", "]", ".", ",", ";", "+", "-", "*", "/", "&", "|", "<", ">", "=", "~"]:
      return True
    return False
    
  @staticmethod
  def is_tok_string(self, tok):
    if tok[0] == "\"" and tok[-1] == "\"":
      return True
    return False

  @staticmethod
  def is_tok_integer(self, tok):
    try:
      int(tok)
      return True
    except ValueError:
      return False
    
  @staticmethod
  def is_tok_identifier(self, tok):
      # Is identifier
      legal_identifier_letters = [v for v in "abcdefghijklmnopqrstuvwxyz_0123456789"]
      ilegal_start_letter = [v for v in "0123456789"]
      if tok[0] in ilegal_start_letter:
        return False
      for char in tok:
        if char not in legal_identifier_letters:
          return False
      return True

  def remove_space(self, cursor):
    cursor_tmp = copy.copy(cursor)
    while self.content[cursor_tmp] == " ":
      cursor_tmp += 1
    return cursor_tmp

  ## Read methods ##
  #  tok_ahead: do not consume
  #  tok_consume
  def get_tok(self):
    # current cursor to next space
    # do not update cursor
    # determine and return tok
    assert not file_ends()
    tok = ""
    cursor = self.remove_space(self.cursor)
    content = self.content
    while True:
      char = content[cursor]
      if char == " ":
        break
      
      if is_tok_symbol(char):
        if len(tok) == 0:
          tok = char
          cursor += 1
        break
      
      tok += char
      cursor += 1
    
    cursor = self.remove_space(self.cursor)
    
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

  ##### User Interface ##### 
  def tok_ahead(self):
    tok, cursor = self.get_tok()
    return tok
    
  def tok_advance(self):
    tok, cursor = self.get_tok()
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


if __name__ == "__main__":
  # Test tokenizer
  filename = ""
  tokenizer = Tokenizer(filename)
  while not tokenizer.file_ends():
    print(tokenizer.tok_ahead)
    print(tokenizer.tok_advance)
