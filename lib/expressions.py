from lib.tokenizer import Terminator
from lib.helper import variable_lookup

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
  
  def codegen(self, symtab_l, symtab_c):
    # Push arguments to stack
    # Already handled by expression.codegen()
    code = []
    for expression in self.espressions:
      code += expression.codegen(symtab_l, symtab_c)
    
    return code
    
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

  def codegen(self, symtab_l, symtab_c):
    # subroutineName(expressionlist): function
    # 
    # className|varName.subroutineName(expressionlist): method
    code = []
    num_arguments = 0
    if self.class_or_var_name:
      # push class instance pointer as first argument
      var_info = variable_lookup(self.class_or_var_name, symtab_l, symtab_c)
      code += ["push {var_info[\"kind\"]} {var_info[\"index\"]}"]
      num_arguments += 1
    
    # push arguments and then call function
    code += self.expression_list.code_gen()
    num_arguments += len(self.expression_list(symtab_l, symtab_c))
    code += [f"call {self.subroutine_name} {num_arguments}"]
    
    return code

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
    
  def codegen(symtab_l, symtab_c):
    code = []
    # Case: subroutineCall
    if self.subroutine_call:
      code += self.subroutine_call.codegen(symtab_l, symtab_c)
      return code
    # Case: varName[expression]
    if self.const_or_op and self.expression:
      # Parse Array Indexing
      var_info = variable_lookup(self.const_or_op, symtab_l, symtab_c)
      # varName + codegen(expression) -> offset
      code += ["push {var_info[\"kind\"]} {var_info[\"index\"]}"]
      code += self.espression.codegen(symtab_l, symtab_c)
      code += ["add"]
      # Set that pointer
      code += ["pop pointer 1"]
      code += ["push that 0"]
    return code
    # Case: (expression)
    if self.expression and self.const_or_op is None:
      code += self.expression.codegen(symtab_l, symtab_c)
      return code
    # Case: UnaryOp term
    if self.term and self.const_or_op:
      # 1. parse term
      code += self.term.codegen(symtab_l, symtab_c)
      # 2. parse unaryOp
      if self.const_or_op == "-":
        code += ["neg"]
      elif self.const_or_op == "~":
        code += ["not"]
      else:
        raise "Unrecognized unaryOp during code gen for term"
      return code
    # Case: integerConstant, stringConstant, keywordConstant, varName
    if self.const_or_op and self.term is None and self.expression is None and self.term is None:
      if type(self.const_or_op) is Terminator and self.const_or_op.type == "identifier":
        # Case: varName
        var_info = variable_lookup(self.const_or_op, symtab_l, symtab_c)
        code += ["push {var_info[\"kind\"]} {var_info[\"index\"]}"]
        return code
      else:
        # Case: Constants
        if self.const_or_op == "true":
          # map to -1
          code += ["push 1"]
          code += ["neg"]
        elif self.const_or_op == "false":
          # map to 0
          code += ["push 0"]
        elif self.const_or_op == "null":
          # map to 0
          code += ["push 0"]
        elif self.const_or_op == "this":
          code += ["push this 0"]
        else:
          # Int/Str Constants
          code += [f"push {self.const_or_op}"]
        return code

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
  
  def codegen(self, symtab_l, symtab_c):
    code = []
    # push first term
    code += self.terms[0].codegen(symtab_l, symtab_c)
    
    # from second term on,
    for i in range(1, len(self.terms)):
      # 1. push term
      term = self.terms[i]
      code += term.codegen(symtab_l, symtab_c)
      
      # 2. push op
      op = self.ops[i]
      if op == "+":
        code += ["add"]
      elif op == "-":
        code += ["sub"]
      elif op == "*":
        code += ["mul"]
      elif op == "/":
        code += ["div"]
      elif op == "&":
        code += ["and"]
      elif op == "|":
        code += ["or"]
      elif op == "<":
        code += ["lt"]
      elif op == ">":
        code += ["gt"]
      elif op == "=":
        code += ["eq"]
      else:
        raise "Unrecognized op during codegen for term"
      
    return code
