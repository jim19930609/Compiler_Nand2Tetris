from lib.tokenizer import Tokenizer
from lib.classes import Class

class AllTypes(object):
  plain_types = ["int", "char", "boolean"]
  class_types = ["Array", "Math", "String", "Memory", "Keyboard", "Output"]

class Parser(object):
  def __init__(self, filenames):
    self.tokenizer = Tokenizer()
    self.classes = []
    self.filenames = filenames

  def parse_program(self):
    for filename in self.filenames:
      self.tokenizer.load_file(filename)
      self.classes.append(self.parse_class())

  def parse_class(self):
    assert Class.is_mytype(self.tokenizer)
    c = Class(AllTypes)
    c.parse(self.tokenizer)
    AllTypes.class_types.append(c.name.val)

    return c

if __name__ == "__main__":
  #parser = Parser(["unit_tests/FunctionDec/Main.jack"])
  parser = Parser(["unit_tests/ArrayInit/Main.jack"])
  parser.parse_program()

  print("!!!!!!!!!!!!!!!!!!")
  print("!!!!!!!!!!!!!!!!!!")
  print("!!!!!!!!!!!!!!!!!!")
  class0 = parser.classes[0]
  code = class0.codegen()

  # Call Main
  code += ["call Main.main 0", "pop temp 0"]
  for c in code:
    print(c)
