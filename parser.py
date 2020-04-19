from lib.tokenizer import Tokenizer
from lib.classes import Class

class AllTypes(object):
  types = set(["int", "char", "boolean"])

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
    c = Class()
    c.parse(self.tokenizer)
    AllTypes.types.add(c.name)

    return c

if __name__ == "__main__":
  parser = Parser(["nand2tetris/projects/10/ExpressionLessSquare/Main.jack"])
  #parser = Parser(["nand2tetris/projects/10/ExpressionLessSquare/Square.jack"])
  #parser = Parser(["nand2tetris/projects/10/ExpressionLessSquare/SquareGame.jack"])
  parser.parse_program()
