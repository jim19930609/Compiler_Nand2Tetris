from lib.tokenizer import Terminator
from lib.helper import variable_lookup
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
    
  def codegen(self, symtab_l, symtab_c, global_tracer):
    code = []
    self.varname = self.varname.val
    if self.expression_l:
      # let varName[expression_l] = expression_r
      # Handle Array
      var_info = variable_lookup(self.varname, symtab_l, symtab_c)
      kind = var_info["kind"]
      index = var_info["index"]
      
      code += [f"push {kind} {index}"]
      code += self.expression_l.codegen(symtab_l, symtab_c, global_tracer)
      code += ["add"]
      code += ["pop pointer 1"]
      # Now that points to varName[expression_l]
      code += self.expression_r.codegen(symtab_l, symtab_c, global_tracer)
      # set expression_r to that 0
      code += ["pop that 0"]
      
    else:
      # let varName = expression_r
      code += self.expression_r.codegen(symtab_l, symtab_c, global_tracer)
      # set expression_r to varName
      var_info = variable_lookup(self.varname, symtab_l, symtab_c)
      kind = var_info["kind"]
      index = var_info["index"]
      code += [f"pop {kind} {index}"]
      
    return code
    
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
      
  def codegen(self, symtab_l, symtab_c, global_tracer):
    label_1 = global_tracer.get_label()
    label_2 = global_tracer.get_label()
    label_3 = global_tracer.get_label()
    code = []
    code += [f"(Label {label_1})"]
    code += self.expression.codegen(symtab_l, symtab_c, global_tracer)
    code += ["not"]
    code += [f"if-goto {label_2}"]
    code += self.if_statements.codegen(symtab_l, symtab_c, global_tracer)
    code += [f"goto {label_3}"]
    code += [f"(Label {label_2})"]
    code += self.else_statements.codegen(symtab_l, symtab_c, global_tracer)
    code += [f"(Label {label_3})"]
    


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
 
  def codegen(self, symtab_l, symtab_c, global_tracer):
    label_1 = global_tracer.get_label()
    label_2 = global_tracer.get_label()
    code = []
    code += [f"(Label {label_1})"]
    code += self.expression.codegen(symtab_l, symtab_c, global_tracer)
    code += ["not"]
    code += [f"if-goto {label_2}"]
    code += self.statements.codegen(symtab_l, symtab_c, global_tracer)
    code += [f"goto {label_1}"]
    code += [f"(Label {label_2})"]
     
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
  
  def codegen(self, symtab_l, symtab_c, global_tracer):
    code = self.subroutine_call.codegen(symtab_l, symtab_c, global_tracer)
    # void return: drop return value
    code += ["pop temp 0"]
    return code

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
  
  def codegen(self, symtab_l, symtab_c, global_tracer):
    if self.expression:
      code = self.expression.codegen(symtab_l, symtab_c, global_tracer)
    else:
      # void return
      code = ["push constant 0"]
    code += ["return"]
    return code

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
    elif IfStatement.is_mytype(tokenizer):
      statement = IfStatement()
      statement.parse(tokenizer)
      self.statement = statement
    elif WhileStatement.is_mytype(tokenizer):
      statement = WhileStatement()
      statement.parse(tokenizer)
      self.statement = statement
    elif DoStatement.is_mytype(tokenizer):
      statement = DoStatement()
      statement.parse(tokenizer)
      self.statement = statement
    elif ReturnStatement.is_mytype(tokenizer):
      statement = ReturnStatement()
      statement.parse(tokenizer)
      self.statement = statement
    else:
      assert False

  def codegen(self, symtab_l, symtab_c, global_tracer):
    return self.statement.codegen(symtab_l, symtab_c, global_tracer)
    
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
  
  def codegen(self, symtab_l, symtab_c, global_tracer):
    code = []
    for statement in self.statements:
      code += statement.codegen(symtab_l, symtab_c, global_tracer)
    return code
