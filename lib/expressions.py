from tokenizer import Terminator

Ops = ["+", "-", "*", "/", "&", "|", "<", ">", "="]
UnaryOps = ["-", "~"]
KeywordConstants = ["true", "false", "null", "this"]

class ExpressionList(object):
  @staticmethod
  def is_mytype(self, tokenizer):
    return True
    
  def __init__(self):
    self.expressions = []
  
  def parse(self, tokenizer):
    while True:
      if not Expression.is_mytype(tokenizer):
        break
      else:
        expression = Espression()
        expression.parse(tokenizer)
        self.expressions.append(expression)
        if tokenizer.tok_ahead() == ",":
          tokenizer.tok_advance()
        else:
          break


class SubroutineCall(object):
  @staticmethod
  def is_mytype(self, tokenizer):
    tok = tokenizer.tok_ahead()
    if type(tok) is Terminator and tok.type == "identifier": return True
    return False
  
  def __init__(self):
    self.subroutine_name = None
    self.expression_list = None
    self.class_or_var_name = None

  def parse(self, tokenizer):
    tok = tokenizer.tok_advance()
    assert type(tok) is Terminator and tok.type == "identifier"
    if tokenizer.tok_ahead() == "(":
      assert tokenizer.tok_advance() == "("
      self.subroutine_name = tok
      assert ExpressionList.is_mytype(tokenizer)
      expression_list = EspressionList()
      expression_list.parse(tokenizer)
      self.expression_list_l = expression_list
      assert tokenizer.tok_advance() == ")"
    elif tokenizer.tok_ahead() == ".":
      assert tokenizer.tok_advance() == "."
      self.class_or_var_name = tok
      
      tok = tokenizer.tok_advance()
      assert type(tok) is Terminator and tok.type == "identifier"
      self.subroutine_name = tok
      
      assert tokenizer.tok_advance() == "("
      assert ExpressionList.is_mytype(tokenizer)
      expression_list = EspressionList()
      expression_list.parse(tokenizer)
      self.expression_list_l = expression_list
      assert tokenizer.tok_advance() == ")"
    

class Term(object):
  @staticmethod
  def is_mytype(self, tokenizer):
    tok = tokenizer.tok_ahead()
    if type(tok) is Terminator:
      if tok.type == "integerConstant": return True
      if tok.type == "stringConstant": return True
      if tok.type == "identifier": return True
      return False
    elif tok in KeywordConstants: return True
    elif tok == "(": return True
    elif tok in UnaryOps: return True
    elif SubroutineCall.is_mytype(tokenizer): return True
    return False
  
  def __init__(self):
    self.const_or_op = None
    self.expression = None
    self.subroutine_call = None
    self.term = None
  
  def parse(self, tokenizer):
    tok = tokenizer.tok_ahead()
    if type(tok) is Terminator and tok.type in ["integerConstant", "stringConstant"]:
      self.const_or_op = tokenizer.tok_advance()
    elif type(tok) is Terminator and tok.type == "identifier":
      self.const_or_op = tokenizer.tok_advance()
      if tokenizer.tok_ahead() == "[":
        assert tokenizer.tok_advance() == "["
        assert Expression.is_mytype(tokenizer)
        expression = Expression()
        expression.parse(tokenizer)
        self.expression = expresssion
        assert tokenizer.tok_advance() == "]"
      if tokenizer.tok_ahead() == "(":
        assert tokenizer.tok_advance() == "("
        assert SubroutineCall.is_mytype(tokenizer)
        subroutine_call = SubroutineCall()
        subroutine_call.parse(tokenizer)
        self.subroutine_call = subroutine_call
      
    elif tok in KeywordConstants:
      self.const_or_op = tokenizer.tok_advance()
    elif tok == "(":
      assert tokenizer.tok_advance() == "("
      assert Expression.is_mytype(tokenizer)
      expression = Expression()
      expression.parse(tokenizer)
      self.expression = expresssion
      assert tokenizer.tok_advance() == ")"
    elif tok in UnaryOps: 
      self.const_or_op = tokenizer.tok_advance()
      assert Term.is_mytype(tokenizer)
      term = Term()
      term.parse(tokenizer)
      self.term = term


class Expression(object):
  @staticmethod
  def is_mytype(self, tokenizer):
    tok = tokenizer.tok_ahead()
    if Term.is_mytype(tokenizer):
      return True
    return False

  def __init__(self):
    self.terms = []
    self.ops = []

  def parse(self, tokenizer):
    assert Term.is_mytype(tokenizer)
    term = Term()
    term.parse(tokenizer)
    self.terms.append(term)
    
    while True:
      if tokenizer.tok_ahead() not in Ops:
        break
    
      self.ops.append(tokenizer.tok_advance())
      assert Term.is_mytype(tokenizer)
      term = Term()
      term.parse(tokenizer)
      self.terms.append(term)
      
