from lib.tokenizer import Terminator

Ops = ["+", "-", "*", "/", "&", "|", "<", ">", "="]
UnaryOps = ["-", "~"]
KeywordConstants = ["true", "false", "null", "this"]

class ExpressionList(object):
  @staticmethod
  def is_mytype(tokenizer):
    return True
    
  def __init__(self):
    self.expressions = []
  
  def parse(self, tokenizer):
    print("----- Expression List Start -----")
    while True:
      if not Expression.is_mytype(tokenizer):
        break
      else:
        print("[Parsing Expression]")
        expression = Expression()
        expression.parse(tokenizer)
        self.expressions.append(expression)
        if tokenizer.tok_ahead() == ",":
          tokenizer.tok_advance()
        else:
          break
    print("----- Expression List End -----")


class SubroutineCall(object):
  @staticmethod
  def is_mytype(tokenizer):
    tok_first = tokenizer.tok_ahead()
    tok_second = tokenizer.tok_ahead_next()
    if type(tok_first) is not Terminator or tok_first.type != "identifier": return False
    if tok_second not in ["(", "."]: return False
    return True
  
  def __init__(self):
    self.subroutine_name = None
    self.expression_list = None
    self.class_or_var_name = None

  def parse(self, tokenizer):
    print("----- Subroutine Call Start -----")
    tok = tokenizer.tok_advance()
    assert type(tok) is Terminator and tok.type == "identifier"
    if tokenizer.tok_ahead() == "(":
      print("[Parsing ExpressionList case 0]")
      assert tokenizer.tok_advance() == "("
      self.subroutine_name = tok
      print(self.subroutine_name)
      assert ExpressionList.is_mytype(tokenizer)
      expression_list = ExpressionList()
      expression_list.parse(tokenizer)
      self.expression_list_l = expression_list
      assert tokenizer.tok_advance() == ")"
    elif tokenizer.tok_ahead() == ".":
      print("[Parsing ExpressionList case 1]")
      assert tokenizer.tok_advance() == "."
      self.class_or_var_name = tok
      
      tok = tokenizer.tok_advance()
      assert type(tok) is Terminator and tok.type == "identifier"
      self.subroutine_name = tok
      print(self.subroutine_name)
      assert tokenizer.tok_advance() == "("
      assert ExpressionList.is_mytype(tokenizer)
      expression_list = ExpressionList()
      expression_list.parse(tokenizer)
      self.expression_list_l = expression_list
      assert tokenizer.tok_advance() == ")"
    print("----- Subroutine Call End -----")
    

class Term(object):
  @staticmethod
  def is_mytype(tokenizer):
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
    print("----- Term Start -----")
    tok = tokenizer.tok_ahead()
    print(tok)
    if type(tok) is Terminator and tok.type in ["integerConstant", "stringConstant"]:
      self.const_or_op = tokenizer.tok_advance()
    elif type(tok) is Terminator and tok.type == "identifier":
      self.const_or_op = tokenizer.tok_advance()
      if tokenizer.tok_ahead() == "[":
        print("[Parsing Expression]")
        assert tokenizer.tok_advance() == "["
        assert Expression.is_mytype(tokenizer)
        expression = Expression()
        expression.parse(tokenizer)
        self.expression = expression
        assert tokenizer.tok_advance() == "]"
      if tokenizer.tok_ahead() in ["(", "."]:
        print("[Parsing Subroutine Call]")
        assert tokenizer.tok_advance() in ["(", "."]
        assert SubroutineCall.is_mytype(tokenizer)
        subroutine_call = SubroutineCall()
        subroutine_call.parse(tokenizer)
        self.subroutine_call = subroutine_call
      
    elif tok in KeywordConstants:
      self.const_or_op = tokenizer.tok_advance()
    elif tok == "(":
      print("[Parsing Expression")
      assert tokenizer.tok_advance() == "("
      assert Expression.is_mytype(tokenizer)
      expression = Expression()
      expression.parse(tokenizer)
      self.expression = expression
      assert tokenizer.tok_advance() == ")"
    elif tok in UnaryOps: 
      print("[Parsing UnaryOps")
      self.const_or_op = tokenizer.tok_advance()
      assert Term.is_mytype(tokenizer)
      term = Term()
      term.parse(tokenizer)
      self.term = term
    print("----- Term End -----")


class Expression(object):
  @staticmethod
  def is_mytype(tokenizer):
    tok = tokenizer.tok_ahead()
    if Term.is_mytype(tokenizer):
      return True
    return False

  def __init__(self):
    self.terms = []
    self.ops = []

  def parse(self, tokenizer):
    print("----- Expression Start -----")
    print("[Parsing Term]")
    assert Term.is_mytype(tokenizer)
    term = Term()
    term.parse(tokenizer)
    self.terms.append(term)
    
    while True:
      if tokenizer.tok_ahead() not in Ops:
        break
      print("[Parsing Term]")
      self.ops.append(tokenizer.tok_advance())
      assert Term.is_mytype(tokenizer)
      term = Term()
      term.parse(tokenizer)
      self.terms.append(term)
    
    print("----- Expression End -----")
    
