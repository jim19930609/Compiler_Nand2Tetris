from tokenizer import Tokenizer
from lib.classes import Class

class AllTypes(object):
  types = set("int", "char", "boolean")


class Parser(object):
  def __init__(self, filenames):
    self.tokenizer = Tokenizer()
    self.classes = []
    self.filenames = filenames

  def parse_program(self):
    for filename in self.filenames:
      self.tokenizer.load_file(filename)
      self.classes.append(parse_class())

  def parse_class(self):
    assert Class.is_mytype(self.tokenizer)
    c = Class()
    c.parse(tokenizer)
    AllTypes.types.add(c.name)

    return c

