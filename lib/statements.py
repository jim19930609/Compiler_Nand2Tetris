from tokenizer import Terminator

class LetStatement(object):
  @staticmethod
  def is_mytype(self, tokenizer):
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
    keyword = tokenizer.tok_advance()
    assert keyword == "let"

    # Parse varName
    name = tokenizer.tok_advance()
    assert type(name) is Terminator
    assert name.type == "identifier"
    self.varname = name
    
    # Parse left expression
    symbol = tokenizer.tok_advance()
    if symbol == "[":
      assert Expression.is_mytype(tokenizer)
      expression = Expression()
      expression.parse(tokenizer)
      self.expression_l = expression
      assert tokenizer.tok_advance() == "]"
      assert tokenizer.tok_advance() == "="
    else:
      assert symbol == "="
    
    # Parse Right expression
    assert Expression.is_mytype(tokenizer)
    expression = Expression()
    expression.parse(tokenizer)
    self.expression_r = expression
    assert tokenizer.tok_advance() == ";"
    

class IfStatement(object):
  @staticmethod
  def is_mytype(self, tokenizer):
    tok = tokenizer.tok_ahead()
    if tok == "if":
      return True
    return False
  
  def __init__(self):
    self.expression = None
    self.if_statements = None
    self.else_statements = None
    
  def parse(self, tokenizer):
    # if (expression) {statements} (else {statements})?
    keyword = tokenizer.tok_advance()
    assert keyword == "if"
    
    # Parse expression
    assert tokenizer.tok_advance() == "("
    assert Expression.is_mytype(tokenizer)
    expression = Expression()
    expression.parse(tokenizer)
    self.expression = expression
    assert tokenizer.tok_advance() == ")"

    # Parse If Statements
    assert tokenizer.tok_advance() == "{"
    statements = Statements()
    statements.parse(tokenizer)
    self.if_statements = statements
    assert tokenizer.tok_advance() == "}"
    
    # Parse Else Statements
    if tokenizer.tok_ahead == "else":
      assert tokenizer.tok_advance() == "else"
      assert tokenizer.tok_advance() == "{"
      statements = Statements()
      statements.parse(tokenizer)
      self.else_statements = statements
      assert tokenizer.tok_advance() == "}"
      

class WhileStatement(object):
  @staticmethod
  def is_mytype(self, tokenizer):
    tok = tokenizer.tok_ahead()
    if tok == "while":
      return True
    return False

  def __init__(self):
    self.expression = None
    self.statements = None
    
  def parse(self, tokenizer):
    # while (expression) {statements}
    assert tokenizer.tok_advance() == "while"
    
    # Parse expression
    assert tokenizer.tok_advance() == "("
    assert Expression.is_mytype(tokenizer)
    expression = Expression()
    expression.parse(tokenizer)
    self.expression = expression
    assert tokenizer.tok_advance() == ")"

    # Parse If Statements
    assert tokenizer.tok_advance() == "{"
    statements = Statements()
    statements.parse(tokenizer)
    self.if_statements = statements
    assert tokenizer.tok_advance() == "}"


class DoStatement(object):
  @staticmethod
  def is_mytype(self, tokenizer):
    tok = tokenizer.tok_ahead()
    if tok == "do":
      return True
    return False

  def __init__(self):
    self.subroutine_call = None
  
  def parse(self, tokenizer):
    assert tokenizer.tok_advance() == "do"
    assert SubroutineCall.is_mytype(tokenizer)
    sub_call = SubroutineCall()
    sub_call.parse(tokenizer)
    self.subroutine_call = sub_call
    assert tokenizer.tok_advance() == ";"


class ReturnStatement(object):
  @staticmethod
  def is_mytype(self, tokenizer):
    tok = tokenizer.tok_ahead()
    if tok == "return":
      return True
    return False

  def __init__(self):
    self.expression = None
  
  def parse(self, tokenizer):
    # return expression? ;
    assert tokenizer.tok_advance() == "return"
    
    if Expression.is_mytype(tokenizer):
      expression = Expression()
      expression.parse(tokenizer)
      self.expression = expression
    
    assert tokenizer.tok_advance() == ";"


class Statement(object):
  @staticmethod
  def is_mytype(self, tokenizer):
    if LetStatement.is_mytype(tomenizer):
      return True
    if IfStatement.is_mytype(tomenizer):
      return True
    if WhileStatement.is_mytype(tomenizer):
      return True
    if DoStatement.is_mytype(tomenizer):
      return True
    if ReturnStatement.is_mytype(tomenizer):
      return True
    return False

  def __init__(self):
    self.statement = None

  def parse(self, tokenizer):
    if LetStatement.is_mytype(tomenizer):
      statement = LetStatement()
      statement.parse(tokenizer)
      self.statement = statement
    if IfStatement.is_mytype(tomenizer):
      statement = IfStatement()
      statement.parse(tokenizer)
      self.statement = statement
    if WhileStatement.is_mytype(tomenizer):
      statement = WhileStatement()
      statement.parse(tokenizer)
      self.statement = statement
    if DoStatement.is_mytype(tomenizer):
      statement = DoStatement()
      statement.parse(tokenizer)
      self.statement = statement
    if ReturnStatement.is_mytype(tomenizer):
      statement = ReturnStatement()
      statement.parse(tokenizer)
      self.statement = statement
    

class Statements(object):
  @staticmethod
  def is_mytype(self, tokenizer):
    return True
  
  def __init__(self):
    self.statements = []
  
  def parse(self, tokenizer):
    while True:
      if Statement.is_mytype(tokenizer.tok_ahead()):
        statement = Statement()
        statement.parse(tokenizer)
        self.statements.append(statement)
      else:
        break
