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
  
  def codegen(self, symtab_l, symtab_c, global_tracer):
    # Push arguments to stack
    # Already handled by expression.codegen()
    code = []
    for expression in self.expressions:
      
      code += expression.codegen(symtab_l, symtab_c, global_tracer)
    
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
      self.expression_list = expression_list
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
      self.expression_list = expression_list
      assert tokenizer.tok_advance() == ")"
    else:
      assert False
    print("----- Subroutine Call End -----")

  def codegen(self, symtab_l, symtab_c, global_tracer):
    # subroutineName(expressionlist): function
    # 
    # className|varName.subroutineName(expressionlist): method
    code = []
    num_arguments = 0
    self.subroutine_name = self.subroutine_name.val
    if self.class_or_var_name:
      # Case: className|varName.subroutineName(expressionlist)
      self.class_or_var_name = self.class_or_var_name.val
      # push class instance pointer as first argument
      class_types = global_tracer.compiled_types.class_types
      type_of_class = None
      if self.class_or_var_name in class_types:
        # function/constructor subroutine
        # No need to push object reference
        type_of_class = self.class_or_var_name
        pass
      else:
        # method subroutine
        var_info = variable_lookup(self.class_or_var_name, symtab_l, symtab_c)
        kind = var_info["kind"]
        index = var_info["index"]
        type_of_class = var_info["type"]

        code += [f"push {kind} {index}"]
        num_arguments += 1
      if type(type_of_class) is Terminator:
        type_of_class = type_of_class.val
      # push arguments and then call function
      if self.expression_list:
        code += self.expression_list.codegen(symtab_l, symtab_c, global_tracer)
        num_arguments += len(self.expression_list.expressions)
      
      code += [f"call {type_of_class}.{self.subroutine_name} {num_arguments}"]
    else:
      code += [f"push pointer 0"]
      num_arguments += 1
      # Case: subroutineName(expressionlist): function
      if self.expression_list:
        code += self.expression_list.codegen(symtab_l, symtab_c, global_tracer)
        num_arguments += len(self.expression_list.expressions)
      curr_class_name = global_tracer.curr_class_name
      assert curr_class_name is not None
      code += [f"call {curr_class_name}.{self.subroutine_name} {num_arguments}"]
    
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
      if tokenizer.tok_ahead_next() == "[":
        self.const_or_op = tokenizer.tok_advance()
        print("[Parsing Expression]")
        assert tokenizer.tok_advance() == "["
        assert Expression.is_mytype(tokenizer)
        expression = Expression()
        expression.parse(tokenizer)
        self.expression = expression
        assert tokenizer.tok_advance() == "]"
      elif tokenizer.tok_ahead_next() in ["(", "."]:
        print("[Parsing Subroutine Call]")
        assert SubroutineCall.is_mytype(tokenizer)
        subroutine_call = SubroutineCall()
        subroutine_call.parse(tokenizer)
        self.subroutine_call = subroutine_call
      else:
        print("[Parsing VarName]")
        self.const_or_op = tokenizer.tok_advance()
      
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
    
  def codegen(self, symtab_l, symtab_c, global_tracer):
    code = []
    # Case: subroutineCall
    if self.subroutine_call:
      code += self.subroutine_call.codegen(symtab_l, symtab_c, global_tracer)
      return code
    # Case: varName[expression]
    elif self.const_or_op and self.expression:
      self.const_or_op = self.const_or_op.val
      # Parse Array Indexing
      var_info = variable_lookup(self.const_or_op, symtab_l, symtab_c)
      kind = var_info["kind"]
      index = var_info["index"]
      # varName + codegen(expression) -> offset
      code += [f"push {kind} {index}"]
      code += self.expression.codegen(symtab_l, symtab_c, global_tracer)
      code += ["add"]
      # Set that pointer
      code += ["pop pointer 1"]
      code += ["push that 0"]
      return code
    # Case: (expression)
    elif self.expression and self.const_or_op is None:
      code += self.expression.codegen(symtab_l, symtab_c, global_tracer)
      return code
    # Case: UnaryOp term
    elif self.term and self.const_or_op:
      if type(self.const_or_op) is Terminator:
        self.const_or_op = self.const_or_op.val
      # 1. parse term
      code += self.term.codegen(symtab_l, symtab_c, global_tracer)
      # 2. parse unaryOp
      if self.const_or_op == "-":
        code += ["neg"]
      elif self.const_or_op == "~":
        code += ["not"]
      else:
        raise "Unrecognized unaryOp during code gen for term"
      return code
    # Case: integerConstant, stringConstant, keywordConstant, varName
    elif self.const_or_op and self.term is None and self.expression is None and self.term is None:
      if type(self.const_or_op) is Terminator and self.const_or_op.type == "identifier":
        self.const_or_op = self.const_or_op.val
        # Case: varName
        var_info = variable_lookup(self.const_or_op, symtab_l, symtab_c)
        kind = var_info["kind"]
        index = var_info["index"]
        
        code += [f"push {kind} {index}"]
        return code
      else:
        # Case: Constants
        if self.const_or_op == "true":
          # map to -1
          code += ["push constant 1"]
          code += ["neg"]
        elif self.const_or_op == "false":
          # map to 0
          code += ["push constant 0"]
        elif self.const_or_op == "null":
          # map to 0
          code += ["push constant 0"]
        elif self.const_or_op == "this":
          code += ["push pointer 0"]
        else:
          # Int/Str Constants
          if self.const_or_op.type == "stringConstant":
            self.const_or_op = self.const_or_op.val
            # length of string
            code += [f"push constant {len(self.const_or_op)}"]
            code += [f"call String.new 1"]
            for c in self.const_or_op:
              # push ascii value
              code += [f"push constant {ord(c)}"]
              code += [f"call String.appendChar 2"]
          else:
            self.const_or_op = self.const_or_op.val
            code += [f"push constant {self.const_or_op}"]
          
        return code
    else:
      assert False
      
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
  
  def codegen(self, symtab_l, symtab_c, global_tracer):
    code = []
    # push first term
    code += self.terms[0].codegen(symtab_l, symtab_c, global_tracer)
    
    # from second term on,
    for i in range(1, len(self.terms)):
      # 1. push term
      term = self.terms[i]
      code += term.codegen(symtab_l, symtab_c, global_tracer)
      
      # 2. push op
      op = self.ops[i-1]
      if op == "+":
        code += ["add"]
      elif op == "-":
        code += ["sub"]
      elif op == "*":
        code += ["call Math.multiply 2"]
      elif op == "/":
        code += ["call Math.divide 2"]
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
