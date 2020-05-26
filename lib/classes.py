from lib.tokenizer import Terminator
from lib.statements import Statements

class GlobalTracer(object):
  def __init__(self, compiled_types):
    self.static_index = 0
    self.label_index = 0
    self.compiled_types = compiled_types
    self.curr_class_name = None
  
  def get_static_index(self):    
    index = self.static_index
    self.static_index += 1
    return index
    
  def get_label(self):
    label = f"Label_{self.label_index}"
    self.label_index += 1
    return label
  
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
      
  def codegen(self, symtab_l, local_index):
    self.names = [v.val for v in self.names]
    for name in self.names:
      symtab_l[name] = {}
      symtab_l[name]["kind"] = "local"
      symtab_l[name]["type"] = self.type
      symtab_l[name]["index"] = local_index
      local_index += 1
    return symtab_l, local_index

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
    
  def codegen(self, symtab_l, symtab_c, global_tracer):
    code = []
    local_index = 0
    for var_dec in self.var_decs:
      symtab_l, local_index = var_dec.codegen(symtab_l, local_index)
    code += self.statements.codegen(symtab_l, symtab_c, global_tracer)
    return code

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
      
      self.params_list.append([datatype, name])

      if tokenizer.tok_ahead() == ",":
        tokenizer.tok_advance()
      else:
        break
      print("[Parsing Parameter End]")
    print("------ ParameterList End ------")

  def codegen(self, global_tracer, is_method):
    argument_index = 0
    if is_method:
      argument_index = 1
    symtab_l = {}
    
    # [[type, name], ...]
    self.params_list = [[v[0], v[1].val] for v in self.params_list]
    for param in self.params_list:
      dtype, name = param
      if type(name) is Terminator:
        name = name.val
      if type(dtype) is Terminator:
        dtype = dtype.val
      # Check if type is known
      class_types = global_tracer.compiled_types.class_types
      plain_types = global_tracer.compiled_types.plain_types
      assert dtype in class_types + plain_types
    
      symtab_l[name] = {}
      symtab_l[name]["kind"] = "argument"
      symtab_l[name]["type"] = dtype
      symtab_l[name]["index"] = argument_index
      argument_index += 1
    return symtab_l

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
  
  def codegen(self, class_name, symtab_c, global_tracer):
    # Init local symtab
    # var_name : {"kind", "index"}
    
    self.name = self.name.val
    num_local_var = 0
    for var_dec in self.subroutine_body.var_decs:
      num_local_var += len(var_dec.names)

    code = [f"function {class_name}.{self.name} {num_local_var}"]
    if self.decorator == "constructor":
      symtab_l = self.params_list.codegen(global_tracer, is_method=False)
      # Number of local variables
      num_arg_var   = len([v for v in symtab_c.keys() if symtab_c[v]["kind"] != "static"])
      
      # Memory Alloc
      code += [f"push constant {num_arg_var}", "call Memory.alloc 1", "pop pointer 0"]
      code += self.subroutine_body.codegen(symtab_l, symtab_c, global_tracer)
      
    elif self.decorator == "method":
      symtab_l = self.params_list.codegen(global_tracer, is_method=True)
      # Set this to pointer 0
      code += ["push argument 0", "pop pointer 0"]
      code += self.subroutine_body.codegen(symtab_l, symtab_c, global_tracer)
    
    elif self.decorator == "function":
      symtab_l = self.params_list.codegen(global_tracer, is_method=False)
      code += self.subroutine_body.codegen(symtab_l, symtab_c, global_tracer)
    else:
      raise "Error"

    return code
    
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
  
  def codegen(self, symtab_c, global_tracer, class_name, field_index):
    # Update symtab_c
    class_types = global_tracer.compiled_types.class_types
    plain_types = global_tracer.compiled_types.plain_types
    if type(self.type) is Terminator:
      self.type = self.type.val
    assert self.type in class_types + plain_types
    self.names = [v.val for v in self.names]
    for name in self.names:
      symtab_c[name] = {}
      if self.decorator == "static":
        static_index = global_tracer.get_static_index()
        symtab_c[name]["kind"] = "static"
        symtab_c[name]["type"] = self.type
        symtab_c[name]["index"] = static_index
      elif self.decorator == "field":
        symtab_c[name]["kind"] = "this"
        symtab_c[name]["type"] = self.type
        symtab_c[name]["index"] = field_index
        field_index += 1
      else:
        raise "Unrecognized decorator during code gen for classVarDec"
    return symtab_c, field_index

class Class(object):
  @staticmethod
  def is_mytype(tokenizer):
    tok = tokenizer.tok_ahead()
    if tok == "class": return True
    return False
  
  def __init__(self, compiled_types):
    self.global_tracer = GlobalTracer(compiled_types)
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
  
  def codegen(self):
    code = []
    symtab_c = {}
    self.name = self.name.val
    self.global_tracer.curr_class_name = self.name
    
    field_index = 0
    for classVarDec in self.classVarDec:
      symtab_c, field_index = classVarDec.codegen(symtab_c, self.global_tracer, self.name, field_index)
    
    for subroutineDec in self.subroutineDec:
      code += subroutineDec.codegen(self.name, symtab_c, self.global_tracer)
    
    return code
