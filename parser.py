from lib.tokenizer import Tokenizer
from lib.classes import Class

class AllTypes(object):
  plain_types = ["int", "char", "boolean"]
  class_types = ["Math", "String", "Memory", "Keyboard", "Output"]

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
  parser = Parser(["/Users/zhanlueyang/Desktop/Compiler_Nand2Tetris/nand2tetris/projects/11/Average/Main.jack"])
  parser.parse_program()

  class0 = parser.classes[0]
  code = class0.codegen()

  for c in code:
    print(c)
