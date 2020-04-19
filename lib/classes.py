from lib.tokenizer import Terminator
from lib.statements import Statements

class VarDec(object):
  @staticmethod
  def is_mytype(tokenizer):
    tok = tokenizer.tok_ahead()
    if tok == "var": return True
    return False
    
  def __init__(self):
    self.type = None
    self.names = []

  def parse(self, tokenizer):
    # var type varName (, varName)
    keyword = tokenizer.tok_advance()
    datatype = tokenizer.tok_advance()
    name = tokenizer.tok_advance()
    
    assert keyword == "var"
    assert type(name) is Terminator
    assert name.type == "identifier"
    print("----- VarDec Start -----")  
    print(f"{keyword} {datatype} {name}")
    
    self.type = datatype
    self.names.append(name)
    while True:
      symbol = tokenizer.tok_advance()
      if symbol == ";":
        break
      assert symbol == ","
      
      name = tokenizer.tok_advance()
      assert type(name) is Terminator
      assert name.type == "identifier"

      print(f"{symbol} {name}")
      
      self.names.append(name)
    
    print("----- VarDec End -----")  
      

class SubroutineBody(object):
  @staticmethod
  def is_mytype(tokenizer):
    tok = tokenizer.tok_ahead()
    if tok == "{": return True
    return False
  
  def __init__(self):
    self.var_decs = []
    self.statements = None
  
  def parse(self, tokenizer):
    # { varDec* statements }
    symbol_l = tokenizer.tok_advance()
    assert symbol_l == "{"
    
    print("------ SubroutineBody Start ------")
    print(symbol_l)
    ## Parse varDecs ##
    while VarDec.is_mytype(tokenizer):
      print("[Parsing VarDec]")
      var_dec = VarDec()
      var_dec.parse(tokenizer)
      self.var_decs.append(var_dec)
    
    ## Parse Statements ##
    print("[Parsing Statements]")
    assert Statements.is_mytype(tokenizer)
    statements = Statements()
    statements.parse(tokenizer)
    self.statements = statements
    
    symbol_r = tokenizer.tok_advance()
    assert symbol_r == "}"
    print(symbol_r)
    print("------ SubroutineBody End ------")


class ParameterList(object):
  @staticmethod
  def is_mytype(tokenizer):
    return True
 
  def __init__(self):
    self.params_list = []
  
  def parse(self, tokenizer):
    # If you hit here, ParamsList is not empty
    # type varName (, type varName)*
    print("------ ParameterList Start ------")
      
    while True:
      if tokenizer.tok_ahead() == ")":
        break

      datatype = tokenizer.tok_advance()
      name = tokenizer.tok_advance()
      print("[Parsing Parameter Start]")
      print(f"{datatype} {name}")
      assert type(name) is Terminator
      assert name.type == "identifier"
      
      self.params_list.append(tuple(datatype, name))

      if tokenizer.tok_ahead() == ",":
        tokenizer.tok_advance()
      else:
        break
      print("[Parsing Parameter End]")
    print("------ ParameterList End ------")


class SubroutineDec(object):
  @staticmethod
  def is_mytype(tokenizer):
    tok = tokenizer.tok_ahead()
    if tok in ["constructor", "function", "method"]: return True
    return False
  
  def __init__(self):
    self.decorator = None
    self.type = None
    self.name = None
    self.params_list = None
    self.subroutine_body = None

  def parse(self, tokenizer):
    # (constructor|function|method) (void|type) subroutineName (parameterList) subroutineBody
    decorator = tokenizer.tok_advance()
    datatype = tokenizer.tok_advance()
    name = tokenizer.tok_advance()
    ## First Part ##
    assert decorator in ["constructor", "function", "method"]
    assert type(name) is Terminator
    assert name.type == "identifier"

    self.decorator = decorator
    self.type = datatype
    self.name = name
    
    print("------ SubroutineDec Start ------")
    print(f"{decorator} {datatype} {name}")

    ## Second Part: ParamsList ##
    symbol_l = tokenizer.tok_advance()
  
    print(symbol_l)
  
    assert symbol_l == "("
    if ParameterList.is_mytype(tokenizer):
      # In case of empty, is_mytype() will return False
      print("[Parsing ParameterList]")
      parameter_list = ParameterList()
      parameter_list.parse(tokenizer)
      symbol_r = tokenizer.tok_advance()
    assert symbol_r == ")"
    print(symbol_r)
    
    self.params_list = parameter_list    
    
    ## Third Part: SubroutineBody ##
    assert SubroutineBody.is_mytype(tokenizer)
    print("[Parsing SubroutineBody]")
    subroutine_body = SubroutineBody()
    subroutine_body.parse(tokenizer)
    
    self.subroutine_body = subroutine_body
    
    print("------ SubroutineDec End ------")

class ClassVarDec(object):
  @staticmethod
  def is_mytype(tokenizer):
    tok = tokenizer.tok_ahead()
    if tok in ["static", "field"]: return True
    return False

  def __init__(self):
    self.decorator = None
    self.type = None
    self.names = []

  def parse(self, tokenizer):
    # (static|field) type varName (, varName);
    decorator = tokenizer.tok_advance()
    datatype = tokenizer.tok_advance()
    name = tokenizer.tok_advance()

    assert decorator in ["static", "field"]
    assert type(name) is Terminator
    assert name.type == "identifier"
    
    print("------ ClassVarDec Start ------")
    print(f"{decorator} {datatype} {name}")

    self.decorator = decorator
    self.type = datatype
    self.names.append(name)

    while True:
      # (, varName);
      symbol = tokenizer.tok_advance()
      if symbol == ";":
        break

      assert symbol == ","
      name = tokenizer.tok_advance()
      assert type(name) is Terminator
      assert name.type == "identifier"

      self.names.append(name)

    print("------ ClassVarDec End ------")


class Class(object):
  @staticmethod
  def is_mytype(tokenizer):
    tok = tokenizer.tok_ahead()
    if tok == "class": return True
    return False
  
  def __init__(self):
    self.name = None
    self.classVarDec = []
    self.subroutineDec = []

  def parse(self, tokenizer):
    # class className { classVarDec* subroutineDec* }
    keyword = tokenizer.tok_advance()
    class_name = tokenizer.tok_advance()
    symbol_l = tokenizer.tok_advance()
    
    assert keyword == "class"
    assert type(class_name) is Terminator
    assert class_name.type == "identifier"
    assert symbol_l == "{"
  
    print("------ Class Start ------")
    print(f"{keyword} {class_name} {symbol_l}")

    self.name = class_name
    while ClassVarDec.is_mytype(tokenizer):
        print("[Parsing ClassVarDec]")
        cvd = ClassVarDec()
        cvd.parse(tokenizer)
        self.classVarDec.append(cvd)
    
    while SubroutineDec.is_mytype(tokenizer):
        print("[Parsing SubroutineDec]")
        sd = SubroutineDec()
        sd.parse(tokenizer)
        self.subroutineDec.append(sd)
    
    symbol_r = tokenizer.tok_advance()
    assert symbol_r == "}"
    
    print(symbol_r)
    print("------ Class End ------")

