from lib.tokenizer import Terminator
from lib.expressions import *

class LetStatement(object):
  @staticmethod
  def is_mytype(tokenizer):
    tok = tokenizer.tok_ahead()
    if tok == "let":
      return True
    return False
  
  def __init__(self):
    self.varname = None
    self.expression_l = None
    self.expression_r = None
  
  def parse(self, tokenizer):
    # let varName ([expression])? = expression;
    print("----- Let Statement Start -----")
    keyword = tokenizer.tok_advance()
    assert keyword == "let"

    # Parse varName
    name = tokenizer.tok_advance()
    assert type(name) is Terminator
    assert name.type == "identifier"
    self.varname = name
    
    print(f"{keyword} {name}")
    # Parse left expression
    symbol = tokenizer.tok_advance()
    if symbol == "[":
      print("[Parsing First Expression]")
      assert Expression.is_mytype(tokenizer)
      expression = Expression()
      expression.parse(tokenizer)
      self.expression_l = expression
      assert tokenizer.tok_advance() == "]"
      assert tokenizer.tok_advance() == "="
    else:
      assert symbol == "="
    
    # Parse Right expression
    print("[Parsing Second Expression]")
    assert Expression.is_mytype(tokenizer)
    expression = Expression()
    expression.parse(tokenizer)
    self.expression_r = expression
    assert tokenizer.tok_advance() == ";"
    
    print("----- Let Statement End -----")
    

class IfStatement(object):
  @staticmethod
  def is_mytype(tokenizer):
    tok = tokenizer.tok_ahead()
    if tok == "if":
      return True
    return False
  
  def __init__(self):
    self.expression = None
    self.if_statements = None
    self.else_statements = None
    
  def parse(self, tokenizer):
    print("----- If Statement Start -----")
    # if (expression) {statements} (else {statements})?
    keyword = tokenizer.tok_advance()
    assert keyword == "if"
    
    print(keyword)
    
    # Parse expression
    print("[Parsing First Expression]")
    assert tokenizer.tok_advance() == "("
    assert Expression.is_mytype(tokenizer)
    expression = Expression()
    expression.parse(tokenizer)
    self.expression = expression
    assert tokenizer.tok_advance() == ")"

    # Parse If Statements
    print("[Parsing If Statement]")
    assert tokenizer.tok_advance() == "{"
    statements = Statements()
    statements.parse(tokenizer)
    self.if_statements = statements
    assert tokenizer.tok_advance() == "}"
    
    # Parse Else Statements
    if tokenizer.tok_ahead() == "else":
      print("[Parsing Else Statement]")
      assert tokenizer.tok_advance() == "else"
      assert tokenizer.tok_advance() == "{"
      statements = Statements()
      statements.parse(tokenizer)
      self.else_statements = statements
      assert tokenizer.tok_advance() == "}"
    
    print("----- If Statement End -----")
      

class WhileStatement(object):
  @staticmethod
  def is_mytype(tokenizer):
    tok = tokenizer.tok_ahead()
    if tok == "while":
      return True
    return False

  def __init__(self):
    self.expression = None
    self.statements = None
    
  def parse(self, tokenizer):
    # while (expression) {statements}
    print("----- While Statement Start -----")
    assert tokenizer.tok_advance() == "while"
    
    # Parse expression
    print("[Parsing First Expression]")
    assert tokenizer.tok_advance() == "("
    assert Expression.is_mytype(tokenizer)
    expression = Expression()
    expression.parse(tokenizer)
    self.expression = expression
    assert tokenizer.tok_advance() == ")"

    # Parse If Statements
    print("[Parsing Second Expression]")
    assert tokenizer.tok_advance() == "{"
    statements = Statements()
    statements.parse(tokenizer)
    self.if_statements = statements
    assert tokenizer.tok_advance() == "}"
    
    print("----- While Statement End -----")


class DoStatement(object):
  @staticmethod
  def is_mytype(tokenizer):
    tok = tokenizer.tok_ahead()
    if tok == "do":
      return True
    return False

  def __init__(self):
    self.subroutine_call = None
  
  def parse(self, tokenizer):
    print("----- Do Statement Start -----")
    assert tokenizer.tok_advance() == "do"
    assert SubroutineCall.is_mytype(tokenizer)
    print("[Parsing Subroutine Call]")
    sub_call = SubroutineCall()
    sub_call.parse(tokenizer)
    self.subroutine_call = sub_call
    assert tokenizer.tok_advance() == ";"
    print("----- Do Statement End -----")


class ReturnStatement(object):
  @staticmethod
  def is_mytype(tokenizer):
    tok = tokenizer.tok_ahead()
    if tok == "return":
      return True
    return False

  def __init__(self):
    self.expression = None
  
  def parse(self, tokenizer):
    # return expression? ;
    print("----- Return Statement Start -----")
    assert tokenizer.tok_advance() == "return"
    
    if Expression.is_mytype(tokenizer):
      print("[Parsing Expression]")
      expression = Expression()
      expression.parse(tokenizer)
      self.expression = expression
    
    assert tokenizer.tok_advance() == ";"
    print("----- Return Statement End -----")


class Statement(object):
  @staticmethod
  def is_mytype(tokenizer):
    if LetStatement.is_mytype(tokenizer):
      print("[Parsing Let Statement]")
      return True
    if IfStatement.is_mytype(tokenizer):
      print("[Parsing If Statement]")
      return True
    if WhileStatement.is_mytype(tokenizer):
      print("[Parsing While Statement]")
      return True
    if DoStatement.is_mytype(tokenizer):
      print("[Parsing Do Statement]")
      return True
    if ReturnStatement.is_mytype(tokenizer):
      print("[Parsing Return Statement]")
      return True
    return False

  def __init__(self):
    self.statement = None

  def parse(self, tokenizer):
    if LetStatement.is_mytype(tokenizer):
      statement = LetStatement()
      statement.parse(tokenizer)
      self.statement = statement
    if IfStatement.is_mytype(tokenizer):
      statement = IfStatement()
      statement.parse(tokenizer)
      self.statement = statement
    if WhileStatement.is_mytype(tokenizer):
      statement = WhileStatement()
      statement.parse(tokenizer)
      self.statement = statement
    if DoStatement.is_mytype(tokenizer):
      statement = DoStatement()
      statement.parse(tokenizer)
      self.statement = statement
    if ReturnStatement.is_mytype(tokenizer):
      statement = ReturnStatement()
      statement.parse(tokenizer)
      self.statement = statement
    

class Statements(object):
  @staticmethod
  def is_mytype(tokenizer):
    return True
  
  def __init__(self):
    self.statements = []
  
  def parse(self, tokenizer):
    while True:
      if Statement.is_mytype(tokenizer):
        statement = Statement()
        statement.parse(tokenizer)
        self.statements.append(statement)
      else:
        break
