def variable_lookup(var_name, symtab_l, symtab_c):
  var_info = None
  if var_name in symtab_l.keys():
    var_info = symtab_l[var_name]
  elif var_name in symtab_c.keys():
    var_info = symtab_c[var_name]
  else:
    raise "Unrecognized variable in subroutineCall"
  
  return var_info
